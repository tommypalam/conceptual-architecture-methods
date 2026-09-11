"""Fixed-text PD background interaction with the MoR/S3 response."""
import argparse
import asyncio
from copy import deepcopy
from hashlib import sha256
import json
import logging
import math
import re
from scipy.stats import norm
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
import run_validity_profile_ablation as previous_run

ROOT = base.ROOT
PREVIOUS = curve.BASE / 'profile_ablation_20260911'
SWEEP = curve.BASE / 'option_c_20260909_restart'
GRADIENTS = curve.BASE / 'gradients_20260909_final'
ARMS = ('pd_low', 'pd_high')
CAP = 2.25
N = 30
PLANNED = 300


def replace_pd(system, value):
    old=' 6. Procedural Dependence: 0.56'
    if system.count(old)!=1: raise ValueError('Expected exact original PD value line')
    new=f' 6. Procedural Dependence: {value:.2f}'
    if len(old.encode())!=len(new.encode()): raise ValueError('PD substitution changed byte length')
    return system.replace(old,new,1)


def prepare(root):
    if base.N!=N: raise ValueError('Frozen schedule does not match N30')
    prior=json.loads((PREVIOUS/'manifest.json').read_bytes());base.check(prior)
    previous_run.report(PREVIOUS,prior)
    ledger=json.loads((PREVIOUS/'budget_ledger.json').read_bytes())
    if ledger['pending_requests'] or ledger['cumulative_conservative_charge_usd']+CAP>9:
        raise ValueError('Conservative charge plus cap exceeds original allowance')
    source=json.loads((SWEEP/'manifest.json').read_bytes())
    if digest(source['design'])!=source['design_hash']: raise ValueError('Source design mismatch')
    cells=[]
    for arm,pd_value in zip(ARMS,(.1,.9)):
        for value in VALUES:
            matches=[c for c in source['design']['cells'] if
                     (c['arm'],c['parameter'],c['problem'],c['value'])==('full_harness','MoR','S3',value)]
            if len(matches)!=1: raise ValueError('Missing canonical cell')
            origin=matches[0];messages=deepcopy(origin['messages']);profile=deepcopy(origin['profile'])
            messages[0]['content']=replace_pd(messages[0]['content'],pd_value);profile['PD']=pd_value
            cells.append({'arm':arm,'wording':f'MoR_v{value:.1f}'.replace('.','p'),
                          'parameter':'MoR','value':value,'problem':'S3','n':N,'labels':['ADOPT','WAIT'],
                          'background_parameter':'PD','background_value':pd_value,'profile':profile,
                          'source_full_profile':deepcopy(origin['profile']),'messages':messages})
    hashes=dict(prior['design']['source_hashes'])
    for path in (Path(__file__),PREVIOUS/'manifest.json',PREVIOUS/'budget_ledger.json',
                 PREVIOUS/'analysis/verification.json',SWEEP/'manifest.json',
                 ROOT/'Theory/concepts_as_architecture_thesis_v0_6.md'):
        hashes[path.relative_to(ROOT).as_posix()]=sha256(path.read_bytes()).hexdigest()
    d={'experiment':'PD_background_by_MoR_fixed_text_interaction_diagnostic','phase':'phase1_5_encoding_validity',
       'configuration':'neutral','model':base.MODEL,'provider':'openai','temperature':1.,'max_tokens':600,
       'seed':20260922,'planned_calls':PLANNED,'n_per_scientific_condition':N,'cells':cells,'source_hashes':hashes,
       'pricing':prior['design']['pricing'],'spending_ceiling_usd':CAP,'original_allowance_usd':9.,
       'prior_settled_token_estimate_usd':ledger['cumulative_token_estimate_usd'],
       'prior_unknown_usage_reserved_usd':ledger['unknown_timeout_reserved_usd'],
       'prior_conservative_charge_usd':ledger['cumulative_conservative_charge_usd'],'prior_pending_requests':0,
       'transport_timeout_seconds':180,
       'primary':'MoR grouped-binomial logistic slope at PD=.9 minus slope at PD=.1. Independent-arm Wald95% CI and two-sided p, no directional interaction hypothesis. Non-estimability explicit; no selected historical reference.',
       'secondary':'All ten rate/Wilson intervals, direct difference in endpoint probability changes using conservative exact binomial bounds, and MoR monotonicity descriptively. Secondary intervals nominal.',
       'manipulation':'All ten canonical entries, descriptions, order, wrappers, neutral context and entire user message retained. Change only PD numeric value from source0.56 to0.10 or0.90; MoR varies across five existing values. Same UTF8 message length at matched MoR. Other eight values remain at source means. Tokenization is not assumed identical.',
       'selection_basis':'Thesis AppendixA PD connects process versus outcome weighting to justice/authority/care; thesis11.3 includes PD in S3 activation cluster. Prior source PD/S3 response and unblinded process-related rationales motivate selection. Theory does not specify the sign or magnitude of a PD-by-MoR interaction; this is exploratory diagnosis, not a new confirmed theoretical mapping.',
       'scope':'Same-length fixed-text background-value contrast. A slope change would show background-value dependence with descriptions held fixed, not prove faithful psychological interaction or attribute the earlier deletion effect wholly to PD. Not a capacity test or paraphrase test.',
       'collection':'30 shuffled complete ten-cell blocks, concurrency3, unique seeds, one attempt, fixed300 fresh responses. No historical pooling or historical-only controls.',
       'stop_rule':'Stop on API/model/usage/reservation failure; preserve every attempt and intent. No retries, in-place replacements, outcome-based extension or automatic next run. Any terminal failure invalidates the diagnostic.',
       'monotonicity_rule':'Primary is the two-sided slope interaction, not a monotonicity gate. Report observed monotonicity and legacy directional summaries for both arms as descriptive only. Misses cannot waive the original phase criterion or prove intrinsic nonmonotonicity. A slope contrast does not qualify either arm for Phase2.',
       'decision_rule':'CI excluding zero: report a scoped background-value effect on fitted MoR slope. CI including zero: unresolved, not proof of no interaction or of a presentation mechanism. Pinned/separated fit: report non-estimability and rates; no alternative primary chosen after results. No reduced architecture or gate change.',
       'budget_policy':'Prior conservative charge including unknown timeout plus$2.25 cap remains below original$9. No provider balance, cached discount or release of unknown prior usage.',
       'authorization_basis':'Researcher agreed to identifying a theory-justified background contrast and instructed proceeding. Exact treatment, fresh300-call allocation and cap are made reviewable here before dispatch.'}
    d['full_dispatch_reserve_usd']=sum(base.reserve(c,d)*N for c in cells)
    if d['full_dispatch_reserve_usd']>CAP: raise ValueError('Full reserve exceeds cap')
    m=freeze(root/'manifest.json',d)
    save_new(root/'request_preview.json',{'design_hash':m['design_hash'],'cells':cells})
    return m


