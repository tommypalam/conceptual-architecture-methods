"""Joint PD/MoR endpoint wording screen using all three approved paraphrases."""
import argparse
import asyncio
from copy import deepcopy
from hashlib import sha256
import json
import logging
import math
import re
from scipy.stats import norm, beta
from itertools import combinations
from engine.validity_variants import load_reviewed_paraphrases, variant_prompt
import os
from pathlib import Path
import zipfile

import pandas as pd
import utils
from engine.llm_client import utc_now_iso
from engine.validity_analysis import analyze, VALUES
from engine.validity_followup import gradient_comparison
from engine.validity_sweep import digest, freeze
from run_validity_claude import save_new
import run_validity_evidence_screen as base
import run_validity_mor_curve as curve
import run_validity_pd_interaction as previous_run

ROOT = base.ROOT
PREVIOUS = curve.BASE / 'pd_interaction_20260911'
PARAPHRASES = curve.BASE / 'claude_paraphrases_20260909_theory_r5/paraphrases_approved.json'
SWEEP = curve.BASE / 'option_c_20260909_restart'
GRADIENTS = curve.BASE / 'gradients_20260909_final'
ARMS = ('canonical', 'paraphrase_1', 'paraphrase_2', 'paraphrase_3')
CAP = 3.5
N = 30
PLANNED = 480


def prepare(root):
    if base.N!=N: raise ValueError('Frozen schedule does not match N30')
    prior=json.loads((PREVIOUS/'manifest.json').read_bytes());base.check(prior)
    previous_run.report(PREVIOUS,prior)
    ledger=json.loads((PREVIOUS/'budget_ledger.json').read_bytes())
    if ledger['pending_requests'] or ledger['cumulative_conservative_charge_usd']+CAP>9:
        raise ValueError('Conservative charge plus cap exceeds original allowance')
    templates=load_reviewed_paraphrases(PARAPHRASES)
    source=json.loads((SWEEP/'manifest.json').read_bytes())
    if digest(source['design'])!=source['design_hash']:raise ValueError('Source design mismatch')
    cells=[]
    for arm in ARMS:
        for pd_value in (.1,.9):
            for mor in (.1,.9):
                origin=next(c for c in source['design']['cells'] if
                            (c['arm'],c['parameter'],c['problem'],c['value'])==('full_harness','MoR','S3',mor))
                canonical,meta=variant_prompt('MoR',mor,'hybrid')
                if canonical!=origin['messages'][0]['content'] or meta['parameter_values']!=origin['profile']:
                    raise ValueError('Canonical rendering differs from frozen source')
                system,provenance=variant_prompt('MoR',mor,'hybrid',template=templates.get(arm))
                if provenance['parameter_values']!=origin['profile']:raise ValueError('Representation changed profile')
                system=previous_run.replace_pd(system,pd_value)
                profile={**origin['profile'],'PD':pd_value};messages=deepcopy(origin['messages']);messages[0]['content']=system
                if arm=='canonical':
                    prior_cell=next(c for c in prior['design']['cells'] if c['background_value']==pd_value and c['value']==mor)
                    if messages!=prior_cell['messages'] or profile!=prior_cell['profile']:raise ValueError('Canonical corner differs from prior diagnostic')
                cells.append({'arm':arm,'wording':f'PD{pd_value:.1f}_MoR{mor:.1f}'.replace('.','p'),
                              'parameter':'MoR','value':mor,'pd_value':pd_value,'problem':'S3','n':N,
                              'labels':['ADOPT','WAIT'],'profile':profile,'messages':messages})
    hashes=dict(prior['design']['source_hashes'])
    for path in (Path(__file__),PREVIOUS/'manifest.json',PREVIOUS/'budget_ledger.json',PREVIOUS/'analysis/verification.json',
                 PARAPHRASES,ROOT/'code/engine/validity_variants.py',ROOT/'code/engine/prompt_assembly.py',ROOT/'code/engine/phase0b.py'):
        hashes[path.relative_to(ROOT).as_posix()]=sha256(path.read_bytes()).hexdigest()
    d={'experiment':'joint_PD_MoR_endpoint_wording_screen','phase':'phase1_5_encoding_validity',
       'configuration':'neutral','model':base.MODEL,'provider':'openai','temperature':1.,'max_tokens':600,
       'seed':20260923,'planned_calls':PLANNED,'n_per_scientific_condition':N,'cells':cells,'source_hashes':hashes,
       'pricing':prior['design']['pricing'],'spending_ceiling_usd':CAP,'original_allowance_usd':9.,
       'prior_settled_token_estimate_usd':ledger['cumulative_token_estimate_usd'],
       'prior_unknown_usage_reserved_usd':ledger['unknown_timeout_reserved_usd'],
       'prior_conservative_charge_usd':ledger['cumulative_conservative_charge_usd'],'prior_pending_requests':0,
       'transport_timeout_seconds':180,
       'primary':'Screen all six wording pairs within each of four fixed profiles for an absolute rate difference exceeding.10. Simultaneous>=95% coverage from16 Bonferroni-adjusted exact binomial cell intervals; propagate to all24 paired differences including unknown outcomes. At least one interval entirely outside[-.10,.10] detects a gross local wording failure. Otherwise unresolved, not equivalence or a pass.',
       'secondary':'Within each wording, MoR endpoint effects at both PD levels and the high-PD minus low-PD endpoint-effect contrast; exact conservative intervals nominal across these secondary comparisons.',
       'manipulation':'Use canonical and ALL3 exact human-approved r5 system templates, rendered with the same ten intended values and neutral context; PD and MoR crossed at.1/.9. No generated revisions or selection of the best wording. User dilemma, labels and response instructions unchanged.',
       'scope':'Selected local joint-profile stress screen.16 cells,N30, fresh concurrent canonical controls. Not a full curve, slope replication, paraphrase battery replacement or mechanism test. No attribution to the wording of a specific trait since all approved endpoint descriptions vary together.',
       'collection':'30 shuffled complete16-cell blocks, concurrency3, unique seeds, one attempt, fixed480 fresh responses; no historical pooling.',
       'stop_rule':'Stop on API/model/usage/reservation failure; preserve all attempts and intents; no retries, in-place replacements, outcome-based extensions or automatic next study. Any terminal failure invalidates the screen.',
       'decision_rule':'Detected gross difference limits transport of the local fixed-template finding. No detected difference means inconclusive at this precision, not equivalence; no sample inflation to chase a pass. Report every wording/profile and secondary effect regardless of direction. No revised theory, original gate or Phase2 launch.',
       'budget_policy':'Cap$3.50 and prior conservative charge including unknown timeout stay below original$9; no provider balance or cache discount assumed.',
       'authorization_basis':'Researcher instructed continued progress after fixed-text PD diagnostic; exact existing approved wordings, four-profile allocation and spending cap are made reviewable before sending.'}
    d['full_dispatch_reserve_usd']=sum(base.reserve(c,d)*N for c in cells)
    if d['full_dispatch_reserve_usd']>CAP:raise ValueError('Full reserve exceeds cap')
    m=freeze(root/'manifest.json',d);save_new(root/'request_preview.json',{'design_hash':m['design_hash'],'cells':cells})
    return m


