"""Prepare/run the reviewed four-condition PD/S3 wording diagnostic; offline by default."""
import argparse
import asyncio
import hashlib
import json
import logging
import os
from pathlib import Path
import random

import pandas as pd
import utils
from engine.llm_client import LLMClient,Message
from engine.parsing import parse_decision,parse_reasoning
from engine.seeding import derive_seed
from engine.validity_followup import comparison_design,summarize_cells
from engine.validity_sweep import ValiditySink,digest,freeze
from engine.validity_variants import load_reviewed_paraphrases,PARAMETER_RE
from run_validity_claude import save_new
from run_validity_restart_followups import archive
from validity_wording_factorial import mix_endpoints,CONTRASTS,analyze_counts

ROOT=Path(__file__).resolve().parents[1]


def prepare(source_root,review_bundle,root,n=300):
    templates=load_reviewed_paraphrases(review_bundle)
    p2,p3=templates['paraphrase_2'],templates['paraphrase_3']
    combinations={'A':p2,'B':mix_endpoints(p3,p2),'C':mix_endpoints(p2,p3),'D':p3}
    # Reuse the tested canonical validation/assembly, then retain only PD/S3.
    d=comparison_design(source_root,'paraphrases',n=n,seed=20260910,provider='openai',
        paraphrases={f'paraphrase_{i}':t for i,t in enumerate([p2,combinations['B'],combinations['C']],1)})
    selected=[c for c in d['cells'] if c['parameter']=='PD' and c['problem']=='S3']
    last=comparison_design(source_root,'paraphrases',n=n,seed=20260910,provider='openai',
        paraphrases={'paraphrase_1':p3,'paraphrase_2':p3,'paraphrase_3':p3})
    selected.append(next(c for c in last['cells'] if c['parameter']=='PD' and c['problem']=='S3'))
    for name,c in zip(combinations,selected): c['variant']=name
    d.update(experiment='wording_factorial_PD_S3',cells=selected,variants=list(combinations),
        planned_calls=4*n,seed=20260910,concurrency=4,
        sampling=f'{n} randomized complete blocks; one request per condition per block; distinct condition-specific seeds',
        power_plan_hash=digest(json.loads((root/'power_plan.json').read_text(encoding='utf-8'))),
        template_hashes={k:digest(v) for k,v in combinations.items()},
        source_review_bundle_hash=digest(json.loads(review_bundle.read_text(encoding='utf-8'))),
        diagnostic_source_hashes={name:hashlib.sha256((ROOT/'code'/name).read_bytes()).hexdigest()
            for name in ('validity_wording_factorial.py','run_validity_wording_factorial.py')},
        analysis={'status':'Exploratory, post-hoc-selected profile; no Phase 1.5 gate amendment',
            'contrasts':{k:v.tolist() for k,v in CONTRASTS.items()},
            'method':'Four Bonferroni exact binomial rate intervals, alpha=.05; weighted simultaneous contrast bounds',
            'unknown_decisions':'Expand bounds over all binary completions of invalid responses',
            'parse_floor':.98,'reporting':'Valid-only estimates plus unknown-expanded intervals; below parse floor: descriptive only',
            'meaningful_effects':{'main':.20,'interaction':.40},
            'small_effect_limitation':'Low power for 10pp main and 20pp interaction; no null-equals-absence claim'},
        stopping='Fixed N per condition; stop after current four-request block on terminal API/model error; preserve all failures')
    manifest=freeze(root/'manifest.json',d)
    review={'design_hash':manifest['design_hash'],'reviewer':None,'approved':False,
        'condition_template_hashes':d['template_hashes'],
        'condition_messages_hashes':{c['variant']:digest(c['messages']) for c in selected},
        'scope':'New mixtures B/C need human review; A/D are unchanged previously approved templates'}
    save_new(root/'review_pending.json',review)
    lines=['# PD/S3 wording factorial: exact mixed-template review', '',
        'Only B and C are new combinations. All endpoint wording was already reviewed in paraphrases 2 and 3.',
        'No definition, numeric value, dilemma, context or non-endpoint scaffold is rewritten.',
        'Approve B and C together to authorise these exact combinations; the original A/D approval is retained.', '',
        '| Condition | PD wording | Other nine descriptions | Status |',
        '|---|---|---|---|', '| A | P2 | P2 | Previously approved P2 |',
        '| B | P3 | P2 | New combination; review pending |',
        '| C | P2 | P3 | New combination; review pending |',
        '| D | P3 | P3 | Previously approved P3 |', '',
        '## The only substituted endpoint pair','',
        '| Version | PD low endpoint | PD high endpoint |','|---|---|---|']
    for name,t in [('P2',p2),('P3',p3)]:
        m=list(PARAMETER_RE.finditer(t))[5]; lines.append(f'| {name} | {m[4]} | {m[5]} |')
    for c in selected:
        name=c['variant']; lines.extend(['',f'## Condition {name}', '',
            f'Template hash: `{d["template_hashes"][name]}`',
            f'Exact request-messages hash: `{digest(c["messages"])}`','',
            '### System message','', '```text',c['messages'][0]['content'],'```','',
            '### User message (same for every condition)','', '```text',c['messages'][1]['content'],'```'])
    content='\n'.join(lines)+'\n'; path=root/'HUMAN_REVIEW.md'
    if path.exists() and path.read_text(encoding='utf-8')!=content: raise ValueError('Existing review differs')
    path.write_text(content,encoding='utf-8')
    return manifest