def assess(rows,planned):
    converted=[]
    for r in rows:
        c=planned[r['record_key']][0]
        converted.append({**r,'swept_parameter':'MoR','sweep_value':c['value'],'labels':c['labels']})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame([{k:r[k] for k in ('arm','sweep_value','parse_status','parsed_decision')} for r in converted]),
                                'All collected PD background observations retained',logging.getLogger('ablation'))
    result=analyze(converted,params=['MoR'],problems=['S3'],arms=list(ARMS),n=N)
    fits=[s['fit'] for s in result['sweeps']]
    contrast={'status':'not_estimable','estimate':None,'ci95':None,'p_two_sided':None,
              'method':'Independent-arm grouped-binomial logistic slope difference; Wald approximation, logit linearity and independent calls assumed'}
    if all(f['status']=='ok' for f in fits):
        delta=fits[1]['slope']-fits[0]['slope'];se=math.sqrt(sum(f['se']**2 for f in fits));z=float(norm.ppf(.975))
        contrast.update(status='estimated',estimate=delta,se=se,ci95=[delta-z*se,delta+z*se],p_two_sided=float(2*norm.sf(abs(delta/se))))
    lookup={}
    for s in result['sweeps']:
        for c in s['cells']:
            lookup[s['arm'],c['value']]={'adopt':c['opt0_count'],'n_expected':N,'n_valid':c['n_valid'],'rate':c['rate']}
    endpoint=base.contrast([(lookup['pd_high',.9],1),(lookup['pd_high',.1],-1),
                            (lookup['pd_low',.9],-1),(lookup['pd_low',.1],1)])
    terminal=sum(r['terminal_failure'] for r in rows)
    quality=all(s['parse_quality_98pct'] for s in result['sweeps'])
    status=('INCOMPLETE' if len(rows)!=PLANNED else 'INVALID_SCREEN' if terminal or not quality else
            'SLOPE_DIFFERENCE_NOT_ESTIMABLE' if contrast['status']!='estimated' else
            'MORE_POSITIVE_MOR_SLOPE_AT_HIGH_PD' if contrast['ci95'][0]>0 else
            'LESS_POSITIVE_MOR_SLOPE_AT_HIGH_PD' if contrast['ci95'][1]<0 else 'SLOPE_DIFFERENCE_UNRESOLVED')
    result.update(status=status,primary_slope_difference=contrast,secondary_endpoint_difference=endpoint,
                  n_terminal_failures=terminal,n_missing_usage=sum(base.cost(r) is None for r in rows),
                  recorded_token_estimate_usd=sum(base.cost(r) or 0 for r in rows),historical_records_pooled=False)
    return result


