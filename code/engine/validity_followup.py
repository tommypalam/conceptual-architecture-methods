"""Execution of later prompt-comparison tests, isolated from the live Option-C run."""
from __future__ import annotations

import asyncio
import hashlib
import itertools
import json
import random
from pathlib import Path

import utils
from .delivery import SystemRoleDelivery
from .llm_client import Message
from .parsing import parse_decision, parse_reasoning
from .phase0b_runner import PROBLEMS
from .prompt_assembly import build_simple_user_turn
from .questions import PHASE0B_QUESTIONS, load_dilemma_body
from .seeding import derive_seed
from .validity_sweep import digest, ValiditySink, verify_record
from .validity_variants import variant_prompt
from .validity_analysis import VALUES, DIRECTIONS, logistic, wilson
from .validity_equivalence import tost


def load_source(root, *, require_complete=False):
    root=Path(root)
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    if digest(manifest['design'])!=manifest['design_hash']:
        raise ValueError('Source manifest integrity failure')
    if require_complete:
        records=list(ValiditySink(root/'records').read_all())
        if len(records)!=manifest['design']['planned_calls']:
            raise ValueError('Wait for complete source experiment before dependent API work')
        if any(r.get('error_message') or r.get('model_version_mismatch') for r in records):
            raise ValueError('Source contains terminal failures; review before dependent work')
    return manifest


def comparison_design(source_root, experiment, *, n=50, seed=20260604, paraphrases=None, provider='mock'):
    source=load_source(source_root)
    original=source['design']
    if original['params']!=list(utils.PARAM_NAMES) or set(original['problems'])!={'S1','S2','S3'}:
        raise ValueError('Expected the complete original ten-parameter/three-problem design')
    if experiment=='rotations':
        variants=['hybrid','numeric_only','verbal_only']; values=(.8,)
    elif experiment=='gradients':
        variants=['numeric_only','verbal_only']; values=VALUES
    elif experiment=='paraphrases' and paraphrases and len(paraphrases)==3:
        variants=list(paraphrases); values=(.8,)
    else:
        raise ValueError('Unknown experiment or missing reviewed paraphrases')
    if n<=0:
        raise ValueError('N must be positive')
    cells=[]
    for param,value,problem,variant in itertools.product(utils.PARAM_NAMES,values,PROBLEMS[:3],variants):
        is_paraphrase=variant.startswith('paraphrase_')
        system,provenance=variant_prompt(param,value,'hybrid' if is_paraphrase else variant,
                                         template=paraphrases[variant] if is_paraphrase else None)
        dilemma=load_dilemma_body(problem.question_file,PHASE0B_QUESTIONS)
        # Compare a canonical probe against the frozen source, so future edits
        # cannot silently make imported hybrid sweep baselines non-comparable.
        probe,_=variant_prompt(param,.5,'hybrid')
        original_cell=next(c for c in original['cells'] if c['arm']=='full_harness'
                           and c['parameter']==param and c['value']==.5 and c['problem']==problem.short_id)
        if probe!=original_cell['messages'][0]['content']:
            raise ValueError('Canonical profile no longer matches source sweep')
        if hashlib.sha256(dilemma.encode()).hexdigest()!=original_cell['dilemma_sha256']:
            raise ValueError('Dilemma differs from source sweep')
        user=build_simple_user_turn(dilemma,problem.labels)
        messages=[{'role':m.role,'content':m.content} for m in SystemRoleDelivery().messages(system,user)]
        cells.append({'variant':variant,'parameter':param,'value':value,'problem':problem.short_id,
                      'labels':list(problem.labels),'profile':provenance['parameter_values'],'messages':messages})
    names=('validity_followup.py','validity_variants.py','validity_equivalence.py','llm_client.py','parsing.py')
    hashes={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in names}
    return {'schema_version':'1.0','phase':'phase1_5_encoding_validity','experiment':experiment,
            'source_design_hash':source['design_hash'],'source_root':str(Path(source_root).resolve()),
            'model':original['model'] if provider=='openai' else 'mock-model','provider':provider,
            'n':n,'seed':seed,'temperature':original['temperature'],'max_tokens':original['max_tokens'],
            'source_hashes':hashes,'cells':cells,'variants':variants,'values':list(values),
            'planned_calls':len(cells)*n,'configuration':'neutral','delivery':'full_harness',
            'analysis':{'rotation_value':.8,'paraphrase_margin':.10,'alpha':.05,
                        'paraphrase_comparisons':'all six pairs among canonical and three paraphrases',
                        'verbal_mapping':'six equal-width intervals; six names in spec, not four quartiles',
                        'gradient_magnitude':'absolute fitted logit slope; numeric/hybrid ratio >=0.5',
                        'gradient_reuse':'exact-model full-harness hybrid sweeps from frozen source only'},
            'stopping':'fixed N; fail-stop after current batch on terminal API error/model mismatch'}


