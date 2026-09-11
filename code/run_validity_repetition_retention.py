"""Focused repetition representation screen; frozen transport and original rules."""
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
from engine.validity_analysis import analyze, VALUES
from engine.validity_followup import gradient_comparison
from engine.validity_sweep import digest, freeze
from run_validity_claude import save_new
import run_validity_evidence_screen as base
import run_validity_mor_curve as curve

ROOT = base.ROOT
PREVIOUS = curve.BASE / 'mor_curve_20260911'
GRADIENTS = curve.BASE / 'gradients_20260909_final'
ARMS = ('full_harness', 'numeric_only', 'verbal_only')
CAP = 3.
PLANNED = 450


def prepare(root):
    prior = json.loads((PREVIOUS/'manifest.json').read_bytes()); base.check(prior)
    # Reconcile the completed previous run before releasing its unused reservations.
    _, settled, seen = base.inventory(PREVIOUS, prior)
    ledger = json.loads((PREVIOUS/'budget_ledger.json').read_bytes())
    intents = [json.loads(p.read_bytes()) for p in (PREVIOUS/'dispatches').rglob('*.json')]
    if (len(settled) != 300 or len(intents) != 300 or {i['record_key'] for i in intents} != seen
            or ledger['pending_requests'] or any(r['terminal_failure'] or base.cost(r) is None for r in settled)):
        raise ValueError('Previous dispatches must be settled before allocating this screen')
    if abs(sum(base.cost(r) for r in settled) - ledger['recorded_token_estimate_usd']) > 1e-9:
        raise ValueError('Previous actual usage estimate mismatch')
    if ledger['cumulative_token_estimate_usd'] + CAP > 9:
        raise ValueError('Settled cost plus new cap exceeds original allowance')
    gradient = json.loads((GRADIENTS/'manifest.json').read_bytes())
    if digest(gradient['design']) != gradient['design_hash']: raise ValueError('Gradient manifest damaged')
    cells = []
    for arm in ARMS:
        for value in VALUES:
            canonical = [c for c in prior['design']['cells'] if c['arm']=='repetition' and c['value']==value]
            if len(canonical)!=1: raise ValueError('Missing canonical repetition cell')
            canonical = canonical[0]
            if arm == 'full_harness': origin = deepcopy(canonical)
            else:
                matches = [c for c in gradient['design']['cells'] if
                           (c['variant'],c['parameter'],c['problem'],c['value'])==(arm,'MoR','S3',value)]
                if len(matches)!=1: raise ValueError('Missing gradient cell')
                origin = deepcopy(matches[0])
            if origin['profile'] != canonical['profile']: raise ValueError('Profile differs across representation')
            origin['messages'][-1] = deepcopy(canonical['messages'][-1])
            cells.append({'arm':arm,'wording':f'MoR_v{value:.1f}'.replace('.','p'),
                          'parameter':'MoR','value':value,'problem':'S3','n':base.N,
                          'labels':['ADOPT','WAIT'],'profile':origin['profile'],'messages':origin['messages']})
    hashes = dict(prior['design']['source_hashes'])
    for path in (Path(__file__), PREVIOUS/'manifest.json',PREVIOUS/'budget_ledger.json',
                 PREVIOUS/'analysis/verification.json', GRADIENTS/'manifest.json',
                 ROOT/'code/engine/validity_followup.py'):
        hashes[path.relative_to(ROOT).as_posix()] = sha256(path.read_bytes()).hexdigest()
    d = {'experiment':'MoR_S3_repetition_representation_screen','phase':'phase1_5_encoding_validity',
         'configuration':'neutral','model':base.MODEL,'provider':'openai','temperature':1.,
         'max_tokens':600,'seed':20260918,'planned_calls':PLANNED,'cells':cells,'source_hashes':hashes,
         'pricing':prior['design']['pricing'],'spending_ceiling_usd':CAP,'original_allowance_usd':9.,
         'prior_settled_token_estimate_usd':ledger['cumulative_token_estimate_usd'],
         'historical_dispatched_reservations_usd':ledger['cumulative_dispatched_reservations_usd'],
         'prior_pending_requests':0,
         'budget_policy':'Past completed reservations are historical bounds, not unspent liabilities. Verified settled full-rate usage plus this full reservation/cap must stay below $9. No extra top-up assumed.',
         'primary':'Both representation-retention checks under the original rule, conditional on this fresh canonical repetition curve meeting the original directional criterion. No substituted historical baseline.',
         'retention_rule':'Complete >=98%-valid five-value variant; positive fitted slope, absolute slope/canonical slope >=.5. Original point-estimate rule; no extra variant monotonicity or significance requirement.',
         'control_rule':'Complete >=98%-valid five-value canonical curve; positive logistic slope LR p<.05, endpoint h>=.20, observed monotonicity. Otherwise retention not assessable.',
         'scope':'One parameter, known S3, all ten intended values preserved; numeric-only removes all endpoint text, verbal-only uses existing six-bin rendering. Not a full battery, paraphrase test, or proof of understanding.',
         'collection':'30 shuffled complete 15-cell blocks, concurrency 3, one attempt, fixed N. All 450 observations fresh; prior results not pooled.',
         'stop_rule':'Stop on API/model/usage/reservation failure. Preserve failures and unresolved intents. No retries, outcome-based stopping or automatic expansion.',
         'authorization_basis':'User go follows recommendation of focused numeric/verbal retention test with fresh control; exact allocation is made reviewable here.'}
    d['full_dispatch_reserve_usd'] = sum(base.reserve(c,d)*c['n'] for c in cells)
    if d['full_dispatch_reserve_usd'] > CAP: raise ValueError('Screen reserve exceeds cap')
    m = freeze(root/'manifest.json',d)
    save_new(root/'request_preview.json',{'design_hash':m['design_hash'],'cells':cells})
    return m