def require_approval(manifest,path):
    r=json.loads(path.read_text(encoding='utf-8')); d=manifest['design']
    if r.get('approved') is not True or not r.get('reviewer') or r.get('design_hash')!=manifest['design_hash']:
        raise ValueError('Exact mixed-template human review is pending')
    if r.get('condition_template_hashes')!=d['template_hashes'] or r.get('condition_messages_hashes')!={c['variant']:digest(c['messages']) for c in d['cells']}:
        raise ValueError('Approval does not match the frozen templates/messages')


async def execute(manifest,client,sink):
    d=manifest['design']; existing=list(sink.read_all()); seen={r['record_key'] for r in existing}
    expected={f"{c['variant']}/PD/S3/0.8/call_{k:04d}" for c in d['cells'] for k in range(1,d['n']+1)}
    if len(seen)!=len(existing) or not seen<=expected: raise ValueError('Unexpected or duplicate existing records')
    if any(r['design_hash']!=manifest['design_hash'] or r.get('error_message') or r.get('model_version_mismatch') for r in existing):
        raise ValueError('Mixed design or preserved terminal failure; cannot resume in place')
    if digest(d)!=manifest['design_hash']: raise ValueError('Invalid manifest')
    for name,h in d['source_hashes'].items():
        if hashlib.sha256((ROOT/'code/engine'/name).read_bytes()).hexdigest()!=h: raise ValueError('Frozen engine source changed')
    for name,h in d['diagnostic_source_hashes'].items():
        if hashlib.sha256((ROOT/'code'/name).read_bytes()).hexdigest()!=h: raise ValueError('Frozen diagnostic source changed')

    async def one(c,k):
        key=f"{c['variant']}/PD/S3/0.8/call_{k:04d}"
        seed=derive_seed(d['seed'],d['experiment'],c['variant'],k)
        result=await client.complete([Message(**m) for m in c['messages']],temperature=d['temperature'],max_tokens=d['max_tokens'],seed=seed)
        decision,status=parse_decision(result.text,tuple(c['labels']))
        expected_model=d['model']+'-mock' if d['provider']=='mock' else d['model']
        mismatch=result.ok and result.model_version!=expected_model
        row={'schema_version':'1.0','phase':d['phase'],'experiment':d['experiment'],
            'design_hash':manifest['design_hash'],'record_key':key,'variant':c['variant'],
            'swept_parameter':'PD','sweep_value':.8,'problem_id':'S3','labels':c['labels'],
            'agent_parameters':c['profile'],'call_index':k,'seed':seed,'randomized_block':k,
            'timestamp_utc':result.timestamp_utc,'model_version':result.model_version,
            'model_version_mismatch':bool(mismatch),'provider':result.provider,
            'api_call_id':result.api_call_id,'attempts':result.attempts,
            'request_messages':result.request_messages,'response_payload':result.raw_response,
            'raw_response':result.text,'parsed_decision':decision,'parsed_reasoning':parse_reasoning(result.text),
            'parse_status':'failed_api' if result.error else 'model_mismatch' if mismatch else status,
            'error_message':result.error}
        row['record_hash']=digest(row); sink.write(key,row)
        if result.error or mismatch: sink.write_failure({'record_key':key,'error':result.error,'model_mismatch':bool(mismatch)})
        return not (result.error or mismatch)

    rng=random.Random(d['seed'])
    for k in range(1,d['n']+1):
        cells=list(d['cells']); rng.shuffle(cells)
        pending=[c for c in cells if f"{c['variant']}/PD/S3/0.8/call_{k:04d}" not in seen]
        if pending:
            outcomes=await asyncio.gather(*(one(c,k) for c in pending))
            if not all(outcomes): raise RuntimeError('Terminal failure preserved; stopped after block')
        if k==1 or k%25==0 or k==d['n']: print(f'Block {k}/{d["n"]}; planned calls {d["planned_calls"]}',flush=True)


