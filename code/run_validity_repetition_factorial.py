"""Concurrent original/repetition endpoint comparison with frozen source messages."""
import argparse
import asyncio
from copy import deepcopy
from hashlib import sha256
import json
import logging
import os
from pathlib import Path
import zipfile

import pandas as pd
import utils
from engine.llm_client import utc_now_iso
from engine.validity_analysis import wilson
from engine.validity_sweep import digest, freeze
from run_validity_claude import save_new
import run_validity_evidence_screen as base

ROOT=base.ROOT
BASE=ROOT/'experiments/phase1_5_encoding_validity'
PREVIOUS=BASE/'repetition_retention_20260911'
SWEEP=BASE/'option_c_20260909_restart'
GRADIENTS=BASE/'gradients_20260909_final'
ARMS=('original','repetition')
REPRESENTATIONS=('full_harness','numeric_only','verbal_only')
VALUES=(.1,.9)
N=60
CAP=4.5
PLANNED=720


def prepare(root):
    if 2*base.N!=N:raise ValueError('Frozen scheduling allocation no longer matches N60')
    prior=json.loads((PREVIOUS/'manifest.json').read_bytes());base.check(prior)
    planned,settled,seen=base.inventory(PREVIOUS,prior)
    ledger=json.loads((PREVIOUS/'budget_ledger.json').read_bytes())
    intents=[json.loads(p.read_bytes()) for p in (PREVIOUS/'dispatches').rglob('*.json')]
    if (len(settled)!=450 or len(intents)!=450 or {i['record_key'] for i in intents}!=seen
            or ledger['pending_requests'] or any(r['terminal_failure'] or base.cost(r) is None for r in settled)):
        raise ValueError('Prior run is not fully settled')
    if any(i!=base.dispatch_intent(i['record_key'],planned[i['record_key']][0],prior) for i in intents):
        raise ValueError('Prior reservation mismatch')
    if abs(sum(base.cost(r) for r in settled)-ledger['recorded_token_estimate_usd'])>1e-9:
        raise ValueError('Prior cost mismatch')
    if ledger['cumulative_token_estimate_usd']+CAP>9:raise ValueError('Original allowance exceeded')
    sources={name:json.loads((path/'manifest.json').read_bytes()) for name,path in [('canonical',SWEEP),('gradient',GRADIENTS)]}
    if any(digest(m['design'])!=m['design_hash'] for m in sources.values()):raise ValueError('Source manifest mismatch')
    cells=[]
    for arm in ARMS:
        for representation in REPRESENTATIONS:
            for value in VALUES:
                rep=[c for c in prior['design']['cells'] if (c['arm'],c['value'])==(representation,value)]
                if len(rep)!=1:raise ValueError('Missing repetition cell')
                if representation=='full_harness':
                    original=[c for c in sources['canonical']['design']['cells'] if
                              (c['arm'],c['parameter'],c['problem'],c['value'])==('full_harness','MoR','S3',value)]
                else:
                    original=[c for c in sources['gradient']['design']['cells'] if
                              (c['variant'],c['parameter'],c['problem'],c['value'])==(representation,'MoR','S3',value)]
                if len(original)!=1:raise ValueError('Missing original cell')
                original=original[0];repeated=rep[0]
                if original['profile']!=repeated['profile'] or original['messages'][0]!=repeated['messages'][0]:
                    raise ValueError('Representation or profile changed across repetition contrast')
                chosen=original if arm=='original' else repeated
                # Two 30-call scheduling allocations implement N60 without editing the frozen transport.
                for allocation in (1,2):
                    cells.append({'arm':arm,'wording':f'{representation}_v{value:.1f}_a{allocation}'.replace('.','p'),
                                  'representation':representation,'value':value,'allocation':allocation,
                                  'parameter':'MoR','problem':'S3','n':base.N,'labels':['ADOPT','WAIT'],
                                  'profile':deepcopy(chosen['profile']),'messages':deepcopy(chosen['messages'])})
    hashes=dict(prior['design']['source_hashes'])
    for path in (Path(__file__),PREVIOUS/'manifest.json',PREVIOUS/'budget_ledger.json',
                 PREVIOUS/'analysis/verification.json',SWEEP/'manifest.json',GRADIENTS/'manifest.json'):
        hashes[path.relative_to(ROOT).as_posix()]=sha256(path.read_bytes()).hexdigest()
    d={'experiment':'concurrent_original_repetition_MoR_endpoint_factorial','phase':'phase1_5_encoding_validity',
       'configuration':'neutral','model':base.MODEL,'provider':'openai','temperature':1.,'max_tokens':600,
       'seed':20260919,'planned_calls':PLANNED,'n_per_scientific_condition':N,'cells':cells,'source_hashes':hashes,
       'spending_ceiling_usd':CAP,'pricing':prior['design']['pricing'],
       'prior_settled_token_estimate_usd':ledger['cumulative_token_estimate_usd'],
       'historical_dispatched_reservations_usd':ledger['historical_dispatched_reservations_usd'],
       'original_allowance_usd':9.,'prior_pending_requests':0,
       'primary':'Verbal-only average ADOPT probability: repetition minus original, equally weighting .1/.9. Conservative >=95% exact interval using four independent cells. Negative interval supports repetition-associated suppression for these conditions.',
       'secondary':'Endpoint .9-minus-.1 effects in six arm/representation conditions and direct repetition-minus-original endpoint-effect contrasts in each representation; conservative exact intervals, nominal not family-adjusted.',
       'scope':'Two endpoints only, same-batch randomised schedule, N60 each. No full curve, retention, equivalence, mechanism or phase-pass inference. No historical pooling.',
       'collection':'30 shuffled 24-allocation blocks; each of 12 scientific cells has two indistinguishable-message 30-call allocations, aggregated to N60. Independent unique-seed calls, concurrency3, one attempt.',
       'decision_rule':'Negative primary interval: do not scale repetition, retain original as reference. Otherwise suppression unresolved, not equivalence or repetition validated. Positive endpoints can motivate a separately frozen full-curve confirmation; no automatic outcome-based expansion.',
       'stop_rule':'Fixed N; stop on API/model/usage/budget failure. Preserve all attempts and intents; no retry or in-place replacement.',
       'authorization_basis':'Researcher explicitly approved carrying out all proposed steps while maintaining objective and limitations, aiming to finish Phase1.5 today. This exact bounded allocation is now reviewable.'}
    d['full_dispatch_reserve_usd']=sum(base.reserve(c,d)*c['n'] for c in cells)
    if d['full_dispatch_reserve_usd']>CAP:raise ValueError('Dispatch reserve exceeds cap')
    m=freeze(root/'manifest.json',d)
    save_new(root/'request_preview.json',{'design_hash':m['design_hash'],'cells':cells})
    return m