async def execute_comparison(manifest, *, client, sink, concurrency=5, limit=None):
    d=manifest['design']
    if digest(d)!=manifest['design_hash']:
        raise ValueError('Manifest integrity failure')
    if not 1<=concurrency<=5:
        raise ValueError('Concurrency must be 1..5')
    if limit is not None and limit<=0:
        raise ValueError('Limit must be positive')
    for name,expected_hash in d['source_hashes'].items():
        if hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()!=expected_hash:
            raise ValueError(f'Frozen source changed: {name}')
    if d['provider']!='mock':
        source=load_source(d['source_root'],require_complete=True)
        if source['design_hash']!=d['source_design_hash']:
            raise ValueError('Wrong source design')
    jobs=[]
    for cell in d['cells']:
        for k in range(1,d['n']+1):
            key=f"{cell['variant']}/{cell['parameter']}/{cell['problem']}/{cell['value']:.1f}/call_{k:04d}"
            jobs.append((key,cell,k))
    random.Random(d['seed']).shuffle(jobs)
    expected={j[0] for j in jobs}
    existing=list(sink.read_all())
    for row in existing:
        verify_record(row)
        if row['design_hash']!=manifest['design_hash'] or row['record_key'] not in expected:
            raise ValueError('Existing record belongs to another experiment')
        if row.get('error_message') or row.get('model_version_mismatch'):
            raise ValueError('Preserved failure requires review and a new designation')
    pending=[j for j in jobs if not sink.exists(j[0])]
    if limit is not None:
        pending=pending[:limit]
    async def one(job):
        key,c,k=job
        seed=derive_seed(d['seed'],d['experiment'],c['parameter'],c['problem'],c['value'],k)
        result=await client.complete([Message(**m) for m in c['messages']],
                                     temperature=d['temperature'],max_tokens=d['max_tokens'],seed=seed)
        decision,status=parse_decision(result.text,tuple(c['labels']))
        expected_model=d['model']+'-mock' if d['provider']=='mock' else d['model']
        mismatch=result.ok and result.model_version!=expected_model
        row={'schema_version':'1.0','phase':d['phase'],'experiment':d['experiment'],
             'design_hash':manifest['design_hash'],'record_key':key,'variant':c['variant'],
             'swept_parameter':c['parameter'],'sweep_value':c['value'],'problem_id':c['problem'],
             'labels':c['labels'],'agent_parameters':c['profile'],'call_index':k,'seed':seed,
             'timestamp_utc':result.timestamp_utc,'model_version':result.model_version,
             'model_version_mismatch':bool(mismatch),'provider':result.provider,
             'api_call_id':result.api_call_id,'attempts':result.attempts,
             'request_messages':result.request_messages,'response_payload':result.raw_response,
             'raw_response':result.text,'parsed_decision':decision,'parsed_reasoning':parse_reasoning(result.text),
             'parse_status':'failed_api' if result.error else 'model_mismatch' if mismatch else status,
             'error_message':result.error}
        row['record_hash']=digest(row)
        sink.write(key,row)
        if result.error or mismatch:
            sink.write_failure({'record_key':key,'error':result.error,'model_mismatch':bool(mismatch)})
        return not (result.error or mismatch)
    for start in range(0,len(pending),concurrency):
        outcomes=await asyncio.gather(*(one(job) for job in pending[start:start+concurrency]))
        count=len(existing)+min(start+concurrency,len(pending))
        if start==0 or count%50==0 or start+concurrency>=len(pending):
            print(f'{d["experiment"]}: {count}/{d["planned_calls"]} records',flush=True)
        if not all(outcomes):
            raise RuntimeError('Dispatch stopped; terminal failure preserved')