def assess(rows,planned):
    cells=[]
    for arm in ARMS:
        for pd_value in (.1,.9):
            for mor in (.1,.9):
                group=[r for r in rows if (r['arm'],planned[r['record_key']][0]['pd_value'],planned[r['record_key']][0]['value'])==(arm,pd_value,mor)]
                valid=[r for r in group if r['parse_status']=='ok' and not r['terminal_failure']]
                k=sum(r['parsed_decision']=='ADOPT' for r in valid);unknown=N-len(valid);tail=.05/(2*16)
                lower=0. if k==0 else float(beta.ppf(tail,k,N-k+1))
                upper=1. if k+unknown==N else float(beta.ppf(1-tail,k+unknown+1,N-k-unknown))
                cells.append({'arm':arm,'pd_value':pd_value,'mor_value':mor,'n_expected':N,'n_recorded':len(group),
                              'n_valid':len(valid),'n_invalid':len(group)-len(valid),'n_missing':N-len(group),
                              'adopt':k,'rate':k/len(valid) if valid else None,'wilson95':base.wilson(k,len(valid)),
                              'simultaneous95_cell_interval_unknown_envelope':[lower,upper]})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(cells),'All480 planned slots retained in16 wording/profile cells',logging.getLogger('joint-wording'))
    lookup={(c['arm'],c['pd_value'],c['mor_value']):c for c in cells};pairs=[]
    for pd_value in (.1,.9):
        for mor in (.1,.9):
            for a,b in combinations(ARMS,2):
                ca,cb=lookup[a,pd_value,mor],lookup[b,pd_value,mor]
                la,ha=ca['simultaneous95_cell_interval_unknown_envelope'];lb,hb=cb['simultaneous95_cell_interval_unknown_envelope']
                interval=[lb-ha,hb-la]
                pairs.append({'pd_value':pd_value,'mor_value':mor,'a':a,'b':b,'contrast':'b minus a',
                              'difference':cb['rate']-ca['rate'] if ca['rate'] is not None and cb['rate'] is not None else None,
                              'simultaneous95_interval_unknown_envelope':interval,'gross_difference_over_10pp':interval[0]>.10 or interval[1]<-.10})
    secondary=[]
    for arm in ARMS:
        effects={str(p):base.contrast([(lookup[arm,p,.9],1),(lookup[arm,p,.1],-1)]) for p in (.1,.9)}
        interaction=base.contrast([(lookup[arm,.9,.9],1),(lookup[arm,.9,.1],-1),(lookup[arm,.1,.9],-1),(lookup[arm,.1,.1],1)])
        secondary.append({'arm':arm,'mor_endpoint_effects_by_pd':effects,'high_pd_minus_low_pd_endpoint_effect':interaction})
    terminal=sum(r['terminal_failure'] for r in rows);quality=all(c['n_valid']/N>=.98 for c in cells)
    n_gross=sum(p['gross_difference_over_10pp'] for p in pairs)
    status=('INCOMPLETE' if len(rows)!=PLANNED else 'INVALID_SCREEN' if terminal or not quality else
            'GROSS_LOCAL_WORDING_FAILURE_DETECTED' if n_gross else 'NO_GROSS_DIFFERENCE_DETECTED_NOT_VALIDATED')
    return {'status':status,'n_records':len(rows),'n_valid':sum(c['n_valid'] for c in cells),'cells':cells,
            'wording_pair_contrasts':pairs,'n_pairs_detecting_gross_difference':n_gross,
            'secondary_nominal':secondary,'n_terminal_failures':terminal,'n_missing_usage':sum(base.cost(r) is None for r in rows),
            'recorded_token_estimate_usd':sum(base.cost(r) or 0 for r in rows),'historical_records_pooled':False,
            'phase_gate':'Unchanged. This local screen cannot establish full paraphrase equivalence or phase validity.'}


