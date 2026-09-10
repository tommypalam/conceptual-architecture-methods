"""Prepare and run the Phase 1.5 PD low/high endpoint diagnostic, offline by default."""
import argparse
import asyncio
from copy import deepcopy
import hashlib
import json
import logging
import os
from pathlib import Path

import pandas as pd
import utils
from engine.llm_client import LLMClient, utc_now_iso
from engine.validity_followup import summarize_cells
from engine.validity_sweep import ValiditySink, digest, freeze
from engine.validity_variants import PARAMETER_RE, load_reviewed_paraphrases
from run_validity_claude import save_new
from run_validity_restart_followups import archive
from run_validity_wording_factorial import ROOT, execute, require_approval
from validity_wording_factorial import CONTRASTS, analyze_counts

NAMES=dict(zip(CONTRASTS,('low_endpoint_P2_minus_P3',
    'high_endpoint_P2_minus_P3','endpoint_interaction_difference_in_differences')))


def mix_pd(low_source,high_source,background):
    matches=[list(PARAMETER_RE.finditer(s)) for s in (low_source,high_source,background)]
    if any(len(m)!=10 or m[5][2]!='Procedural Dependence' for m in matches):
        raise ValueError('Expected ten parameters with PD in position six')
    result=background
    for group,source in ((5,matches[1][5]),(4,matches[0][5])):
        target=matches[2][5]
        result=result[:target.start(group)]+source[group]+result[target.end(group):]
    return result


def prepare(parent_root,bundle,root,n=300):
    if n<=0: raise ValueError('N must be positive')
    parent=json.loads((parent_root/'manifest.json').read_text(encoding='utf-8'))
    if digest(parent['design'])!=parent['design_hash']: raise ValueError('Parent integrity failure')
    require_approval(parent,parent_root/'review_approved.json')
    templates=load_reviewed_paraphrases(bundle)
    p2,p3=templates['paraphrase_2'],templates['paraphrase_3']
    pairs={'A':(p2,p2),'B':(p3,p2),'C':(p2,p3),'D':(p3,p3)}
    mixed={k:mix_pd(lo,hi,p2) for k,(lo,hi) in pairs.items()}
    prior={c['variant']:c for c in parent['design']['cells']}
    s2,s3=prior['A']['messages'][0]['content'],prior['B']['messages'][0]['content']
    sources={'A':(s2,s2),'B':(s3,s2),'C':(s2,s3),'D':(s3,s3)}
    cells=[]
    for name,(lo,hi) in sources.items():
        c=deepcopy(prior['A']); c['variant']=name
        c['messages'][0]['content']=mix_pd(lo,hi,s2)
        cells.append(c)
    assert cells[0]['messages']==prior['A']['messages']
    assert cells[3]['messages']==prior['B']['messages']
    # The same four-condition probability contrasts have the same planning power.
    power=json.loads((parent_root/'power_plan.json').read_text(encoding='utf-8'))
    encoded=json.dumps(power)
    for old,new in NAMES.items(): encoded=encoded.replace(old,new)
    encoded=encoded.replace('PD_main','low_endpoint_main').replace('other_nine_main','high_endpoint_main')
    power=json.loads(encoded)
    power['adaptation']='Unchanged mathematical design and simulated probabilities; factor names relabelled low/high. Planning seed retained; fresh collection seed 20260912.'
    power['source_power_plan_sha256']=hashlib.sha256((parent_root/'power_plan.json').read_bytes()).hexdigest()
    save_new(root/'power_plan.json',power)
    d=deepcopy(parent['design'])
    d.update(experiment='PD_low_high_endpoint_factorial',cells=cells,n=n,planned_calls=4*n,
        seed=20260912,parent_design_hash=parent['design_hash'],
        parent_root=str(parent_root.resolve()),
        sampling=f'{n} randomized four-request blocks, distinct condition/block seeds',
        template_hashes={k:digest(v) for k,v in mixed.items()},
        source_review_bundle_hash=digest(json.loads(bundle.read_text(encoding='utf-8'))),
        power_plan_hash=digest(power),
        factors={'low_endpoint':['P2','P3'],'high_endpoint':['P2','P3'],'other_nine':'P2 fixed'},
        selection='Exploratory: PD=.8/S3 and P2 background selected after earlier wording results; no historical responses pooled')
    d['analysis']['contrasts']={NAMES[k]:v.tolist() for k,v in CONTRASTS.items()}
    d['analysis']['status']='Exploratory endpoint attribution; original Phase 1.5 gate unchanged'
    d['analysis']['budget_usd']={'expected':1.35,'planning_reservation':5,
        'additional_budget_authorized':50,'note':'No enforced billing cap; reservation is not incurred spend'}
    for name in ('run_validity_pd_endpoints.py','run_validity_restart_followups.py','run_validity_claude.py'):
        d['diagnostic_source_hashes'][name]=hashlib.sha256((ROOT/'code'/name).read_bytes()).hexdigest()
    manifest=freeze(root/'manifest.json',d)
    review={'approved':False,'reviewer':None,'design_hash':manifest['design_hash'],
        'condition_template_hashes':d['template_hashes'],
        'condition_messages_hashes':{c['variant']:digest(c['messages']) for c in cells},
        'scope':'A/D equal previously approved factorial A/B; new split-endpoint combinations B/C require review'}
    save_new(root/'review_pending.json',review)
    lines=['# PD low/high endpoint diagnostic: exact-template review','',
        'Only the low and high PD endpoint sources vary. Other nine descriptions remain P2.',
        'A and D equal the previously approved factorial A and B; all four receive fresh data.',
        'B and C are the two new combinations. Their words are copied verbatim from approved P2/P3.','',
        '| Condition | Low PD endpoint | High PD endpoint | Review |','|---|---|---|---|']
    for name,t in mixed.items():
        m=list(PARAMETER_RE.finditer(t))[5]
        lines.append(f'| {name} | {m[4]} | {m[5]} | '+('New combination' if name in 'BC' else 'Previously approved')+' |')
    lines+=['','Assistant assessment: both mixed pairs retain outcome dominance with substantive secondary procedural value at the low end, and independent value of fair procedure at the high end. No intended definition or direction changes. Human review of the exact combinations remains separate.']
    for c in cells:
        lines+=['',f'## Condition {c["variant"]}','',f'Messages hash: `{digest(c["messages"])}`','']
        for message in c['messages']:
            lines += [f'### {message["role"]} message','','```text',message['content'],'```','']
    path=root/'HUMAN_REVIEW.md'; content='\n'.join(lines)+'\n'
    if path.exists() and path.read_text(encoding='utf-8')!=content: raise ValueError('Review changed')
    path.write_text(content,encoding='utf-8')
    return manifest


