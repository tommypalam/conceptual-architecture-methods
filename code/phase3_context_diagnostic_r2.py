"""Frozen canonical-only exploratory E/U diagnostic; no original Phase 3 pass."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import zipfile
import math

import numpy as np
from engine.population import Population
from phase3_budget import BudgetStop, POLICY, canonical, digest, read_checked, token_cost_nano
from phase3_recognition_run import ROOT, LEDGER, Ledger, network, charge, MODELS
from phase3_recognition_recovery import verify, sha, archived_evidence
from phase3_design_pilot import request, RATERS, JUDGE, PRICES
from phase3_design_pilot_r2 import review_value
from phase3_variant_round import save
from phase3_protocol_kernel import context_prompt
from phase3_canonical_stimuli import CONTEXTS, ultimatum_turn

FOLDER = ROOT / 'experiments/phase3_benchmarks/context_diagnostic_r2'
PARENT = ROOT / 'experiments/phase3_benchmarks/design_pilot_r2'
STUDY = 'context_diagnostic_r2'
N = 24
CAP = 4_300_000_000
SEEDS = {'population': 2026091313, 'schedule': 2026091314, 'analysis': 2026091315}
TASKS = [('proposer', None)] + [('responder', x) for x in (10,20,30,40,50)]


def system(profile, context, arm):
    text = context_prompt(profile, CONTEXTS['ultimatum'][context])
    suffix = '\n\nReturn a JSON object matching the requested schema.'
    if arm == 'E': return text + suffix
    if arm != 'U': raise ValueError('Unknown arm')
    start, end = text.index('# Your decision-making profile'), text.index('# Your normative context')
    text = text[:start] + text[end:]
    text = text.replace('it does not remove your individual characteristics or the facts of the task.',
                        'it does not remove the facts of the task.')
    start = text.index('# Your task')
    return text[:start] + ('# Your task\n\nYou will be presented with a decision. Apply the normative '
        'context as an operative input. Do not infer demographic identity, personality, ideology, '
        'or narrative backstory beyond what is specified. Do not refuse to decide. '
        'Answer in the exact format specified.') + suffix


def make_job(slot, model, body, system_text, bound, maximum):
    if len((body+system_text).encode()) + 1024 > bound:
        raise BudgetStop('Input bytes exceed reserved token bound')
    req = request(model, system_text, body, maximum, temperature=1)
    if model == RATERS[1]: req['response_format'] = {'type': 'json_object'}
    return {'slot': f'{STUDY}/{slot}', 'kind': 'probe', 'request': req,
        'input_token_bound': bound, 'reserved_nano': token_cost_nano(bound, maximum, *PRICES[model])}


def jobs(population):
    output = []
    for agent in population['agents']:
        block = []
        for context in (0,1):
            for arm in ('E','U'):
                for role, offer in TASKS:
                    task = 'proposer' if role == 'proposer' else f'r{offer}'
                    j = make_job(f'participant/{agent["agent_id"]}/{context}/{arm}/{task}', RATERS[1],
                        ultimatum_turn(role, offer), system(agent['parameters'], context, arm), 8192, 64)
                    j['cell'] = {'block': str(agent['agent_id']), 'context': context, 'arm': arm,
                                 'role': role, 'offer': offer}
                    block.append(j)
        random.Random(SEEDS['schedule']+agent['agent_id']).shuffle(block)
        output.extend(block)
    return output


def review_job(population):
    packet = {'protocol': (FOLDER/'PROTOCOL.md').read_text(encoding='utf-8'),
        'systems': {f'{c}/{a}': system(population['agents'][0]['parameters'], c, a)
                    for c in (0,1) for a in ('E','U')},
        'tasks': [ultimatum_turn(r,o) for r,o in TASKS],
        'population': {k:v for k,v in population.items() if k != 'agents'},
        'rendering': 'All profiles use exactly this template with their ten two-decimal values.'}
    return make_job('review/0', JUDGE, json.dumps(packet, ensure_ascii=False, sort_keys=True),
        'Independently review the attached exploratory study before collection. Assess whether its '
        'exact prompts, matched cells, context-only comparator, estimands, missingness and claims '
        'are coherent. This is explicitly canonical-only; no failed gate is to be waived. '
        'Return only JSON with verdict accept/revise/reject, blocking_issues list and limits list. '
        'Accept requires no blocking issues. Keep the entire response below 900 UTF-8 bytes '
        'and at most 100 words.', 32768, 1024)


def prepare(persist=False):
    parent, check = read_checked(PARENT/'release.json'), read_checked(PARENT/'CHECKPOINT.json')
    verify(parent); archived_evidence(check, LEDGER)
    with Ledger(LEDGER, parent) as ledger:
        if ledger.state['failed'] or ledger.state['pending'] or len(ledger.state['reservations']) != 660:
            raise BudgetStop('Unexpected parent evidence')
    population = Population.draw(N, seed=SEEDS['population']).to_dict()
    batch = [review_job(population)] + jobs(population)
    slots = {j['slot']: {'kind': j['kind'], 'model': j['request']['model'],
        'input_token_bound': j['input_token_bound'], 'reserved_nano': j['reserved_nano'],
        'max_output': j['request'].get('max_tokens', j['request'].get('max_completion_tokens')),
        'request_sha256': digest(j['request'])} for j in batch}
    if len(slots) != 577 or sum(j['reserved_nano'] for j in batch) > CAP:
        raise BudgetStop('Schedule size or bound mismatch')
    paths = [Path(__file__), FOLDER/'PROTOCOL.md', PARENT/'release.json', PARENT/'CHECKPOINT.json',
        ROOT/'code/phase3_context_diagnostic.py', ROOT/'experiments/phase3_benchmarks/context_diagnostic_r1/release.json',
        ROOT/'code/engine/population.py', ROOT/'code/utils.py', ROOT/'code/phase3_canonical_stimuli.py',
        ROOT/'code/phase3_protocol_kernel.py', ROOT/'prompts/system_prompt_template.md']
    release = {'id': STUDY, 'population_sha256': digest(population), 'jobs_sha256': digest(batch),
        'slots': slots, 'recognition_cap_nano': sum(j['reserved_nano'] for j in batch),
        'prior_screening_nano': 0, 'original_screening_cap_nano': CAP,
        'provider_caps_nano': parent['provider_caps_nano'], 'parent_checkpoint_sha256': digest(check),
        'historical_keys': sorted(p.stem for p in (LEDGER/'records').glob('*.json')),
        'preserved_files': {p.relative_to(LEDGER).as_posix(): sha(p) for p in LEDGER.rglob('*.json')},
        'failure_log_prefix_bytes': (LEDGER/'failures.jsonl').stat().st_size,
        'failure_log_prefix_sha256': sha(LEDGER/'failures.jsonl'),
        'source_sha256': {**parent['source_sha256'], **{p.relative_to(ROOT).as_posix(): sha(p) for p in paths}}}
    with Ledger(LEDGER, release): pass
    if persist:
        save(FOLDER/'population.json', population)
        save(FOLDER/'requests.json', batch)
        save(FOLDER/'release.json', release)
    return release, population, batch


def action(text, cell):
    def unique(pairs):
        if len({k for k,v in pairs}) != len(pairs): raise ValueError('Duplicate keys')
        return dict(pairs)
    try:
        value = json.loads(text, object_pairs_hook=unique)
        if not isinstance(value, dict): raise ValueError('Not object')
        if cell['role'] == 'proposer':
            if set(value) != {'offer_to_other'} or type(value['offer_to_other']) is not int or not 0 <= value['offer_to_other'] <= 100:
                raise ValueError('Invalid offer')
            return value['offer_to_other']/100
        if set(value) != {'action'} or value['action'] not in ('accept','reject'): raise ValueError('Invalid action')
        return int(value['action'] == 'reject')
    except (ValueError, TypeError): return None


def contrast(vectors, coefficients, seed):
    n = len(vectors[0]); limit = sum(abs(c) for c in coefficients)
    rows = list(zip(*vectors))
    complete = [sum(c*x for c,x in zip(coefficients,row)) for row in rows if all(x is not None for x in row)]
    bounds = [sum(sum(c*(x if x is not None else (0 if (c>0) == (side==0) else 1))
                            for c,x in zip(coefficients,row)) for row in rows)/n for side in (0,1)]
    result = {'assigned_blocks': n, 'complete_blocks': len(complete), 'missing_blocks': n-len(complete),
        'identification_interval': bounds, 'estimate': None,
        'complete_block_supplement': float(np.mean(complete)) if complete else None,
        'bootstrap_95_interval': None, 'bootstrap_degenerate': None, 'hoeffding_95_interval': None,
        'analysis_seed': seed, 'resamples': 9999}
    if len(complete) == n:
        a = np.array(complete); mean = float(a.mean()); rng = np.random.default_rng(seed)
        boot = a[rng.integers(0,n,size=(9999,n))].mean(axis=1)
        lower, upper = sum(min(0,c) for c in coefficients), sum(max(0,c) for c in coefficients)
        radius = limit*math.sqrt(math.log(40)/(2*n))
        result.update(estimate=mean, bootstrap_95_interval=np.quantile(boot,[.025,.975]).tolist(),
            bootstrap_degenerate=bool(np.ptp(a)==0),
            hoeffding_95_interval=[max(lower, mean-radius),min(upper,mean+radius)])
    return result


def analyze(rows, n):
    expected = {(str(i),c,a,r,o) for i in range(1,n+1) for c in (0,1) for a in ('E','U') for r,o in TASKS}
    keys = [(r['block'],r['context'],r['arm'],r['role'],r['offer']) for r in rows]
    if len(keys) != len(set(keys)) or set(keys) != expected: raise BudgetStop('Duplicate, extra or missing assigned cells')
    values = dict(zip(keys, [r['value'] for r in rows]))
    def vector(c,a,role='responder',offer=20): return [values[(str(i),c,a,role,offer)] for i in range(1,n+1)]
    cells = []
    for c in (0,1):
        for a in ('E','U'):
            for role, offer in TASKS:
                v = vector(c,a,role,offer); valid = [x for x in v if x is not None]
                cells.append({'context': c, 'arm': a, 'role': role, 'offer': offer, 'assigned': n,
                    'valid': len(valid), 'missing': n-len(valid), 'mean_available': float(np.mean(valid)) if valid else None,
                    'mean_identification_interval': [sum(valid)/n,(sum(valid)+n-len(valid))/n]})
    primary = {
        'E_context': contrast([vector(0,'E'),vector(1,'E')],[1,-1],SEEDS['analysis']),
        'U_context': contrast([vector(0,'U'),vector(1,'U')],[1,-1],SEEDS['analysis']+1),
        'interaction': contrast([vector(0,'E'),vector(1,'E'),vector(0,'U'),vector(1,'U')],[1,-1,-1,1],SEEDS['analysis']+2)}
    secondary = {f'E_minus_U_context_{c}': contrast([vector(c,'E'),vector(c,'U')],[1,-1],SEEDS['analysis']+3+c) for c in (0,1)}
    monotonic = []
    for c in (0,1):
        for a in ('E','U'):
            grids = [[values[(str(i),c,a,'responder',o)] for o in (10,20,30,40,50)] for i in range(1,n+1)]
            valid = [g for g in grids if None not in g]
            monotonic.append({'context': c, 'arm': a, 'complete_grids': len(valid),
                'nonmonotone': sum(any(x<y for x,y in zip(g,g[1:])) for g in valid), 'missing_grids': n-len(valid)})
    return {'study': STUDY, 'stage': 'exploratory_canonical_only', 'assigned_responses': len(rows),
        'invalid_actions': sum(r['value'] is None for r in rows), 'primary': primary, 'secondary': secondary,
        'cells': cells, 'monotonicity': monotonic, 'phase3_pass': None, 'formal_gate': 'unmet_unchanged',
        'human_equivalence': None, 'moral_quality': None, 'full_population_released': False}


def collect(replay=False, *, root=LEDGER, folder=FOLDER, responder=network, test_data=None):
    root,folder = Path(root),Path(folder)
    if root == LEDGER and test_data is not None: raise BudgetStop('Test release on live ledger')
    release,population,batch = test_data if test_data else tuple(read_checked(folder/f) for f in ('release.json','population.json','requests.json'))
    verify(release,root)
    if digest(population) != release['population_sha256'] or digest(batch) != release['jobs_sha256']:
        raise BudgetStop('Population or schedule changed')
    if batch != [review_job(population)] + jobs(population): raise BudgetStop('Frozen requests differ from reconstruction')
    manifest = {'release_sha256': digest(release), 'jobs_sha256': digest(batch)}
    save(folder/'execution_manifest.json',manifest)
    with Ledger(root,release) as ledger:
        if ledger.state['failed'] or ledger.state['pending']: raise BudgetStop('Unresolved dispatch')
        seen = set()
        def dispatch(j):
            r,called = ledger.dispatch(j,digest(manifest),responder,replay)
            if charge(r['raw'],j,False) != r['accounted_nano']: raise BudgetStop('Cost replay mismatch')
            seen.add(digest(j['slot']))
            return r['parsed']
        review = review_value(dispatch(batch[0]))
        print(json.dumps({'review':review,'accounted_usd':ledger.state['recognition_nano']/1e9}),flush=True)
        rows = []
        if review['verdict'] == 'accept':
            for index,j in enumerate(batch[1:],1):
                value = action(dispatch(j),j['cell'])
                rows.append({**j['cell'],'value':value})
                if index%24 == 0: print(json.dumps({'completed':index,'assigned':len(batch)-1,
                    'invalid':sum(r['value'] is None for r in rows),'accounted_usd':ledger.state['recognition_nano']/1e9}),flush=True)
            result = analyze(rows,population['n_agents'])
            save(folder/'scored_rows.json',rows)
        else:
            result = {'study':STUDY,'decision':'review_stop','assigned_responses':len(batch)-1,
                'participant_calls':0,'phase3_pass':None,'full_population_released':False}
        if set(ledger.state['reservations'])-set(release['historical_keys']) != seen:
            raise BudgetStop('Unmanifested dispatch')
        result.update(review=review,calls=len(seen),accounted_nano=ledger.state['recognition_nano'],
            provider_totals_nano=ledger.state['providers'],release_sha256=digest(release))
        save(folder/'results.json',result)
    return result


def archive():
    result = collect(True,responder=lambda _: (_ for _ in ()).throw(AssertionError('Network during verification')))
    release = read_checked(FOLDER/'release.json')
    with Ledger(LEDGER,release) as ledger:
        archived_evidence(read_checked(PARENT/'CHECKPOINT.json'),LEDGER)
        members = {p.relative_to(LEDGER).as_posix():sha(p) for p in LEDGER.rglob('*') if p.is_file() and p.suffix in ('.json','.jsonl')}
        path = ROOT/f'output/phase3_{STUDY}_20260913.zip'
        if not path.exists():
            with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED) as z:
                for name in sorted(members): z.write(LEDGER/name,name)
        with zipfile.ZipFile(path) as z:
            if z.testzip() or set(z.namelist()) != set(members) or any(hashlib.sha256(z.read(n)).hexdigest()!=s for n,s in members.items()):
                raise BudgetStop('Archive mismatch')
        check = {'results_sha256':digest(result),'new_calls_during_verification':0,'historical_records_preserved':660,
            'total_paid_records':len(ledger.state['reservations']),'diagnostic_accounted_nano':result['accounted_nano'],
            'provider_totals_nano':ledger.state['providers'],'phase3_accounted_nano':sum(ledger.state['providers'].values()),
            'package_accounted_nano':POLICY['prior_package_nano']+sum(ledger.state['providers'].values()),
            'archive':path.relative_to(ROOT).as_posix(),'archive_members':len(members),'archive_sha256':sha(path),
            'off_device_backup_verified':False}
    save(FOLDER/'CHECKPOINT.json',check)
    return check


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('command',choices=('prepare','run','verify')); parser.add_argument('--yes',action='store_true'); args=parser.parse_args()
    if args.command == 'prepare':
        r,p,b=prepare(True); print(json.dumps({'release_sha256':digest(r),'maximum_usd':r['recognition_cap_nano']/1e9,'participant_calls':len(b)-1}))
    elif args.command == 'run':
        if not args.yes: raise BudgetStop('Explicit execution flag required')
        print(json.dumps(collect()))
    else: print(json.dumps(archive()))