def assess(rows, planned):
    converted = []
    for r in rows:
        c = planned[r['record_key']][0]
        converted.append({**r,'swept_parameter':'MoR','sweep_value':c['value'],'labels':c['labels']})
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame([{k:r[k] for k in ('arm','sweep_value','parse_status','parsed_decision')} for r in converted]),
                                'All collected retention observations retained',logging.getLogger('retention'))
    result = analyze(converted,params=['MoR'],problems=['S3'],arms=list(ARMS),n=base.N)
    canonical = next(s for s in result['sweeps'] if s['arm']=='full_harness')
    cells = [{**c,'variant':s['arm'],'parameter':'MoR','problem':'S3'} for s in result['sweeps']
             if s['arm']!='full_harness' for c in s['cells']]
    utils.log_dataframe_summary(pd.DataFrame(cells),'10 variant summary cells; 5 canonical cells retained as reference',logging.getLogger('retention'))
    retention = gradient_comparison(cells,[canonical])
    terminal = sum(r['terminal_failure'] for r in rows)
    quality = all(s['parse_quality_98pct'] for s in result['sweeps'])
    status = ('INCOMPLETE' if len(rows)!=PLANNED else 'INVALID_SCREEN' if terminal or not quality
              else 'RETENTION_NOT_ASSESSABLE_CONTROL_CRITERION_NOT_MET' if not canonical['criterion_met']
              else 'BOTH_RETENTION_CHECKS_MET_NOT_VALIDATED' if all(r['criterion_met'] for r in retention)
              else 'RETENTION_CRITERION_NOT_MET')
    result.update({'status':status,'retention':retention,'n_terminal_failures':terminal,
                   'n_missing_usage':sum(base.cost(r) is None for r in rows),
                   'recorded_token_estimate_usd':sum(base.cost(r) or 0 for r in rows),
                   'historical_records_pooled':False})
    return result