def score(root,m):
    planned,rows,_ = base.inventory(root,m)
    result = assess(rows,planned); result['design_hash']=m['design_hash']
    save_new(root/'analysis'/f'interaction_{digest(result)[:16]}.json',result)
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
    lines=['# Fixed-text PD background interaction diagnostic','',f"Status: **{result['status']}**.",
           f'{PLANNED} fresh calls; known cost ${current:.6f}; cumulative known ${cumulative:.6f}.',
           f'Conservative charge including prior unknown timeout ${conservative:.6f}; original allowance remaining ${9-conservative:.6f}.','',
           '| Arm | ADOPT counts /30 at .1/.3/.5/.7/.9 | Slope (95% CI) | Legacy directional criterion, descriptive only |',
           '|---|---|---|---|']
    for s in result['sweeps']:
        f=s['fit'];counts='/'.join(str(c['opt0_count']) for c in s['cells'])
        lines.append(f"| {s['arm']} | {counts} | {f.get('slope')} ({f.get('ci95')}) | {s['criterion_met']} |")
    lines+=['','Primary slope difference, PD=.9 minus PD=.1:',
            '```json',json.dumps(result['primary_slope_difference'],indent=2),'```','',
            'Secondary direct difference in endpoint probability changes:',
            '```json',json.dumps(result['secondary_endpoint_difference'],indent=2),'```','',
            'The primary assumes linear logits and independent binomial calls; counts and endpoint intervals retain a less model-dependent description.',
            'All ten entries, exact text and matched UTF8 message lengths stay fixed; only PD background value differs between arms.',
            'A background-value effect is not proof of faithful psychological interaction or an explanation of the entire deletion effect. No paraphrase, capacity or phase-pass claim.',
            f'Model {base.MODEL}; neutral context; temperature1; output cap600; N30 each; root seed20260922.',
            'Fixed300 calls, all responses fresh, exact retained text and requests verified, one attempt per slot.',
            'Raw ZIP bytes verified. Backup is on the same computer. No automatic further experiment.','']
    target=root/'analysis/INTERACTION_REPORT.md'; data='\n'.join(lines).encode('utf-8')
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
