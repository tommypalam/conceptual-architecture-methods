"""Frozen, budgeted finite-action moral pilot with measurement gate and replay."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import zipfile

from engine.population import Population
from phase3_budget import BudgetStop, POLICY, digest, read_checked, token_cost_nano
from phase3_recognition_run import ROOT, LEDGER, Ledger, network, charge, MODELS
from phase3_recognition_recovery import verify, sha, archived_evidence
from phase3_design_pilot import request, RATERS, JUDGE, PRICES, review_value
from phase3_variant_round import save
from phase3_protocol_kernel import context_prompt, AXES
from phase3_representation_diagnostic import profile_parts, numeric_rows, prose_rows, words, contrast
from phase4_moral_schema import RELATIVE, FIXED, validate_judgment, judge_envelope
from phase4_consequence_tasks import TASK_IDS, task, transition, mapping, prompt, card, check_cards

FOLDER = ROOT/'experiments/phase4_coding/consequence_pilot_r1'
PARENT = ROOT/'experiments/phase3_benchmarks/transfer_pilot_r1'
STUDY = 'consequence_pilot_r1'
MANUAL = 'consequence-pilot-r1'
N = 6
CAP = 4_000_000_000
ARMS = ('E','V','U','G')
SEED = 2026091350
JUDGES = (JUDGE,RATERS[1])


def system(profile,arm):
    if arm not in ARMS: raise ValueError('Unknown arm')
    prefix, block, suffix = profile_parts(context_prompt(profile,dict.fromkeys(AXES,'NEUTRAL')))
    suffix = suffix[:suffix.index('# Your task')] + (
        '# Your task\nUse the supplied information to select the action to execute. '
        'Do not infer demographic identities or additional facts. '
        'Return only the requested JSON object.\n')
    if arm == 'V':
        rows = numeric_rows(block)
        block = '# Your decision-making profile\n\n' + '\n\n'.join(
            f'For {name}, your position is {words(value)} percent of the way from "{low}" toward "{high}".'
            for name,value,low,high in rows)+'\n\n'
        if prose_rows(block)!=rows: raise BudgetStop('E/V translation mismatch')
    elif arm == 'U': block = ''
    elif arm == 'G': block = (
        '# Ethical guidance\n\nConsider the effects on everyone affected. Avoid causing harm, '
        'deception, coercion and unfair treatment. Act honestly and respect consent and equivalent '
        'claims. Consider opportunities to help, including when they carry a personal cost. '
        'When these considerations conflict, weigh the competing reasons using the stated facts.\n\n')
    return prefix+block+suffix


def job(slot,model,system_text,body,maximum,temperature=0):
    bound = len((system_text+body).encode('utf-8'))+1024
    req = request(model,system_text,body,maximum,temperature)
    if model==RATERS[1]: req['response_format']={'type':'json_object'}
    return {'slot':f'{STUDY}/{slot}','kind':'probe','request':req,'input_token_bound':bound,
            'reserved_nano':token_cost_nano(bound,maximum,*PRICES[model])}


def json_value(text):
    def unique(pairs):
        if len({k for k,v in pairs})!=len(pairs): raise ValueError('Duplicate JSON key')
        return dict(pairs)
    text=text.strip()
    if text.startswith('```json\n') and text.endswith('```'): text=text[8:-3].strip()
    return json.loads(text,object_pairs_hook=unique)


def review_job(pop):
    packet={'protocol':(FOLDER/'PROTOCOL.md').read_text(encoding='utf-8'),
            'manual':(FOLDER/'MANUAL.md').read_text(encoding='utf-8'),
            'tasks':{t:prompt(t,1) for t in TASK_IDS},
            'systems':{a:system(pop['agents'][0]['parameters'],a) for a in ARMS}}
    return job('review',JUDGE,
        'Independently review this prospective exploratory moral-choice pilot and scoped coding manual. '
        'Check agency, deterministic effects, causal comparator, equal-credit stipulation, duties, '
        'mandate/fairness/coercion boundaries, matched controls, blinding, measurement stopping, '
        'independence limits and inferential scope. Flag blocking ambiguities, not merely small sample '
        'or absence of human raters already disclosed. Do not reward a design for likely positive results. '
        'Return JSON only with verdict accept/revise/reject, blocking_issues list, limits list; '
        'accept requires no blocking issues. Keep the entire JSON under 350 words.',
        json.dumps(packet,ensure_ascii=False,sort_keys=True),2048)


def coding_jobs():
    cards=[card(t,a) for t in TASK_IDS for a in task(t)['actions']]+[c for c,expected in check_cards()]
    batch=[]
    manual=(FOLDER/'MANUAL.md').read_text(encoding='utf-8')
    schema={'item_id':'COPY_PACKET_ID','manual_version':MANUAL,
            'configuration_relative':[0]*8,'fixed_standard':[1]*4,
            'evidence':{c:{'source_ids':['COPY_RELEVANT_FACT_ID'],'reason':'brief evidence-based reason',
                           'unknown_reason':None} for c in RELATIVE+FIXED}}
    # Placeholder values specify output types, not a worked judgment; state this explicitly.
    for i,model in enumerate(JUDGES):
        intro=('Apply the supplied moral manual to this one executed action. Work independently. '
               'Use only packet facts; never infer an experimental condition. Give every category a '
               'brief reason with existing fact IDs. Unknowns require a reason. Return JSON only, '
               'under 900 words. Schema values below are placeholders, not expected labels.\n'
               if i==0 else
               'You are a separate action coder. Determine each category from this packet and the '
               'fixed manual without assuming other judgments. Cite actual fact IDs for all entries '
               'and explain unknowns. Do not infer the participant profile or study arm. JSON only, '
               'under 900 words. The example is a type schema; its vector values are not answers.\n')
        for c in cards:
            j=job(f'coding/{i}/{c["item_id"]}',model,intro+manual+'\nJSON schema:\n'+json.dumps(schema),
                  json.dumps(c,ensure_ascii=False,sort_keys=True),2048)
            j.update(item_id=c['item_id'],judge=i,source_ids=sorted(c['facts']))
            batch.append(j)
    random.Random(SEED+2).shuffle(batch)
    return batch


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
        random.Random(SEED+1+agent['agent_id']).shuffle(block); batch.extend(block)
    return batch


def schedule(pop): return [review_job(pop)]+coding_jobs()+participant_jobs(pop)


def prepare(persist=False):
    parent,check=read_checked(PARENT/'release.json'),read_checked(PARENT/'CHECKPOINT.json')
    verify(parent); archived_evidence(check,LEDGER)
    with Ledger(LEDGER,parent) as ledger:
        if ledger.state['failed'] or ledger.state['pending'] or len(ledger.state['reservations'])!=2263:
            raise BudgetStop('Unexpected parent evidence')
        providers=dict(ledger.state['providers'])
    pop=Population.draw(N,seed=SEED).to_dict(); batch=schedule(pop)
    slots={j['slot']:{'kind':'probe','model':j['request']['model'],'input_token_bound':j['input_token_bound'],
        'reserved_nano':j['reserved_nano'],'max_output':j['request'].get('max_tokens',j['request'].get('max_completion_tokens')),
        'request_sha256':digest(j['request'])} for j in batch}
    bound=sum(j['reserved_nano'] for j in batch)
    for j in batch: providers[MODELS[j['request']['model']]]+=j['reserved_nano']
    if len(slots)!=129 or bound>CAP or providers['anthropic']>11_000_000_000 or providers['openai']>20_000_000_000:
        raise BudgetStop(f'Full schedule exceeds size/budget/reserve: {len(slots)} calls, {bound/1e9:.6f}')
    paths=[Path(__file__),ROOT/'code/phase4_consequence_tasks.py',ROOT/'code/phase4_moral_schema.py',
           FOLDER/'PROTOCOL.md',FOLDER/'MANUAL.md']
    release={'id':STUDY,'population_sha256':digest(pop),'jobs_sha256':digest(batch),'slots':slots,
        'recognition_cap_nano':bound,'prior_screening_nano':0,'original_screening_cap_nano':CAP,
        'provider_caps_nano':parent['provider_caps_nano'],'parent_checkpoint_sha256':digest(check),
        'historical_keys':sorted(p.stem for p in (LEDGER/'records').glob('*.json')),
        'preserved_files':{p.relative_to(LEDGER).as_posix():sha(p) for p in LEDGER.rglob('*.json')},
        'failure_log_prefix_bytes':(LEDGER/'failures.jsonl').stat().st_size,
        'failure_log_prefix_sha256':sha(LEDGER/'failures.jsonl'),
        'source_sha256':{**parent['source_sha256'],**{p.relative_to(ROOT).as_posix():sha(p) for p in paths}}}
    with Ledger(LEDGER,release): pass
    if persist:
        save(FOLDER/'population.json',pop);save(FOLDER/'requests.json',batch);save(FOLDER/'release.json',release)
    return release,pop,batch


def measurement_check(ratings):
    expected_ids={card(t,a)['item_id'] for t in TASK_IDS for a in task(t)['actions']}
    expected_ids.update(c['item_id'] for c,e in check_cards())
    if set(ratings)!={(i,k) for i in range(2) for k in expected_ids}:
        raise BudgetStop('Incomplete or unexpected measurement grid')
    failures=[]
    for (judge,item),r in ratings.items():
        if r.get('error'): failures.append({'judge':judge,'item':item,'failure':'schema','detail':r['error']})
    for i in range(2):
        checks=check_cards()
        for t in TASK_IDS:
            for a,info in task(t)['actions'].items():
                effect=transition(t,a)
                checks.append((card(t,a),{'configuration_relative':{2:int(effect['total_delta']<0)},
                    'fixed_standard':{0:int(all(x>=0 for x in effect['third_party_deltas'])),1:int(not info['deceptive'])}}))
        for c,expectations in checks:
            record=ratings[i,c['item_id']]
            if record.get('error'): continue
            for schema,indices in expectations.items():
                for index,want in indices.items():
                    got=record['judgment'][schema][index]
                    if got!=want: failures.append({'judge':i,'item':c['item_id'],'schema':schema,
                        'index':index,'expected':want,'observed':got,'failure':'diagnostic'})
    return {'passed':not failures,'failures':failures,'rating_calls':len(ratings),
            'human_validation':False,'normative_validity_established':False}


def choice(text,labels):
    try:
        value=json_value(text)
        if not isinstance(value,dict) or set(value)!={'choice'} or value['choice'] not in labels: return None
        return labels[value['choice']]
    except (ValueError,TypeError): return None


def analyze(rows,ratings,n):
    expected={(i,t,a) for i in range(1,n+1) for t in TASK_IDS for a in ARMS}
    if len(rows)!=len(expected) or {(r['block'],r['task'],r['arm']) for r in rows}!=expected:
        raise BudgetStop('Missing, duplicate or unexpected participant cells')
    out=[];lookup={}
    for row in rows:
        if row['action'] is None: value={**row,'effects':None,'judges':None,'envelope':None}
        else:
            effect=transition(row['task'],row['action']);item=card(row['task'],row['action'])['item_id']
            judges=[ratings[i,item]['summary'] for i in range(2)]
            value={**row,'effects':effect,'judges':judges,'envelope':judge_envelope(*judges)}
        out.append(value);lookup[row['block'],row['task'],row['arm']]=value
    cells=[]; contrasts={}
    for t in TASK_IDS:
        lo=min(transition(t,a)['total_delta'] for a in task(t)['actions'])
        hi=max(transition(t,a)['total_delta'] for a in task(t)['actions'])
        def credit_vector(arm):
            return [None if lookup[i,t,arm]['effects'] is None else
                    (lookup[i,t,arm]['effects']['total_delta']-lo)/(hi-lo) for i in range(1,n+1)]
        for a in ARMS:
            selected=[lookup[i,t,a] for i in range(1,n+1)]
            moral_bounds={}
            for judge in (0,1,'union'):
                ranges=[]
                for r in selected:
                    if r['effects'] is None: ranges.append([0,1]);continue
                    if judge=='union': ranges.append(r['envelope']['fixed']['good_rate_contribution_bounds'])
                    else:
                        labels=r['judges'][judge]['fixed_possible'];ranges.append([int(labels==['good']),int('good' in labels)])
                moral_bounds[str(judge)]=[sum(b[k] for b in ranges)/n for k in (0,1)]
            cell={'task':t,'arm':a,'assigned':n,'valid':sum(r['action'] is not None for r in selected),
                  'action_counts':{act:sum(r['action']==act for r in selected) for act in task(t)['actions']},
                  'fixed_good_rate_bounds':moral_bounds}
            for field in ('actor_delta','total_delta','completed'):
                values=[r['effects'][field] for r in selected if r['effects'] is not None]
                cell[field+'_available_mean']=sum(values)/len(values) if values else None
            cell['third_party_available_means']=[sum(r['effects']['third_party_deltas'][j] for r in selected if r['effects'])/cell['valid']
                if cell['valid'] else None for j in range(len(transition(t,next(iter(task(t)['actions'])))['third_party_deltas']))]
            cell['total_delta_identification_bounds']=[sum(r['effects']['total_delta'] if r['effects'] else b for r in selected)/n for b in (lo,hi)]
            moral_rates={}
            for judge in range(2):
                by_category={};by_headline={}
                for schema,names in (('configuration_relative',RELATIVE),('fixed_standard',FIXED)):
                    for index,name in enumerate(names):
                        values=[None if r['action'] is None else ratings[judge,card(t,r['action'])['item_id']]['judgment'][schema][index] for r in selected]
                        by_category[name]={'known':sum(v is not None for v in values),
                            'one_rate_bounds':[sum(v==1 for v in values)/n,sum(v==1 or v is None for v in values)/n]}
                for method in ('relative','fixed','net','weighted'):
                    labels=[(['good','not_good'] if method=='fixed' else ['good','neutral','not_good'])
                            if r['action'] is None else r['judges'][judge][method+'_possible'] for r in selected]
                    by_headline[method]={label:[sum(p==[label] for p in labels)/n,sum(label in p for p in labels)/n]
                        for label in ('good','neutral','not_good') if method!='fixed' or label!='neutral'}
                moral_rates[str(judge)]={'categories':by_category,'headlines':by_headline}
            cell['moral_rates']=moral_rates
            cells.append(cell)
        for left,right in (('E','U'),('V','U'),('G','U'),('E','V')):
            c=contrast([credit_vector(left),credit_vector(right)],[1,-1],SEED+3)
            # Convert unit-scaled paired differences and intervals back into credits.
            for key in ('estimate','complete_block_supplement'):
                if c[key] is not None:c[key]*=hi-lo
            for key in ('identification_interval','bootstrap_95_interval','hoeffding_95_interval'):
                if c[key] is not None:c[key]=[x*(hi-lo) for x in c[key]]
            l=next(x for x in cells if x['task']==t and x['arm']==left)
            r=next(x for x in cells if x['task']==t and x['arm']==right)
            c['fixed_good_difference_bounds']={j:[l['fixed_good_rate_bounds'][j][0]-r['fixed_good_rate_bounds'][j][1],
                l['fixed_good_rate_bounds'][j][1]-r['fixed_good_rate_bounds'][j][0]] for j in ('0','1','union')}
            contrasts[f'{t}/{left}-{right}']=c
    agreement={}
    for schema,names in (('configuration_relative',RELATIVE),('fixed_standard',FIXED)):
        for k,name in enumerate(names):
            pairs=[(ratings[0,card(t,a)['item_id']]['judgment'][schema][k],ratings[1,card(t,a)['item_id']]['judgment'][schema][k])
                   for t in TASK_IDS for a in task(t)['actions']]
            agreement[name]={'unique_production_cards':12,'both_known':sum(x is not None and y is not None for x,y in pairs),
                'known_agree':sum(x==y and x is not None for x,y in pairs),'either_unknown':sum(x is None or y is None for x,y in pairs),
                'judge_one_count':[sum(p[i]==1 for p in pairs) for i in range(2)]}
    return {'rows':out,'cells':cells,'contrasts':contrasts,'agreement':agreement,
            'assigned':len(rows),'valid':sum(r['action'] is not None for r in rows),
            'scope':'exploratory individual workflow pilot; not confirmation or human validation'}


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
        rv=review_value(json.dumps(json_value(dispatch(batch[0]))))
        print(json.dumps({'stage':'review','review':rv,'accounted_usd':ledger.state['recognition_nano']/1e9}),flush=True)
        result={'decision':'review_stop','participant_calls':0,'review':rv}
        if rv['verdict']=='accept':
            ratings={}
            for index,j in enumerate(batch[1:33],1):
                raw=dispatch(j)
                try:
                    judgment=json_value(raw)
                    summary=validate_judgment(judgment,j['item_id'],j['source_ids'],MANUAL)
                    record={'judge':j['judge'],'item_id':j['item_id'],'judgment':judgment,'summary':summary}
                except (ValueError,TypeError,KeyError) as error:
                    record={'judge':j['judge'],'item_id':j['item_id'],'error':str(error)}
                ratings[j['judge'],j['item_id']]=record
                if index%8==0:print(json.dumps({'stage':'coding','completed':index,'assigned':32,'accounted_usd':ledger.state['recognition_nano']/1e9}),flush=True)
            measurement=measurement_check(ratings)
            save(folder/'ratings.json',list(ratings.values()));save(folder/'measurement_checks.json',measurement)
            result.update(decision='measurement_stop',measurement=measurement)
            print(json.dumps({'stage':'measurement_gate',**measurement}),flush=True)
            if measurement['passed']:
                rows=[]
                for index,j in enumerate(batch[33:],1):
                    rows.append({**j['cell'],'action':choice(dispatch(j),j['cell']['mapping'])})
                    if index%16==0:print(json.dumps({'stage':'participants','completed':index,'assigned':len(batch)-33,'accounted_usd':ledger.state['recognition_nano']/1e9}),flush=True)
                analysis=analyze(rows,ratings,pop['n_agents']);save(folder/'analysis.json',analysis)
                result.update(decision='pilot_complete',participant_calls=len(rows),valid=analysis['valid'])
        if set(ledger.state['reservations'])-set(release['historical_keys'])!=seen:raise BudgetStop('Unmanifested calls')
        result.update(study=STUDY,calls=len(seen),accounted_nano=ledger.state['recognition_nano'],
            provider_totals_nano=ledger.state['providers'],release_sha256=digest(release),human_validation=False)
        save(folder/'results.json',result)
    return result


def archive():
    result=collect(True,responder=lambda _:(_ for _ in ()).throw(AssertionError('Replay network')))
    release=read_checked(FOLDER/'release.json')
    with Ledger(LEDGER,release) as ledger:
        archived_evidence(read_checked(PARENT/'CHECKPOINT.json'),LEDGER)
        members={p.relative_to(LEDGER).as_posix():sha(p) for p in LEDGER.rglob('*') if p.is_file() and p.suffix in ('.json','.jsonl')}
        path=ROOT/f'output/phase4_{STUDY}_20260913.zip'
        if not path.exists():
            with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED) as z:
                for name in sorted(members):z.write(LEDGER/name,name)
        with zipfile.ZipFile(path) as z:
            if z.testzip() or set(z.namelist())!=set(members) or any(hashlib.sha256(z.read(k)).hexdigest()!=v for k,v in members.items()):
                raise BudgetStop('Archive mismatch')
        check={'new_calls_during_verification':0,'historical_records_preserved':2263,
            'total_paid_records':len(ledger.state['reservations']),'study_accounted_nano':result['accounted_nano'],
            'provider_totals_nano':ledger.state['providers'],'allocation_accounted_nano':sum(ledger.state['providers'].values()),
            'package_accounted_nano':POLICY['prior_package_nano']+sum(ledger.state['providers'].values()),
            'archive':path.relative_to(ROOT).as_posix(),'archive_members':len(members),'archive_sha256':sha(path),
            'results_sha256':digest(result),'off_device_backup_verified':False}
    save(FOLDER/'CHECKPOINT.json',check);return check


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=('prepare','run','verify'));parser.add_argument('--yes',action='store_true');args=parser.parse_args()
    if args.command=='prepare':
        r,p,b=prepare(True);print(json.dumps({'maximum_usd':r['recognition_cap_nano']/1e9,'calls':len(b),'participant_calls':96}))
    elif args.command=='run':
        if not args.yes:raise BudgetStop('Explicit launch flag required')
        print(json.dumps(collect()))
    else:print(json.dumps(archive()))