def score(root,manifest):
    rows=list(ValiditySink(root/'records').read_all())
    summary=summarize_cells(manifest,rows)
    ordered=[next(c for c in summary['cells'] if c['variant']==name) for name in 'ABCD']
    complete=all(c['n_recorded']==c['n_expected'] for c in ordered)
    valid=all(c['n_valid']/c['n_expected']>=.98 for c in ordered)
    terminal=any(r.get('error_message') or r.get('model_version_mismatch') for r in rows)
    analysis=analyze_counts([c['opt0_count'] for c in ordered],[c['n_expected'] for c in ordered],
        [c['n_invalid']+c['n_missing'] for c in ordered])
    analysis['contrasts']={NAMES[k]:v for k,v in analysis['contrasts'].items()}
    result={'design_hash':manifest['design_hash'],'configuration':'neutral',
        'seed':manifest['design']['seed'],'cells':ordered,'contrast_analysis':analysis,
        'status':'EXPLORATORY_DIAGNOSTIC_COMPLETE' if complete and valid and not terminal else 'INCOMPLETE_PARSE_FLOOR_OR_TERMINAL_FAILURE',
        'phase_gate':'Unchanged; this local diagnostic cannot close the original battery'}
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(ordered),'Endpoint cells; no exclusions',logging.getLogger('endpoints'))
    path=root/'analysis'/f'endpoints_{digest(result)[:16]}.json'; save_new(path,result)
    if complete: archive(root)
    print(path,flush=True)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--parent-root',type=Path)
    p.add_argument('--review-bundle',type=Path)
    p.add_argument('--prepare-only',action='store_true')
    p.add_argument('--score-only',action='store_true')
    p.add_argument('--approval',type=Path)
    p.add_argument('--yes',action='store_true')
    a=p.parse_args(); root=a.run_root.resolve()
    if a.prepare_only:
        if not a.parent_root or not a.review_bundle: p.error('Need parent run and reviewed bundle')
        m=prepare(a.parent_root.resolve(),a.review_bundle.resolve(),root)
        print(f'Prepared {m["design"]["planned_calls"]} calls; no API calls; review {root/"HUMAN_REVIEW.md"}')
        return
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    if digest(m['design'])!=m['design_hash']: raise ValueError('Invalid manifest')
    if a.score_only:
        score(root,m); return
    if not a.yes or not a.approval or not os.environ.get('OPENAI_API_KEY'):
        p.error('Real calls need --yes, exact approval and configured key')
    require_approval(m,a.approval)
    import msvcrt
    logs=ROOT/'output'/root.name; logs.mkdir(parents=True,exist_ok=True)
    with (logs/'execution.lock').open('a+b') as lock:
        lock.write(b'0'); lock.flush(); lock.seek(0)
        msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        def status(state):
            (logs/'status.json').write_text(json.dumps({'status':state,'timestamp_utc':utc_now_iso(),
                'design_hash':m['design_hash']},indent=2),encoding='utf-8')
        status('RUNNING')
        try:
            client=LLMClient(model=m['design']['model'],concurrency=4)
            try: asyncio.run(execute(m,client,ValiditySink(root/'records')))
            finally: result=score(root,m)
            status(result['status'])
        except BaseException:
            status('STOPPED_WITH_ERROR'); raise


if __name__=='__main__': main()
