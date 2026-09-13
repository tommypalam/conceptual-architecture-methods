"""Prospective finite-rule moral pilot, immutable ledger and zero-call replay."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import zipfile

from engine.population import Population
from phase3_budget import BudgetStop, POLICY, digest, read_checked
from phase3_recognition_run import ROOT, LEDGER, network, charge, MODELS
from phase4_moral_transport import Ledger
from phase3_recognition_recovery import verify, sha, archived_evidence
from phase3_design_pilot import RATERS, JUDGE, review_value
from phase3_variant_round import save
from phase3_representation_diagnostic import contrast
from phase4_consequence_pilot_r3 import system, json_value, choice, job as prior_job
from phase4_consequence_tasks import TASK_IDS, task, transition, mapping, prompt
from phase4_moral_schema import RELATIVE, FIXED
from phase4_finite_rules import score

FOLDER=ROOT/'experiments/phase4_coding/consequence_rule_pilot_r1'
PARENT=ROOT/'experiments/phase4_coding/consequence_pilot_r3'
STUDY='consequence_rule_pilot_r1'
ARMS=('E','V','U','G')
N=6
SEED=2026091380
CAP=4_000_000_000
PRIOR=1_218_321_225
HISTORY=2338


def job(slot,*args):
    value=prior_job(slot,*args)
    value['slot']=f'{STUDY}/{slot}'
    return value


def review_job(pop):
    packet={'protocol':(FOLDER/'PROTOCOL.md').read_text(encoding='utf-8'),
        'rules':(FOLDER/'RULES.md').read_text(encoding='utf-8'),
        'prior_scoped_definitions':(PARENT/'MANUAL.md').read_text(encoding='utf-8'),
        'scorer_source':(ROOT/'code/phase4_finite_rules.py').read_text(encoding='utf-8'),
        'tasks':{t:prompt(t,1) for t in TASK_IDS},
        'outcomes':[score(t,a) for t in TASK_IDS for a in task(t)['actions']],
        'systems':{a:system(pop['agents'][0]['parameters'],a) for a in ARMS}}
    return job('review',JUDGE,
        'Independently review this prospective finite-rule exploratory moral-choice pilot. '
        'Check rule/manual correspondence for all twelve actions, causal effects, duties, '
        'fairness, polarity, aggregation, attribution, controls and inferential scope. '
        'Primary labels are operational normative conventions, not AI ratings or universal truth. '
        'Earlier AI-rating gates remain failed under a documented separate-method amendment. '
        'Flag concrete blocking errors, not merely small sample size or lack of human raters '
        'already disclosed. Do not reward likely positive results. Return JSON only with '
        'verdict accept/revise/reject, blocking_issues list, limits list; accept requires no '
        'blocking issues. Keep the complete JSON under 350 words.',
        json.dumps(packet,ensure_ascii=False,sort_keys=True),2048)


def participant_jobs(pop):
    batch=[]
    for agent in pop['agents']:
        block=[]
        for t in TASK_IDS:
            for arm in ARMS:
                j=job(f'participant/{agent["agent_id"]}/{t}/{arm}',RATERS[1],
                    system(agent['parameters'],arm),prompt(t,agent['agent_id']),64,1)
                j['cell']={'block':agent['agent_id'],'task':t,'arm':arm,'mapping':mapping(t,agent['agent_id'])}
                block.append(j)
        random.Random(SEED+1+agent['agent_id']).shuffle(block);batch.extend(block)
    return batch


def schedule(pop):return [review_job(pop)]+participant_jobs(pop)


def prepare(persist=False):
    parent,check=read_checked(PARENT/'release.json'),read_checked(PARENT/'CHECKPOINT.json')
    verify(parent);archived_evidence(check,LEDGER)
    with Ledger(LEDGER,parent) as ledger:
        if ledger.state['failed'] or ledger.state['pending'] or len(ledger.state['reservations'])!=HISTORY:
            raise BudgetStop('Unexpected parent evidence')
        providers=dict(ledger.state['providers'])
    pop=Population.draw(N,seed=SEED).to_dict();batch=schedule(pop)
    slots={j['slot']:{'kind':'moral_text','model':j['request']['model'],'input_token_bound':j['input_token_bound'],
        'reserved_nano':j['reserved_nano'],'max_output':j['request'].get('max_tokens',j['request'].get('max_completion_tokens')),
        'request_sha256':digest(j['request'])} for j in batch}
    bound=sum(j['reserved_nano'] for j in batch)
    for j in batch:providers[MODELS[j['request']['model']]]+=j['reserved_nano']
    if len(slots)!=97 or bound+PRIOR>CAP or providers['anthropic']>11_000_000_000 or providers['openai']>20_000_000_000:
        raise BudgetStop('Full schedule exceeds size/budget/reserve')
    paths=[Path(__file__),ROOT/'code/phase4_finite_rules.py',FOLDER/'PROTOCOL.md',FOLDER/'RULES.md',
           FOLDER.parent/'DETERMINISTIC_SCOPE_20260914.md']
    release={'id':STUDY,'population_sha256':digest(pop),'jobs_sha256':digest(batch),'slots':slots,
        'recognition_cap_nano':bound,'prior_screening_nano':PRIOR,'original_screening_cap_nano':CAP,
        'provider_caps_nano':parent['provider_caps_nano'],'parent_checkpoint_sha256':digest(check),
        'historical_keys':sorted(p.stem for p in (LEDGER/'records').glob('*.json')),
        'preserved_files':{p.relative_to(LEDGER).as_posix():sha(p) for p in LEDGER.rglob('*.json')},
        'failure_log_prefix_bytes':(LEDGER/'failures.jsonl').stat().st_size,
        'failure_log_prefix_sha256':sha(LEDGER/'failures.jsonl'),
        'source_sha256':{**parent['source_sha256'],**{p.relative_to(ROOT).as_posix():sha(p) for p in paths}}}
    with Ledger(LEDGER,release):pass
    if persist:
        save(FOLDER/'population.json',pop);save(FOLDER/'requests.json',batch);save(FOLDER/'release.json',release)
    return release,pop,batch


def analyze(rows,n):
    expected={(i,t,a) for i in range(1,n+1) for t in TASK_IDS for a in ARMS}
    if len(rows)!=len(expected) or {(r['block'],r['task'],r['arm']) for r in rows}!=expected:
        raise BudgetStop('Missing, duplicate or unexpected participant cells')
    out=[{**r,'outcome':None if r['action'] is None else score(r['task'],r['action'])} for r in rows]
    lookup={(r['block'],r['task'],r['arm']):r['outcome'] for r in out}
    cells=[];contrasts={}
    for t in TASK_IDS:
        possibilities=[score(t,a) for a in task(t)['actions']]
        lo=min(v['effects']['total_delta'] for v in possibilities)
        hi=max(v['effects']['total_delta'] for v in possibilities)
        for a in ARMS:
            selected=[lookup[i,t,a] for i in range(1,n+1)]
            valid=[v for v in selected if v is not None]
            def bounds(getter):
                limits=[getter(v) for v in possibilities]
                return [sum(getter(v) if v is not None else b for v in selected)/n for b in (min(limits),max(limits))]
            def mean(getter):return sum(getter(v) for v in valid)/len(valid) if valid else None
            c={'task':t,'arm':a,'assigned':n,'valid':len(valid),'missing':n-len(valid),
                'action_counts':{act:sum(v['action']==act for v in valid) for act in task(t)['actions']}}
            for field in ('actor_delta','total_delta','completed'):
                getter=lambda v,f=field:v['effects'][f]
                c[field+'_available_mean']=mean(getter)
                c[field+'_identification_bounds']=bounds(getter)
            recipients=len(possibilities[0]['effects']['third_party_deltas'])
            c['third_party_available_means']=[mean(lambda v,k=k:v['effects']['third_party_deltas'][k]) for k in range(recipients)]
            c['third_party_identification_bounds']=[bounds(lambda v,k=k:v['effects']['third_party_deltas'][k]) for k in range(recipients)]
            c['category_one_rate_bounds']={name:bounds(lambda v,s=s,k=k:v[s][k])
                for s,names in (('configuration_relative',RELATIVE),('fixed_standard',FIXED)) for k,name in enumerate(names)}
            c['headline_rate_bounds']={method:{label:bounds(lambda v,m=method,l=label:int(v['headlines'][m+'_possible']==[l]))
                for label in (('good','not_good') if method=='fixed' else ('good','neutral','not_good'))}
                for method in ('relative','fixed','net','weighted')}
            cells.append(c)
        def vector(arm,metric):
            return [None if lookup[i,t,arm] is None else
                (lookup[i,t,arm]['effects']['total_delta']-lo)/(hi-lo) if metric=='total_credits' else
                int(lookup[i,t,arm]['headlines']['fixed_headline']=='good') for i in range(1,n+1)]
        for left,right in (('E','U'),('V','U'),('G','U'),('E','V')):
            pair={}
            for metric in ('total_credits','fixed_good'):
                value=contrast([vector(left,metric),vector(right,metric)],[1,-1],SEED+2)
                scale=hi-lo if metric=='total_credits' else 1
                for k in ('estimate','complete_block_supplement'):
                    if value[k] is not None:value[k]*=scale
                for k in ('identification_interval','bootstrap_95_interval','hoeffding_95_interval'):
                    if value[k] is not None:value[k]=[x*scale for x in value[k]]
                pair[metric]=value
            contrasts[f'{t}/{left}-{right}']=pair
    return {'rows':out,'cells':cells,'contrasts':contrasts,'assigned':len(rows),
        'valid':sum(r['outcome'] is not None for r in out),'measurement':'finite deterministic operational rules',
        'scope':'exploratory individual pilot; no confirmation, human validation or universal moral truth'}


def collect(replay=False,root=LEDGER,folder=FOLDER,responder=network,test_data=None):
    root,folder=Path(root),Path(folder)
    if root==LEDGER and test_data is not None:raise BudgetStop('Test data on live ledger')
    release,pop,batch=test_data or tuple(read_checked(folder/f) for f in ('release.json','population.json','requests.json'))
    verify(release,root)
    if digest(pop)!=release['population_sha256'] or digest(batch)!=release['jobs_sha256'] or batch!=schedule(pop):
        raise BudgetStop('Changed or unreconstructible population/requests')
    manifest={'release_sha256':digest(release),'jobs_sha256':digest(batch)};save(folder/'execution_manifest.json',manifest)
    with Ledger(root,release) as ledger:
        if ledger.state['failed'] or ledger.state['pending']:raise BudgetStop('Unresolved dispatch')
        seen=set()
        def dispatch(j):
            r,called=ledger.dispatch(j,digest(manifest),responder,replay)
            if charge(r['raw'],j,False)!=r['accounted_nano']:raise BudgetStop('Charge replay differs')
            seen.add(digest(j['slot']));return r['parsed']
        raw=dispatch(batch[0])
        try:rv=review_value(json.dumps(json_value(raw)))
        except (ValueError,TypeError,KeyError,BudgetStop) as error:
            rv={'verdict':'invalid','blocking_issues':[str(error)],'limits':[]}
        print(json.dumps({'stage':'review','review':rv,'accounted_usd':ledger.state['recognition_nano']/1e9}),flush=True)
        result={'decision':'review_stop','participant_calls':0,'review':rv}
        if rv['verdict']=='accept':
            rows=[]
            for index,j in enumerate(batch[1:],1):
                rows.append({**j['cell'],'action':choice(dispatch(j),j['cell']['mapping'])})
                if index%16==0:print(json.dumps({'stage':'participants','completed':index,'assigned':len(batch)-1,
                    'accounted_usd':ledger.state['recognition_nano']/1e9}),flush=True)
            analysis=analyze(rows,pop['n_agents']);save(folder/'analysis.json',analysis)
            result.update(decision='pilot_complete',participant_calls=len(rows),valid=analysis['valid'])
        if set(ledger.state['reservations'])-set(release['historical_keys'])!=seen:raise BudgetStop('Unmanifested calls')
        result.update(study=STUDY,calls=len(seen),accounted_nano=ledger.state['recognition_nano'],
            provider_totals_nano=ledger.state['providers'],release_sha256=digest(release),human_validation=False,
            measurement='finite deterministic operational rules')
        save(folder/'results.json',result)
    return result


def archive():
    result=collect(True,responder=lambda _:(_ for _ in ()).throw(AssertionError('Replay network')))
    release=read_checked(FOLDER/'release.json')
    with Ledger(LEDGER,release) as ledger:
        archived_evidence(read_checked(PARENT/'CHECKPOINT.json'),LEDGER)
        members={p.relative_to(LEDGER).as_posix():sha(p) for p in LEDGER.rglob('*') if p.is_file() and p.suffix in ('.json','.jsonl')}
        path=ROOT/f'output/phase4_{STUDY}_20260914.zip'
        if not path.exists():
            with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED) as z:
                for name in sorted(members):z.write(LEDGER/name,name)
        with zipfile.ZipFile(path) as z:
            if z.testzip() or set(z.namelist())!=set(members) or any(hashlib.sha256(z.read(k)).hexdigest()!=v for k,v in members.items()):
                raise BudgetStop('Archive mismatch')
        check={'new_calls_during_verification':0,'historical_records_preserved':HISTORY,
            'total_paid_records':len(ledger.state['reservations']),'study_accounted_nano':result['accounted_nano'],
            'provider_totals_nano':ledger.state['providers'],'allocation_accounted_nano':sum(ledger.state['providers'].values()),
            'package_accounted_nano':POLICY['prior_package_nano']+sum(ledger.state['providers'].values()),
            'archive':path.relative_to(ROOT).as_posix(),'archive_members':len(members),'archive_sha256':sha(path),
            'results_sha256':digest(result),'off_device_backup_verified':False}
    save(FOLDER/'CHECKPOINT.json',check);return check


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=('prepare','run','verify'));parser.add_argument('--yes',action='store_true');args=parser.parse_args()
    if args.command=='prepare':
        r,p,b=prepare(True);print(json.dumps({'maximum_usd':r['recognition_cap_nano']/1e9,
            'cumulative_development_maximum_usd':(PRIOR+r['recognition_cap_nano'])/1e9,'calls':len(b),'participant_calls':96}))
    elif args.command=='run':
        if not args.yes:raise BudgetStop('Explicit launch flag required')
        print(json.dumps(collect()))
    else:print(json.dumps(archive()))