def score(root,manifest):
    rows=list(ValiditySink(root/'records').read_all()); summary=summarize_cells(manifest,rows)
    ordered=[next(c for c in summary['cells'] if c['variant']==name) for name in 'ABCD']
    complete=all(c['n_recorded']==c['n_expected'] for c in ordered)
    valid=all(c['n_valid']/c['n_expected']>=.98 for c in ordered)
    terminal=any(r.get('error_message') or r.get('model_version_mismatch') for r in rows)
    result={'design_hash':manifest['design_hash'],'configuration':'neutral','seed':20260910,
        'status':'EXPLORATORY_DIAGNOSTIC_COMPLETE' if complete and valid and not terminal else 'INCOMPLETE_PARSE_FLOOR_OR_TERMINAL_FAILURE',
        'cells':ordered,'contrast_analysis':analyze_counts([c['opt0_count'] for c in ordered],
            [c['n_expected'] for c in ordered],[c['n_invalid']+c['n_missing'] for c in ordered]),
        'phase_gate':'Unchanged; not met by the completed original battery'}
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(ordered),'Factorial conditions, none dropped',logging.getLogger('factorial'))
    path=root/'analysis'/f'factorial_{digest(result)[:16]}.json'; save_new(path,result)
    if complete: archive(root)
    print(path,flush=True)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--source-root',type=Path)
    p.add_argument('--review-bundle',type=Path)
    p.add_argument('--prepare-only',action='store_true')
    p.add_argument('--score-only',action='store_true')
    p.add_argument('--approval',type=Path)
    p.add_argument('--yes',action='store_true')
    a=p.parse_args(); root=a.run_root.resolve()
    if a.prepare_only:
        if not a.source_root or not a.review_bundle: p.error('Preparation needs source and reviewed bundle')
        m=prepare(a.source_root.resolve(),a.review_bundle.resolve(),root)
        print(f'Prepared {m["design"]["planned_calls"]} calls; no API calls; review {root/"HUMAN_REVIEW.md"}')
        return
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    if digest(m['design'])!=m['design_hash']: raise ValueError('Invalid manifest')
    if a.score_only:
        score(root,m)
        return
    if not a.yes or not a.approval or not os.environ.get('OPENAI_API_KEY'): p.error('Real calls need --yes, --approval and configured key')
    require_approval(m,a.approval)
    import msvcrt
    lock=(root/'execution.lock').open('a+b'); lock.write(b'0'); lock.flush(); lock.seek(0)
    msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
    client=LLMClient(model=m['design']['model'],concurrency=4)
    try: asyncio.run(execute(m,client,ValiditySink(root/'records')))
    finally: score(root,m)


if __name__=='__main__': main()