def assess(rows,planned):
    cells=[]
    for arm in ARMS:
        for representation in REPRESENTATIONS:
            for value in VALUES:
                group=[r for r in rows if (r['arm'],planned[r['record_key']][0]['representation'],planned[r['record_key']][0]['value'])==(arm,representation,value)]
                valid=[r for r in group if r['parse_status']=='ok' and not r['terminal_failure']]
                k=sum(r['parsed_decision']=='ADOPT' for r in valid)
                cells.append({'arm':arm,'representation':representation,'value':value,'n_expected':N,
                              'n_recorded':len(group),'n_valid':len(valid),'n_invalid':len(group)-len(valid),'n_missing':N-len(group),
                              'adopt':k,'rate':k/len(valid) if valid else None,'ci95':wilson(k,len(valid))})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(cells),'All records retained: 24 scheduling allocations -> 12 scientific conditions, N60 each',logging.getLogger('factorial'))
    by={(c['arm'],c['representation'],c['value']):c for c in cells}
    primary=base.contrast([(by['repetition','verbal_only',v],.5) for v in VALUES]+[(by['original','verbal_only',v],-.5) for v in VALUES])
    endpoints={f'{a}/{r}':base.contrast([(by[a,r,.9],1),(by[a,r,.1],-1)]) for a in ARMS for r in REPRESENTATIONS}
    interactions={r:base.contrast([(by['repetition',r,.9],1),(by['repetition',r,.1],-1),
                                  (by['original',r,.9],-1),(by['original',r,.1],1)]) for r in REPRESENTATIONS}
    lo,hi=primary['conservative_95_interval_unknown_envelope']
    terminal=sum(r['terminal_failure'] for r in rows)
    quality=all(c['n_valid']/N>=.98 for c in cells)
    status=('INCOMPLETE' if len(rows)!=PLANNED else 'INVALID_SCREEN' if terminal or not quality else
            'VERBAL_SUPPRESSION_DETECTED_NOT_VALIDATED' if hi<0 else 'VERBAL_INCREASE_DETECTED_NOT_VALIDATED' if lo>0 else 'VERBAL_REPETITION_EFFECT_UNRESOLVED')
    return {'status':status,'cells':cells,'primary_verbal_average_difference':primary,'endpoint_effects':endpoints,
            'endpoint_effect_interactions':interactions,'n_records':len(rows),'n_valid':sum(c['n_valid'] for c in cells),
            'n_terminal_failures':terminal,'n_missing_usage':sum(base.cost(r) is None for r in rows),
            'recorded_token_estimate_usd':sum(base.cost(r) or 0 for r in rows),'historical_records_pooled':False,
            'phase_gate':'Unchanged. Endpoint diagnostic, not full-curve or representation-validity pass.'}


