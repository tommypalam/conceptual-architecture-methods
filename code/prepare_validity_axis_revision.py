"""Prepare one theory-preserving axis-instruction candidate; never dispatch API calls."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pandas as pd
import utils
from engine.prompt_assembly import load_template
from engine.validity_sweep import digest,freeze
from engine.validity_variants import load_reviewed_paraphrases,variant_prompt
from run_validity_claude import save_new

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'experiments/phase1_5_encoding_validity'
INSTRUCTION=(
    'For numerical parameter values, read the two endpoint descriptions of each parameter together as one axis. '
    'Its number locates your position along that axis: lower values are closer '
    'to the stated 0-end meaning, and higher values are closer to the stated '
    '1-end meaning. Intermediate values represent intermediate positions; '
    'retain their degree rather than substituting an endpoint or a category. '
    'Interpret the number within its own parameter, and apply all ten parameter '
    'positions jointly to the decision in the stated normative context.'
)


def revise(system):
    marker='# Your normative context'
    if system.count(marker)!=1 or INSTRUCTION in system:
        raise ValueError('Expected one unmodified context marker')
    return system.replace(marker,'# Reading the parameter values\n\n'+INSTRUCTION+'\n\n'+marker)


def prepare(root):
    source=json.loads((BASE/'option_c_20260909_restart/manifest.json').read_text(encoding='utf-8'))
    rotations=json.loads((BASE/'rotations_20260909_restart/manifest.json').read_text(encoding='utf-8'))
    paraphrases=json.loads((BASE/'paraphrases_20260909_final/manifest.json').read_text(encoding='utf-8'))
    for m in (source,rotations,paraphrases):
        if digest(m['design'])!=m['design_hash']: raise ValueError('Historical manifest integrity failure')
    templates={'canonical':load_template(),**load_reviewed_paraphrases(
        BASE/'claude_paraphrases_20260909_theory_r5/paraphrases_approved.json')}
    cells=[]
    for wording,template in templates.items():
        system,provenance=variant_prompt('PD',.8,'hybrid',template=template)
        old=next(c for c in (rotations if wording=='canonical' else paraphrases)['design']['cells']
            if c['parameter']=='PD' and c['problem']=='S3' and c['variant']==('hybrid' if wording=='canonical' else wording))
        assert system==old['messages'][0]['content']
        for arm in ('baseline','revision'):
            c=deepcopy(old)
            c.update(stage='equivalence',wording=wording,arm=arm,variant=f'{arm}_{wording}',n=800)
            if arm=='revision': c['messages'][0]['content']=revise(system)
            cells.append(c)
    for old in source['design']['cells']:
        if old['parameter']!='PD' or old['arm']!='full_harness': continue
        for arm in ('baseline','revision'):
            c=deepcopy(old)
            c.update(stage='sweep',wording='canonical',arm=arm,variant=arm,n=50)
            if arm=='revision': c['messages'][0]['content']=revise(c['messages'][0]['content'])
            cells.append(c)
    precision=BASE/'offline_diagnosis_20260909/precision_extension.json'
    power=json.loads(precision.read_text(encoding='utf-8'))
    save_new(root/'equivalence_precision_reference.json',{
        'source_sha256':hashlib.sha256(precision.read_bytes()).hexdigest(),'source':str(precision.relative_to(ROOT)),
        'interpretation':'Previously simulated equal-rate four-formulation TOST precision, not new empirical data or predicted repair success.',
        'result':power})
    d={'phase':'phase1_5_encoding_validity','experiment':'axis_instruction_PD_development_pilot',
        'configuration':'neutral','model':source['design']['model'],'provider':'openai',
        'temperature':source['design']['temperature'],'max_tokens':source['design']['max_tokens'],
        'seed':20260913,'planned_calls':sum(c['n'] for c in cells),'cells':cells,
        'revision_text':INSTRUCTION,'single_candidate':True,
        'source_design_hashes':[m['design_hash'] for m in (source,rotations,paraphrases)],
        'template_hashes':{f'{arm}_{name}':digest(revise(t) if arm=='revision' else t)
            for name,t in templates.items() for arm in ('baseline','revision')},
        'analysis':{
            'scope':'Selected-PD development pilot; no whole-battery pass or theory amendment',
            'equivalence':'All six constrained-score TOST pairs, .10 margin, alpha .05, separately for each arm',
            'N_equivalence_per_arm_formulation':800,'N_sweep_per_arm_problem_value':50,
            'parse_floor':.98,'invalids':'Preserved; primary valid-only TOST plus exhaustive binary completions of invalid decisions for eligible equivalence cells. Local progression requires both.',
            'sweep':'Reuse original logistic, h, monotonicity and frozen direction rules. Only PD/S1 has a prespecified sign.',
            'saturation':'Flag if every formulation in an arm has ADOPT rate <=.05 or every rate >=.95; equivalence alone is insufficient',
            'progression':'Only consider broader revalidation if revision establishes local equivalence, meets PD/S1 sweep criterion and is not saturated. This is a local screening rule, not a replacement phase gate.',
            'control':'Report fresh baseline and revised results together; failure-versus-success classifications alone are not a formal between-arm improvement test',
            'limitations':'Instruction applies to all ten traits; only PD is manipulated here. Full audit/representation/all-parameter validation remains necessary.'},
        'collection':{'order':'Seed-shuffle matched baseline/revision request pairs; randomize within each pair',
            'seeds':'Distinct by stage, arm, wording, problem, value and repetition',
            'stopping':'Fixed planned N; terminal API/model error or pilot spending ceiling stops dispatch; retain incomplete records',
            'spending_ceiling_usd':12,'expected_cost_usd':9,'remaining_additional_budget_estimate_usd':48.6856535},
        'source_hashes':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in (
            'code/prepare_validity_axis_revision.py','code/run_validity_axis_revision.py',
            'code/engine/validity_analysis.py','code/engine/validity_equivalence.py',
            'code/engine/validity_sweep.py','code/engine/llm_client.py','code/engine/parsing.py',
            'code/engine/seeding.py','code/run_validity_restart_followups.py')},
        'execution_status':'NOT_LAUNCHED; exact instruction review required'}
    m=freeze(root/'manifest.json',d)
    save_new(root/'review_pending.json',{'approved':False,'reviewer':None,'proposal_hash':m['design_hash'],
        'instruction_hash':digest(INSTRUCTION),'template_hashes':d['template_hashes'],
        'exact_messages_hash':digest([c['messages'] for c in cells]),
        'scope':'New shared axis-reading instruction; existing definitions, endpoints, values, contexts and dilemma text unchanged'})
    lines=['# Candidate revision: exact instruction review','',
        'This candidate adds only the following block immediately before the normative-context section in each revised system message. Baseline messages are byte-identical to previous frozen designs.','',
        '```text','# Reading the parameter values','',INSTRUCTION,'```','',
        'This is one proposed shared-scaffold revision, not a new independently generated endpoint paraphrase. The three existing Claude-generated, human-approved endpoint paraphrases remain unchanged.','',
        'No formula converts a value into an action probability or a numerical utility weight. No new priority ordering, categorical cut-point or correct dilemma answer is introduced.','',
        '## Exact revised templates','']
    for name,template in templates.items():
        lines += [f'### {name}',f'Template hash: `{d["template_hashes"]["revision_"+name]}`','',
            '```text',revise(template),'```','']
    path=root/'HUMAN_REVIEW.md';content='\n'.join(lines).rstrip()+'\n'
    if path.exists() and path.read_text(encoding='utf-8')!=content: raise ValueError('Changed review')
    path.write_text(content,encoding='utf-8')
    import logging
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame([{k:c[k] for k in ('stage','arm','wording','problem','value','n')} for c in cells]),
        'Prepared candidate/control cells; rendered messages retained in manifest',logging.getLogger('axis-preparation'))
    print(f'Prepared {len(cells)} cells, {d["planned_calls"]} proposed calls; no API access.')
    return m


if __name__=='__main__':
    prepare(BASE/'axis_instruction_20260910')