def score(root,m):
    planned,rows,_ = base.inventory(root,m)
    result = assess(rows,planned); result['design_hash']=m['design_hash']
    save_new(root/'analysis'/f'retention_{digest(result)[:16]}.json',result)
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
    if reserved>CAP or m['design']['prior_settled_token_estimate_usd']+reserved>9: raise ValueError('Budget guard exceeded')
    backup=json.loads((root/'local_backup.json').read_bytes()); archive=Path(backup['path'])
    if sha256(archive.read_bytes()).hexdigest()!=backup['sha256']: raise ValueError('Backup hash mismatch')
    with zipfile.ZipFile(archive) as z:
        if z.testzip(): raise ValueError('Corrupt ZIP')
        for key in seen:
            rel='records/'+key+'.json'
            if z.read(rel)!=(root/rel).read_bytes(): raise ValueError('Raw ZIP mismatch')
    result=score(root,m); current=result['recorded_token_estimate_usd']; cumulative=current+m['design']['prior_settled_token_estimate_usd']
    save_new(root/'analysis/verification.json',{'design_hash':m['design_hash'],'unique_real_api_ids':len(set(ids)),
             'unique_requested_seeds':len({r['seed'] for r in rows}),'exact_sources_requests_profiles_and_reservations':True,
             'raw_zip_payloads_verified':True,'reserved_usd':reserved})
    save_new(root/'budget_ledger.json',{'original_allowance_usd':9,'screen_cap_usd':CAP,'recorded_token_estimate_usd':current,
             'cumulative_token_estimate_usd':cumulative,'remaining_original_allowance_estimate_usd':9-cumulative,
             'pending_requests':0,'historical_dispatched_reservations_usd':m['design']['historical_dispatched_reservations_usd']+reserved,
             'provider_balance_verified':False,'automatic_expansion':False})
    lines=['# Repetition representation screen','',f"Status: **{result['status']}**.",
           f'{PLANNED} calls; full-rate token estimate ${current:.6f}; cumulative ${cumulative:.6f}.',
           f'Original allowance estimate remaining ${9-cumulative:.6f}; provider balance not checked.','',
           '| Representation | ADOPT counts /30 at .1/.3/.5/.7/.9 | Fitted slope (95% CI) | LR p | Original directional criterion |',
           '|---|---|---|---|---|']
    for s in result['sweeps']:
        f=s['fit']; counts='/'.join(str(c['opt0_count']) for c in s['cells'])
        lines.append(f"| {s['arm']} | {counts} | {f.get('slope')} ({f.get('ci95')}) | {f.get('p_value')} | {s['criterion_met']} |")
    lines+=['','Variant directional criteria above are descriptive, not additional retention requirements.','',
            '| Variant | Assessable | Absolute slope ratio to fresh canonical | Direction matches | Retention criterion |',
            '|---|---|---|---|---|']
    for r in result['retention']:
        lines.append(f"| {r['variant']} | {r['assessment']} | {r['absolute_logit_slope_ratio']} | {r['direction_matches']} | {r['criterion_met']} |")
    lines+=['','Original retention rule uses fitted point ratios, not ratio confidence bounds or equivalence tests.',
            'A failed fresh canonical criterion makes retention not assessable; no historical baseline substitution.',
            'All data are fresh; one parameter on known S3. Six-bin verbal mapping and all other profile values unchanged.',
            'No paraphrase, internal-understanding or phase-pass claim. No automatic expansion.',
            f'Model {base.MODEL}; neutral; temperature 1; output cap 600; seed 20260918.',
            'Exact source/request/profile hashes, unique real API IDs, reservations and raw ZIP bytes verified. Same-computer backup.','']
    target=root/'analysis/RETENTION_REPORT.md'; data='\n'.join(lines).encode('utf-8')
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
        client=base.SingleAttemptOpenAI(base.MODEL,concurrency=3,max_retries=1,timeout_s=90)
        async with AsyncOpenAI(base_url='https://api.openai.com/v1',max_retries=0,timeout=90) as sdk:
            client._client=sdk; await base.execute(root,m,client)
    with (logs/'execution.lock').open('a+b') as lock:
        lock.write(b'0'); lock.flush(); lock.seek(0); msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
        try: asyncio.run(run())
        finally:
            result=score(root,m); base.archive(root,m)
            (logs/'status.json').write_text(json.dumps({'status':result['status'],'timestamp_utc':utc_now_iso()}),encoding='utf-8')
        report(root,m)


if __name__=='__main__': main()