def summarize_cells(manifest,records):
    d=manifest['design']; seen=set(); grouped={}
    expected={(c['variant'],c['parameter'],c['problem'],c['value']) for c in d['cells']}
    for row in records:
        verify_record(row)
        group=(row['variant'],row['swept_parameter'],row['problem_id'],row['sweep_value'])
        key=group+(row['call_index'],)
        if row['design_hash']!=manifest['design_hash'] or key in seen or group not in expected or not 1<=key[-1]<=d['n']:
            raise ValueError('Mixed, duplicate or out-of-design comparison record')
        seen.add(key); grouped.setdefault(group,[]).append(row)
    cells=[]
    for c in d['cells']:
        data=grouped.get((c['variant'],c['parameter'],c['problem'],c['value']),[])
        valid=[r for r in data if r['parse_status']=='ok' and r['parsed_decision'] in c['labels']]
        k=sum(r['parsed_decision']==c['labels'][0] for r in valid)
        cells.append({'variant':c['variant'],'parameter':c['parameter'],'problem':c['problem'],
                      'value':c['value'],'n_expected':d['n'],'n_recorded':len(data),'n_valid':len(valid),
                      'n_missing':d['n']-len(data),'n_invalid':len(data)-len(valid),'opt0_count':k,
                      'rate':k/len(valid) if valid else None,'ci95':wilson(k,len(valid))})
    return {'design_hash':manifest['design_hash'],'experiment':d['experiment'],'provider':d['provider'],
            'n_expected':d['planned_calls'],'n_records':len(records),'cells':cells,
            'status':'Descriptive comparison; full battery verdict requires all subtests'}


def paraphrase_equivalence(cells):
    by={}
    for c in cells:
        if c['value']!=.8:
            continue
        key=(c['variant'],c['parameter'],c['problem'])
        if key in by:
            raise ValueError('Duplicate equivalence cell')
        by[key]=c
    variants=('hybrid','paraphrase_1','paraphrase_2','paraphrase_3')
    rows=[]
    for param,problem in itertools.product(utils.PARAM_NAMES,('S1','S2','S3')):
        selected=[by.get((v,param,problem)) for v in variants]
        complete=all(c and c['n_recorded']==c['n_expected'] and c['n_valid']/c['n_expected']>=.98 for c in selected)
        pairs=[]
        if complete:
            for a,b in itertools.combinations(selected,2):
                pairs.append({'a':a['variant'],'b':b['variant'],
                              **tost(a['opt0_count'],a['n_valid'],b['opt0_count'],b['n_valid'])})
        rows.append({'parameter':param,'problem':problem,'complete':bool(complete),
                     'all_pairs_equivalent':bool(complete and all(p['equivalent'] for p in pairs)),
                     'pairs':pairs})
    count=sum(r['all_pairs_equivalent'] for r in rows)
    return {'cells':rows,'n_equivalent':count,'n_expected':30,
            'criterion_met':bool(all(r['complete'] for r in rows) and count>=24),
            'note':'Failure to establish equivalence is not proof of a meaningful difference.'}


def gradient_comparison(new_cells,source_sweeps):
    rows=[]
    for source in source_sweeps:
        if source['arm']!='full_harness':
            continue
        for variant in ('numeric_only','verbal_only'):
            cells=sorted([c for c in new_cells if c['variant']==variant and c['parameter']==source['parameter']
                          and c['problem']==source['problem']],key=lambda c:c['value'])
            complete=len(cells)==5 and all(c['n_recorded']==c['n_expected'] and c['n_valid']/c['n_expected']>=.98 for c in cells)
            fit=logistic(cells)
            baseline=source['fit'].get('slope')
            ratio=abs(fit['slope']/baseline) if fit['status']=='ok' and baseline and source['fit']['status']=='ok' else None
            predicted=DIRECTIONS.get((source['parameter'],source['problem']))
            direction=bool(predicted and fit['status']=='ok' and predicted*fit['slope']>0)
            assessable=bool(complete and source['criterion_met'])
            rows.append({'variant':variant,'parameter':source['parameter'],'problem':source['problem'],
                         'complete':complete,'source_sweep_criterion_met':source['criterion_met'],
                         'fit':fit,'absolute_logit_slope_ratio':ratio,'direction_matches':direction,
                         'criterion_met':bool(assessable and ratio is not None and ratio>=.5 and direction),
                         'assessment':'eligible' if assessable else 'not_assessable'})
    return rows