def score(root,m):
    planned,rows,_ = base.inventory(root,m)
    result = assess(rows,planned); result['design_hash']=m['design_hash']
    save_new(root/'analysis'/f'wording_{digest(result)[:16]}.json',result)
    return result


def check_authorization(root,m):
    a=json.loads((root/'dispatch_authorization.json').read_bytes())
    if (a['design_hash']!=m['design_hash'] or a['exact_messages_hash']!=digest([c['messages'] for c in m['design']['cells']])
            or a['planned_calls']!=PLANNED or a['spending_ceiling_usd']!=CAP):
        raise ValueError('Authorization scope mismatch')


def report(root,m):
    planned,rows,seen=base.inventory(root,m); check_authorization(root,m)
    if len(rows)!=PLANNED or seen!=set(planned): raise ValueError('Incomplete allocation')
    ids=[r['api_call_id'] for r in rows]
    if len(set(ids))!=PLANNED or any(not i or i.startswith('mock-') for i in ids): raise ValueError('API IDs invalid')
    if any(r['terminal_failure'] or r['attempts']!=1 or r['provider']!='openai' or r['model_version']!=base.MODEL for r in rows):
        raise ValueError('Unresolved response failure')
    intents=[json.loads(p.read_bytes()) for p in (root/'dispatches').rglob('*.json')]
    if len(intents)!=PLANNED or {i['record_key'] for i in intents}!=seen: raise ValueError('Dispatch mismatch')
    for i in intents:
        if i!=base.dispatch_intent(i['record_key'],planned[i['record_key']][0],m): raise ValueError('Invalid reservation')
    reserved=sum(i['reserved_usd'] for i in intents)
    if reserved>CAP or m['design']['prior_conservative_charge_usd']+reserved>9: raise ValueError('Budget guard exceeded')
    backup=json.loads((root/'local_backup.json').read_bytes()); archive=Path(backup['path'])
    if sha256(archive.read_bytes()).hexdigest()!=backup['sha256']: raise ValueError('Backup hash mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip(): raise ValueError('Corrupt ZIP')
        for key in seen:
            rel='records/'+key+'.json'
            if z.read(rel)!=(root/rel).read_bytes(): raise ValueError('Raw ZIP mismatch')
    result=score(root,m); current=result['recorded_token_estimate_usd']; cumulative=current+m['design']['prior_settled_token_estimate_usd']; conservative=cumulative+m['design']['prior_unknown_usage_reserved_usd']
    save_new(root/'analysis/verification.json',{'design_hash':m['design_hash'],'unique_real_api_ids':len(set(ids)),
             'unique_requested_seeds':len({r['seed'] for r in rows}),'exact_sources_requests_profiles_and_reservations':True,
             'raw_zip_payloads_verified':True,'reserved_usd':reserved})
    save_new(root/'budget_ledger.json',{'original_allowance_usd':9,'screen_cap_usd':CAP,'recorded_token_estimate_usd':current,
             'cumulative_token_estimate_usd':cumulative,'remaining_original_allowance_conservative_usd':9-conservative,
             'cumulative_conservative_charge_usd':conservative,'unknown_timeout_reserved_usd':m['design']['prior_unknown_usage_reserved_usd'],
             'pending_requests':0,'current_dispatched_reservations_usd':reserved,
             'provider_balance_verified':False,'automatic_expansion':False})
    lines=['# Joint-profile wording screen','',f"Status: **{result['status']}**.",
           f'{PLANNED} fresh calls;{result["n_valid"]} valid; known cost${current:.6f}.',
           f'Cumulative conservative charge${conservative:.6f}; remaining${9-conservative:.6f}.','',
           '| Wording | PD | MoR | ADOPT / valid | Wilson95% interval |','|---|---|---|---|---|']
    for c in result['cells']:
        lines.append(f"| {c['arm']} | {c['pd_value']} | {c['mor_value']} | {c['adopt']}/{c['n_valid']} | {c['wilson95']} |")
    lines+=['','Primary:24 wording-pair contrasts, with simultaneous>=95% intervals from16 exact cell bounds.',
            f"Pairs with interval entirely outside+/-.10: {result['n_pairs_detecting_gross_difference']}.",
            '```json',json.dumps(result['wording_pair_contrasts'],indent=2),'```','',
            'Secondary nominal endpoint effects and their PD contrasts:','```json',json.dumps(result['secondary_nominal'],indent=2),'```','',
            'No detected difference is not equivalence. This small local screen cannot pass the full paraphrase battery.',
            'All three previously approved paraphrases used; exact retained meanings not revised. All ten values and original user message retained.',
            f'Model {base.MODEL}; neutral; temperature1; max600;N30 per cell;seed20260923.',
            'Exact requests, approval provenance, unique API IDs, reservations and raw ZIP bytes verified. Same-computer archive. No automatic expansion.','']
    target=root/'analysis/WORDING_REPORT.md'; data='\n'.join(lines).encode('utf-8')
    if target.exists() and target.read_bytes()!=data: raise ValueError('Preserve differing report')
    if not target.exists(): target.write_bytes(data)
    print(json.dumps({'status':result['status'],'cost_usd':current,'report':str(target)}))


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--prepare-only',action='store_true'); p.add_argument('--report-only',action='store_true'); p.add_argument('--yes',action='store_true')
    a=p.parse_args(); root=a.run_root.resolve()
    if a.prepare_only:
        m=prepare(root); print(json.dumps({k:m['design'][k] for k in ('planned_calls','spending_ceiling_usd','full_dispatch_reserve_usd')})); return
    m=json.loads((root/'manifest.json').read_bytes()); base.check(m)
    if a.report_only: report(root,m); return
    if not a.yes or not os.environ.get('OPENAI_API_KEY'): p.error('Need --yes and configured key')
    check_authorization(root,m)
    import msvcrt
    from openai import AsyncOpenAI
    logs=ROOT/'output'/root.name; logs.mkdir(parents=True,exist_ok=True)
    async def run():
        client=base.SingleAttemptOpenAI(base.MODEL,concurrency=3,max_retries=1,timeout_s=m['design']['transport_timeout_seconds'])
        async with AsyncOpenAI(base_url='https://api.openai.com/v1',max_retries=0,timeout=m['design']['transport_timeout_seconds']) as sdk:
            client._client=sdk; await base.execute(root,m,client)
    with (logs/'execution.lock').open('a+b') as lock:
        lock.write(b'0'); lock.flush(); lock.seek(0); msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        try: asyncio.run(run())
        finally:
            result=score(root,m); base.archive(root,m)
            (logs/'status.json').write_text(json.dumps({'status':result['status'],'timestamp_utc':utc_now_iso()}),encoding='utf-8')
        report(root,m)


if __name__=='__main__': main()