def score(root,m):
    planned,rows,_=base.inventory(root,m);result=assess(rows,planned);result['design_hash']=m['design_hash']
    save_new(root/'analysis'/f'factorial_{digest(result)[:16]}.json',result);return result


def check_authorization(root,m):
    a=json.loads((root/'dispatch_authorization.json').read_bytes())
    if (a['design_hash']!=m['design_hash'] or a['exact_messages_hash']!=digest([c['messages'] for c in m['design']['cells']])
            or a['planned_calls']!=PLANNED or a['spending_ceiling_usd']!=CAP):raise ValueError('Authorization scope mismatch')


def report(root,m):
    planned,rows,seen=base.inventory(root,m);check_authorization(root,m)
    if len(rows)!=PLANNED or seen!=set(planned):raise ValueError('Incomplete allocation')
    ids=[r['api_call_id'] for r in rows]
    if len(set(ids))!=PLANNED or any(not i or i.startswith('mock-') for i in ids):raise ValueError('Invalid API IDs')
    if any(r['terminal_failure'] or r['attempts']!=1 or r['provider']!='openai' or r['model_version']!=base.MODEL for r in rows):raise ValueError('Unresolved API failure')
    intents=[json.loads(p.read_bytes()) for p in (root/'dispatches').rglob('*.json')]
    if len(intents)!=PLANNED or {i['record_key'] for i in intents}!=seen:raise ValueError('Dispatch mismatch')
    for i in intents:
        if i!=base.dispatch_intent(i['record_key'],planned[i['record_key']][0],m):raise ValueError('Reservation mismatch')
    reserved=sum(i['reserved_usd'] for i in intents)
    if reserved>CAP or reserved+m['design']['prior_settled_token_estimate_usd']>9:raise ValueError('Budget exceeded')
    backup=json.loads((root/'local_backup.json').read_bytes());archive=Path(backup['path'])
    if sha256(archive.read_bytes()).hexdigest()!=backup['sha256']:raise ValueError('Archive hash mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip():raise ValueError('Corrupt ZIP')
        for key in seen:
            rel='records/'+key+'.json'
            if z.read(rel)!=(root/rel).read_bytes():raise ValueError('Raw ZIP mismatch')
    result=score(root,m);cost=result['recorded_token_estimate_usd'];total=cost+m['design']['prior_settled_token_estimate_usd']
    save_new(root/'analysis/verification.json',{'design_hash':m['design_hash'],'unique_real_api_ids':len(set(ids)),
             'unique_requested_seeds':len({r['seed'] for r in rows}),'sources_requests_profiles_reservations_verified':True,'raw_zip_bytes_verified':True,'reserved_usd':reserved})
    save_new(root/'budget_ledger.json',{'original_allowance_usd':9,'screen_cap_usd':CAP,'recorded_token_estimate_usd':cost,
             'cumulative_token_estimate_usd':total,'remaining_original_allowance_estimate_usd':9-total,'pending_requests':0,
             'historical_dispatched_reservations_usd':m['design']['historical_dispatched_reservations_usd']+reserved,
             'provider_balance_verified':False,'automatic_expansion':False})
    lines=['# Concurrent original/repetition endpoint comparison','',f"Status: **{result['status']}**.",
           f'Collected {result["n_records"]}/{PLANNED}, valid {result["n_valid"]}. Estimated cost ${cost:.6f}; cumulative ${total:.6f}.',
           f'Original allowance remaining estimate ${9-total:.6f}; not provider account balance.','',
           '| Arm | Representation | MoR | ADOPT / valid | Wilson 95% interval |','|---|---|---|---|---|']
    for c in result['cells']:lines.append(f"| {c['arm']} | {c['representation']} | {c['value']} | {c['adopt']}/{c['n_valid']} | {c['ci95']} |")
    for title,key in [('Primary: verbal average repeated minus original','primary_verbal_average_difference'),
                      ('Secondary: within-condition endpoint effects','endpoint_effects'),('Secondary: repetition minus original endpoint effects','endpoint_effect_interactions')]:
        lines+=['',title,'```json',json.dumps(result[key],indent=2),'```']
    lines+=['','All contrast intervals are conservative >=95% exact-binomial envelopes; secondary family not adjusted.',
            'Fresh concurrent observations only. No inference from significance in one arm but not another.',
            f'Neutral; pinned model {base.MODEL}; temperature1; max600 output tokens; root seed20260919.',
            'All profiles, requests, unique IDs, reservations and raw ZIP bytes verified. Same-computer backup.',
            'Two endpoints do not establish continuous encoding, retention, paraphrase robustness, understanding, or phase closure.','']
    target=root/'analysis/FACTORIAL_REPORT.md';data='\n'.join(lines).encode()
    if target.exists() and target.read_bytes()!=data:raise ValueError('Preserve prior report')
    if not target.exists():target.write_bytes(data)
    print(json.dumps({'status':result['status'],'cost_usd':cost,'report':str(target)}))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--prepare-only',action='store_true');p.add_argument('--report-only',action='store_true');p.add_argument('--yes',action='store_true')
    a=p.parse_args();root=a.run_root.resolve()
    if a.prepare_only:
        m=prepare(root);print(json.dumps({k:m['design'][k] for k in ('planned_calls','spending_ceiling_usd','full_dispatch_reserve_usd')}));return
    m=json.loads((root/'manifest.json').read_bytes());base.check(m)
    if a.report_only:report(root,m);return
    if not a.yes or not os.environ.get('OPENAI_API_KEY'):p.error('Need --yes and configured key')
    check_authorization(root,m)
    import msvcrt
    from openai import AsyncOpenAI
    logs=ROOT/'output'/root.name;logs.mkdir(parents=True,exist_ok=True)
    async def run():
        client=base.SingleAttemptOpenAI(base.MODEL,concurrency=3,max_retries=1,timeout_s=90)
        async with AsyncOpenAI(base_url='https://api.openai.com/v1',max_retries=0,timeout=90) as sdk:
            client._client=sdk;await base.execute(root,m,client)
    with (logs/'execution.lock').open('a+b') as lock:
        lock.write(b'0');lock.flush();lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        try:asyncio.run(run())
        finally:
            result=score(root,m);base.archive(root,m)
            (logs/'status.json').write_text(json.dumps({'status':result['status'],'timestamp_utc':utc_now_iso()}),encoding='utf-8')
        report(root,m)


if __name__=='__main__':main()
