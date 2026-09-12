"""Offline repeated-prompt stability audit; never makes API calls."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
import logging
import zipfile
from pathlib import Path

import pandas as pd
from scipy.stats import fisher_exact
import utils
from engine.parsing import parse_decision
from engine.validity_sweep import digest, parse_output
from run_validity_claude import save_new
from run_validity_original_expanded import holm
import run_validity_evidence_screen as base

ROOT=base.ROOT
BASE=ROOT/'experiments/phase1_5_encoding_validity'
OUT=BASE/'repeat_stability_20260912'
SOURCES=('option_c_20260909_restart','rotations_20260909_restart','gradients_20260909_final',
 'paraphrases_20260909_final','pd_endpoints_20260910','wording_factorial_20260910',
 'axis_instruction_20260911_assembled','evidence_screen_20260911','evidence_sensitivity_20260911',
 'repetition_factorial_20260911_continuation','repetition_retention_20260911','mor_curve_20260911',
 'profile_ablation_20260911','pd_interaction_20260911','joint_wording_20260911',
 'tool_delivery_20260911','original_expanded_20260911','ms_stanza_crossover_20260912')
LABELS={'S1':('A','B'),'S2':('FORMAL_REPORT','LOCAL_CORRECTION'),'S3':('ADOPT','WAIT')}


def prompt_key(messages,model,temperature,max_tokens,labels):
    # Seed deliberately excluded, separately audited. No whitespace/Unicode normalization.
    return digest({'messages':messages,'provider':'openai','model':model,'temperature':temperature,
                   'max_completion_tokens':max_tokens,'labels':list(labels)})


def exact_test(a,b):
    return float(fisher_exact([[b['first_count'],b['n']-b['first_count']],
                              [a['first_count'],a['n']-a['first_count']]],alternative='two-sided').pvalue)


def contrast(a,b):
    def cell(x):return {'adopt':x['first_count'],'n_expected':x['n'],'n_valid':x['n'],'rate':x['rate']}
    return base.contrast([(cell(b),1),(cell(a),-1)])


def summarize(records):
    grouped=defaultdict(list)
    for r in records:grouped[r['prompt_key'],r['run']].append(r)
    summaries=[]
    for (key,run),rows in grouped.items():
        ordered=sorted(rows,key=lambda r:(r['timestamp_utc'],r['api_call_id']))
        count=sum(r['first'] for r in rows)
        summaries.append({'prompt_key':key,'run':run,'problem':rows[0]['problem'],'n':len(rows),
            'first_count':count,'rate':count/len(rows),'wilson95':base.wilson(count,len(rows)),
            'start':ordered[0]['timestamp_utc'],'end':ordered[-1]['timestamp_utc'],
            'profile_hashes':sorted(set(r['profile_hash'] for r in rows)),
            'fingerprints':dict(Counter(str(r['fingerprint']) for r in rows)),
            'service_tiers':dict(Counter(str(r['service_tier']) for r in rows)),
            'prompt_token_counts':dict(Counter(str(r['prompt_tokens']) for r in rows)),
            'calls_with_cache_hits':sum((r['cached_tokens'] or 0)>0 for r in rows),
            'successful_records_with_multiple_attempts':sum(r.get('attempts',1)>1 for r in rows),
            'unique_response_texts':len(set(r['response_text_hash'] for r in rows)),
            'first_half_count':sum(r['first'] for r in ordered[:len(rows)//2]),
            'first_half_n':len(rows)//2,'second_half_count':sum(r['first'] for r in ordered[len(rows)//2:]),
            'second_half_n':len(rows)-len(rows)//2})
    by_key=defaultdict(list)
    for s in summaries:
        if s['n']>=20:by_key[s['prompt_key']].append(s)
    repeated={k:v for k,v in by_key.items() if len(v)>=2}
    pairs=[];within=[]
    for key,groups in sorted(repeated.items()):
        for a,b in combinations(sorted(groups,key=lambda s:(s['start'],s['run'])),2):
            pairs.append({'prompt_key':key,'problem':a['problem'],'earlier':a['run'],'later':b['run'],
                          'earlier_n':a['n'],'later_n':b['n'],'earlier_count':a['first_count'],
                          'later_count':b['first_count'],'effect':contrast(a,b),'p':exact_test(a,b)})
        for s in groups:
            a={'first_count':s['first_half_count'],'n':s['first_half_n']}
            b={'first_count':s['second_half_count'],'n':s['second_half_n']}
            within.append({'prompt_key':key,'run':s['run'],'first_half':a,'second_half':b,'p':exact_test(a,b)})
    for family in (pairs,within):
        for c,p in zip(family,holm([c['p'] for c in family])):
            c['holm_p']=p;c['difference_detected']=p<.05
    return summaries,repeated,pairs,within


def archived_records(root):
    info=json.loads((root/'local_backup.json').read_bytes());path=Path(info['path'])
    if sha256(path.read_bytes()).hexdigest()!=info['sha256']:raise ValueError('Archive checksum mismatch')
    with zipfile.ZipFile(path) as z:
        names=sorted(n for n in z.namelist() if n.startswith('records/') and n.endswith('.json'))
        disk_names=sorted(p.relative_to(root).as_posix() for p in (root/'records').rglob('*.json'))
        if names!=disk_names:raise ValueError('Archive/current filename inventory mismatch')
        if z.read('manifest.json')!=(root/'manifest.json').read_bytes():raise ValueError('Archived manifest differs')
        for name in names:yield root/name,z.read(name)


def main():
    OUT.mkdir(exist_ok=True);records=[];index=[];scope=[];ids=set();manifests={}
    for name in SOURCES:
        root=BASE/name;mp=root/'manifest.json';m=json.loads(mp.read_bytes());d=m['design']
        if digest(d)!=m['design_hash']:raise ValueError('Manifest hash mismatch: '+name)
        manifests[name]={'sha256':sha256(mp.read_bytes()).hexdigest(),'design_hash':m['design_hash'], 'archive':json.loads((root/'local_backup.json').read_bytes())['sha256']}
        counts=Counter();labels_by_problem={c['problem']:tuple(c['labels']) for c in d['cells']}
        for path,raw in archived_records(root):
            r=json.loads(raw);counts['files']+=1
            rh=r['record_hash'];without={k:v for k,v in r.items() if k!='record_hash'}
            if digest(without)!=rh:raise ValueError('Record hash mismatch: '+str(path))
            index.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha256(raw).hexdigest()})
            if name=='tool_delivery_20260911':
                if not r['record_key'].startswith('system/'):
                    counts['excluded_tool_protocol_calls']+=1;continue
                req=json.loads(r['wire_body'])
                if req!=r['request']:raise ValueError('Wire/request mismatch')
                if set(req)!= {'model','messages','temperature','max_completion_tokens','seed'}:raise ValueError('Unexpected request options')
                payload=r['response_payload'];messages=req['messages'];temp=req['temperature'];max_tokens=req['max_completion_tokens']
                seed=req['seed'];problem='S3';labels=LABELS[problem];profile=None
                text=payload['choices'][0]['message']['content'] if payload else None
                decision,status=parse_decision(text,labels)
                error=r['error'];model=(payload or {}).get('model');api_id=(payload or {}).get('id')
            else:
                payload=r['response_payload'];messages=r['request_messages'];temp=r.get('temperature',d['temperature'])
                max_tokens=r.get('max_tokens',d['max_tokens']);seed=r['seed'];problem=r['problem_id']
                labels=tuple(r.get('labels') or labels_by_problem[problem]);profile=r['agent_parameters']
                text=r['raw_response'];decision,status=parse_output(text,labels,r.get('arm'))
                if (decision,status)!=(r['parsed_decision'],r['parse_status']):
                    if not (r['parse_status']=='failed_api' and r.get('error_message') and text is None and r['parsed_decision'] is None):
                        raise ValueError('Parse mismatch: '+str(path))
                error=r.get('error_message') or r.get('terminal_failure') or r.get('model_version_mismatch')
                model=r['model_version'];api_id=r['api_call_id']
            if error or status!='ok' or model!=base.MODEL or not payload:
                counts['excluded_invalid_or_failure']+=1;continue
            if not isinstance(r.get('attempts'),int) or r['attempts']<1:raise ValueError('Missing attempt count')
            if r['attempts']>1:counts['successful_records_with_multiple_attempts']+=1
            if payload['choices'][0]['message']['content']!=text or payload['id']!=api_id or payload['model']!=model:
                raise ValueError('Payload/record mismatch')
            if api_id in ids:raise ValueError('Duplicate API ID in selected sources')
            if not api_id or api_id.startswith('mock'):raise ValueError('Nonreal response')
            ids.add(api_id);counts['valid_retained']+=1
            usage=payload.get('usage') or {};detail=usage.get('prompt_tokens_details') or {}
            records.append({'run':name,'record_key':r['record_key'],'prompt_key':prompt_key(messages,model,temp,max_tokens,labels),
                'profile_hash':digest(profile),'problem':problem,'first':decision==labels[0],
                'api_call_id':api_id,'seed':seed,'attempts':r['attempts'],'timestamp_utc':r['timestamp_utc'],
                'fingerprint':payload.get('system_fingerprint'),'service_tier':payload.get('service_tier'),
                'prompt_tokens':usage.get('prompt_tokens'),'cached_tokens':detail.get('cached_tokens'),
                'response_text_hash':digest(text)})
        scope.append({'run':name,**counts});print(name,dict(counts),flush=True)
    summaries,repeated,pairs,within=summarize(records)
    logging.basicConfig(level=logging.INFO)
    logger=logging.getLogger('repeat-stability')
    utils.log_dataframe_summary(pd.DataFrame(scope),'Every source: before/after record filtering',logger)
    utils.log_dataframe_summary(pd.DataFrame(summaries),f'All{len(records)} retained valid records ->all prompt/run summaries',logger)
    matched=[s for s in summaries if s['prompt_key'] in repeated and s['n']>=20]
    utils.log_dataframe_summary(pd.DataFrame(matched),f'All{len(summaries)} summaries ->{len(matched)} repeated prompt/run summaries with N>=20 in >=2 runs; others retained in full summary',logger)
    utils.log_dataframe_summary(pd.DataFrame(pairs),'All eligible between-run comparisons; one Holm family',logger)
    utils.log_dataframe_summary(pd.DataFrame(within),'All eligible first-half/second-half checks; separate Holm family',logger)
    seed_groups=defaultdict(list)
    for r in records:seed_groups[r['prompt_key'],r['seed']].append(r)
    same_seed=[{'prompt_key':key,'seed':seed,'n':len(rs),'runs':sorted(set(r['run'] for r in rs)),
                'first_count':sum(r['first'] for r in rs)} for (key,seed),rs in seed_groups.items() if len(rs)>1]
    anchors=[]
    src=json.loads((BASE/'original_expanded_20260911/manifest.json').read_bytes())['design']
    for c in src['cells']:
        if c['parameter'] in ('MoR','MS') and c['wording']=='canonical' and c['value'] in (.1,.9):
            key=prompt_key(c['messages'],src['model'],src['temperature'],src['max_tokens'],c['labels'])
            anchors.append({'parameter':c['parameter'],'value':c['value'],'prompt_key':key,
                            'runs':sorted([s for s in summaries if s['prompt_key']==key],key=lambda s:s['start'])})
    result={'scope':scope,'source_manifests':manifests,'valid_records':len(records),'unique_api_ids':len(ids),
        'all_prompt_run_summaries':summaries,'repeated_prompt_groups':len(repeated),
        'between_run_comparisons':pairs,'within_run_halves':within,'same_prompt_and_seed_repeats':same_seed,
        'anchors':anchors,'between_run_detections':sum(p['difference_detected'] for p in pairs),
        'within_run_detections':sum(p['difference_detected'] for p in within),
        'fingerprints':dict(Counter(str(r['fingerprint']) for r in records)),
        'seed':'Offline deterministic exact tests; no sampling seed, API calls or new simulation.',
        'limits':'Post-result exploratory audit. Prompt key includes exact messages, pinned model, temperature, max completion tokens and labels; excludes seed. Same prompt is not same complete request. Run/time/seed/transport are confounded. Two-sided Fisher assumes independent exchangeable binomial responses; corrected discrepancies flag violations, not causes. No records pooled to meet a phase gate.',
        'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    save_new(OUT/'results.json',result)
    save_new(OUT/'record_index.json',{'checksums':index,'normalized_metadata':records})
    print(json.dumps({'records':len(records),'repeated_groups':len(repeated),'pairs':len(pairs),
        'between_detections':result['between_run_detections'],'within_detections':result['within_run_detections'],
        'same_seed_repeat_groups':len(same_seed),'anchors':[{k:v for k,v in a.items() if k!='runs'}|{'counts':[(s['run'],s['first_count'],s['n']) for s in a['runs']]} for a in anchors]},indent=2))


if __name__=='__main__':main()
