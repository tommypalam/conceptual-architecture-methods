"""Prospective PD process/outcome pilot; frozen evidence is never edited."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import random
import zipfile

from engine.population import Population
from phase3_budget import BudgetStop, POLICY, canonical, digest, read_checked, token_cost_nano
from phase3_recognition_run import ROOT, LEDGER, Ledger, network, charge, MODELS
from phase3_recognition_recovery import verify, sha, archived_evidence
from phase3_design_pilot import request, RATERS, JUDGE, PRICES
from phase3_design_pilot_r2 import review_value
from phase3_variant_round import save
from phase3_protocol_kernel import context_prompt, AXES
from phase3_representation_diagnostic import profile_parts, numeric_rows, prose_rows, words, contrast

FOLDER = ROOT / 'experiments/phase3_benchmarks/transfer_pilot_r1'
PARENT = ROOT / 'experiments/phase3_benchmarks/representation_diagnostic_r1'
STUDY = 'transfer_pilot_r1'
N = 8
CAP = 2_000_000_000
SEEDS = {'population': 2026091340, 'schedule': 2026091341, 'analysis': 2026091342}
NEUTRAL = dict.fromkeys(AXES, 'NEUTRAL')
ARMS = ('E', 'V', 'S', 'U')
DOMAINS = ('workshop', 'maintenance')
LEVELS = (0.1, 0.9)


def system(background, level, arm):
    if arm not in ARMS or (arm != 'U' and level not in LEVELS) or (arm == 'U' and level is not None):
        raise ValueError('Invalid arm/PD level')
    profile = dict(background)
    if level is not None:
        profile['PD'] = level
    original = context_prompt(profile, NEUTRAL)
    prefix, block, suffix = profile_parts(original)
    # Common task instruction does not refer to absent coordinates in S/U.
    suffix = suffix[:suffix.index('# Your task')] + (
        '# Your task\nUse the supplied information to make the requested decision. '
        'Do not infer a demographic identity or additional facts. '
        'Return only the requested JSON object.\n')
    if arm == 'E':
        selected = block
    elif arm == 'V':
        selected = '# Your decision-making profile\n\n'
        selected += '\n\n'.join(
            f'For {name}, your position is {words(value)} percent of the way from "{low}" toward "{high}".'
            for name, value, low, high in numeric_rows(block)) + '\n\n'
        if prose_rows(selected) != numeric_rows(block):
            raise BudgetStop('Prose translation lost information')
    elif arm == 'S':
        row = next(r for r in numeric_rows(block) if r[0] == 'Procedural Dependence')
        name, value, low, high = row
        selected = ('# Your decision-making profile\n\n'
            f'For {name}, your position is {words(value)} percent of the way from "{low}" toward "{high}".\n\n')
    else:
        selected = ''
    return prefix + selected + suffix


def task(domain, procedure, outcome, support_first=True):
    if domain not in DOMAINS or procedure not in (0, 1) or outcome not in (0, 1):
        raise ValueError('Unknown scenario cell')
    if domain == 'workshop':
        start = ('A shared workshop had one equipment grant for one of four eligible projects. '
                 'Before applications, it announced that all four qualified equally and that a witnessed draw '
                 'would select the recipient. Each applicant had access to the same information and a chance '
                 'to correct its eligibility record. ')
        process = (
            'The administrator followed the announced draw and funded its selected project.' if procedure else
            'After the draw, the administrator secretly replaced its selected project with another eligible '
            'project run by a personal associate. The replacement was not permitted by the announced rules.')
        benefit = ('After delivery, an independent audit found that the funded project caused a net '
                   f'{"gain" if outcome else "loss"} of 40 workshop sessions available to residents, '
                   'relative to not making the grant, after all operating demands were counted. '
                   'The grant amount was fixed; no applicant had a prior entitlement to it.')
    else:
        start = ('A maintenance cooperative could repair one of four equally eligible public facilities. '
                 'It announced in advance that a witnessed draw would select one, with equal entry rights '
                 'and a chance for each facility to correct its records. ')
        process = (
            'The coordinator used the announced draw and repaired its selected facility.' if procedure else
            'After the draw, the coordinator secretly substituted another eligible facility managed by a '
            'personal associate. The substitution violated the announced selection rules.')
        benefit = ('After the repair, an independent audit found that it caused a net '
                   f'{"gain" if outcome else "loss"} of 40 hours of public access, relative to no repair, '
                   'after all closures and maintenance demands were counted. '
                   'The repair cost was fixed; none of the facilities had a prior entitlement to selection.')
    common = ('The public-access effect was unpredictable at selection time. Nobody then knew which '
              'project or facility would gain or lose access. The audit is complete and certain now. '
              'There were no other benefits, losses, future effects or personal consequences for you. '
              'No official or peer is asking you to approve or oppose the decision. '
              'You are an independent observer giving an overall evaluation of the completed selection; '
              'your answer cannot change its consequences. ')
    options = ('A = support the decision overall; B = oppose the decision overall.' if support_first else
               'A = oppose the decision overall; B = support the decision overall.')
    return '\n\n'.join((start, process, benefit, common, options,
                        'Return JSON only: {"choice":"A"} or {"choice":"B"}.'))


def make_job(slot, model, system_text, body, maximum):
    # Decoded UTF-8 bytes plus message framing, not an optimistic tokenizer estimate.
    bound = len((system_text + body).encode('utf-8')) + 1024
    req = request(model, system_text, body, maximum, temperature=1)
    if model == RATERS[1]:
        req['response_format'] = {'type': 'json_object'}
    return {'slot': f'{STUDY}/{slot}', 'kind': 'probe', 'request': req,
            'input_token_bound': bound,
            'reserved_nano': token_cost_nano(bound, maximum, *PRICES[model])}


def jobs(population):
    batch = []
    for agent in population['agents']:
        block = []
        for d, domain in enumerate(DOMAINS):
            for p in (0, 1):
                for o in (0, 1):
                    # Same mapping across arms/PD within a cell, exactly balanced by block.
                    first = (agent['agent_id'] + d + p + o) % 2 == 0
                    for arm in ARMS:
                        for level in ((None,) if arm == 'U' else LEVELS):
                            tag = 'none' if level is None else str(level)
                            j = make_job(f'participant/{agent["agent_id"]}/{domain}/{p}/{o}/{arm}/{tag}',
                                RATERS[1], system(agent['parameters'], level, arm), task(domain,p,o,first), 64)
                            j['cell'] = {'block': str(agent['agent_id']), 'domain': domain,
                                         'procedure': p, 'outcome': o, 'arm': arm, 'pd': level,
                                         'support_label': 'A' if first else 'B'}
                            block.append(j)
        random.Random(SEEDS['schedule'] + agent['agent_id']).shuffle(block)
        batch.extend(block)
    return batch


def fidelity(population):
    for a in population['agents']:
        for level in LEVELS:
            e = system(a['parameters'], level, 'E')
            v = system(a['parameters'], level, 'V')
            pe, be, se = profile_parts(e)
            pv, bv, sv = profile_parts(v)
            if pe != pv or se != sv or numeric_rows(be) != prose_rows(bv):
                raise BudgetStop('E/V mismatch')
            rows = numeric_rows(be)
            if next(x[1] for x in rows if x[0] == 'Procedural Dependence') != int(level*100):
                raise BudgetStop('PD endpoint mismatch')
        low = numeric_rows(profile_parts(system(a['parameters'],.1,'E'))[1])
        high = numeric_rows(profile_parts(system(a['parameters'],.9,'E'))[1])
        if [x for x in low if x[0] != 'Procedural Dependence'] != [x for x in high if x[0] != 'Procedural Dependence']:
            raise BudgetStop('Non-PD coordinate changed')
    return {'backgrounds': len(population['agents']), 'non_pd_coordinates_fixed': True,
            'E_V_information_identical': True, 'marginals_R_unchanged': True,
            'PD_interventions_are_not_natural_population_draws': True}


def review_job(population):
    packet = {'protocol': (FOLDER/'PROTOCOL.md').read_text(encoding='utf-8'),
              'systems': {f'{arm}/{pd}':system(population['agents'][0]['parameters'],pd,arm)
                          for arm in ARMS for pd in ((None,) if arm == 'U' else LEVELS)},
              'tasks': {f'{d}/{p}/{o}':task(d,p,o) for d in DOMAINS for p in (0,1) for o in (0,1)},
              'fidelity': fidelity(population)}
    return make_job('review/0', JUDGE,
        'Review the supplied prospective exploratory design independently. Check factorial coherence, '
        'plausible process/outcome separation, whether outcome-dominance is adequately operationalized, '
        'label mappings, matched controls and inference limitations. Flag blocking ambiguities. '
        'This is an overall evaluation task, not consequential behavior or moral scoring. '
        'Do not accept merely because it could show an effect. Return only JSON with verdict '
        'accept/revise/reject, blocking_issues list, limits list. Keep the entire JSON under 150 words.',
        json.dumps(packet, ensure_ascii=False, sort_keys=True), 1024)


def prepare(persist=False):
    parent, check = read_checked(PARENT/'release.json'), read_checked(PARENT/'CHECKPOINT.json')
    verify(parent)
    archived_evidence(check, LEDGER)
    with Ledger(LEDGER, parent) as ledger:
        if ledger.state['failed'] or ledger.state['pending'] or len(ledger.state['reservations']) != 1814:
            raise BudgetStop('Unexpected starting evidence')
        providers = dict(ledger.state['providers'])
    population = Population.draw(N,seed=SEEDS['population']).to_dict()
    fidelity(population)
    batch = [review_job(population)] + jobs(population)
    slots = {j['slot']:{'kind':j['kind'],'model':j['request']['model'],
             'input_token_bound':j['input_token_bound'],'reserved_nano':j['reserved_nano'],
             'max_output':j['request'].get('max_tokens',j['request'].get('max_completion_tokens')),
             'request_sha256':digest(j['request'])} for j in batch}
    bound = sum(j['reserved_nano'] for j in batch)
    for j in batch:
        providers[MODELS[j['request']['model']]] += j['reserved_nano']
    if len(slots) != 1 + N*56 or bound > CAP:
        raise BudgetStop(f'Size or $2 bound exceeded: {len(slots)} calls, {bound/1e9:.6f} USD')
    if providers['anthropic'] > 11_000_000_000 or providers['openai'] > 20_000_000_000:
        raise BudgetStop('Moral capstone reserve would be consumed')
    paths = [Path(__file__),FOLDER/'PROTOCOL.md',FOLDER/'REVIEW.md',
             ROOT/'code/phase3_representation_diagnostic.py',ROOT/'code/phase3_design_pilot.py',
             ROOT/'code/phase3_design_pilot_r2.py',ROOT/'code/engine/population.py',ROOT/'code/utils.py',
             ROOT/'code/phase3_protocol_kernel.py',ROOT/'prompts/system_prompt_template.md']
    release = {'id':STUDY,'population_sha256':digest(population),'jobs_sha256':digest(batch),
        'slots':slots,'recognition_cap_nano':bound,'prior_screening_nano':0,
        'original_screening_cap_nano':CAP,'provider_caps_nano':parent['provider_caps_nano'],
        'parent_checkpoint_sha256':digest(check),
        'historical_keys':sorted(p.stem for p in (LEDGER/'records').glob('*.json')),
        'preserved_files':{p.relative_to(LEDGER).as_posix():sha(p) for p in LEDGER.rglob('*.json')},
        'failure_log_prefix_bytes':(LEDGER/'failures.jsonl').stat().st_size,
        'failure_log_prefix_sha256':sha(LEDGER/'failures.jsonl'),
        'source_sha256':{**parent['source_sha256'], **{p.relative_to(ROOT).as_posix():sha(p) for p in paths}}}
    with Ledger(LEDGER,release): pass
    if persist:
        save(FOLDER/'population.json',population); save(FOLDER/'requests.json',batch); save(FOLDER/'release.json',release)
    return release,population,batch


def action(text, cell):
    def unique(pairs):
        if len({k for k,v in pairs}) != len(pairs): raise ValueError('Duplicate JSON key')
        return dict(pairs)
    try:
        value = json.loads(text, object_pairs_hook=unique)
        if not isinstance(value,dict) or set(value) != {'choice'} or value['choice'] not in ('A','B'):
            return None
        return int(value['choice'] == cell['support_label'])
    except (ValueError,TypeError):
        return None


def analyze(rows,n):
    def key(r): return (r['block'],r['domain'],r['procedure'],r['outcome'],r['arm'],r['pd'])
    expected = {(str(i),d,p,o,a,l) for i in range(1,n+1) for d in DOMAINS for p in (0,1) for o in (0,1)
                for a in ARMS for l in ((None,) if a == 'U' else LEVELS)}
    if len(rows)!=len(expected) or {key(r) for r in rows}!=expected:
        raise BudgetStop('Missing, duplicate or unexpected scored cells')
    lookup = {key(r):r['value'] for r in rows}
    def vector(d,p,o,a,l): return [lookup[str(i),d,p,o,a,l] for i in range(1,n+1)]
    cells = []
    for d in DOMAINS:
        for p in (0,1):
            for o in (0,1):
                for a in ARMS:
                    for l in ((None,) if a=='U' else LEVELS):
                        v=vector(d,p,o,a,l)
                        cells.append({'domain':d,'procedure':p,'outcome':o,'arm':a,'pd':l,
                                      'support':sum(x==1 for x in v),'valid':sum(x is not None for x in v),'assigned':n})
    tradeoffs = {}
    for d in DOMAINS:
        for a in ('E','V','S'):
            vectors=[vector(d,1,0,a,.9),vector(d,0,1,a,.9),vector(d,1,0,a,.1),vector(d,0,1,a,.1)]
            tradeoffs[f'{d}/{a}']=contrast(vectors,[1,-1,-1,1],SEEDS['analysis'])
    return {'study':STUDY,'assigned_responses':len(rows),'valid_responses':sum(r['value'] is not None for r in rows),
            'cells':cells,'tradeoffs':tradeoffs,'independent_domains':2,'blocks':n,
            'analysis_status':'exploratory descriptive; no significance or confirmation claim',
            'phase3_pass':None,'moral_scores_assigned':False}


def collect(replay=False,root=LEDGER,folder=FOLDER,responder=network,test_data=None):
    root,folder=Path(root),Path(folder)
    if root==LEDGER and test_data is not None: raise BudgetStop('Test data on real ledger')
    release,pop,batch=test_data or tuple(read_checked(folder/f) for f in ('release.json','population.json','requests.json'))
    verify(release,root)
    fidelity(pop)
    if digest(pop)!=release['population_sha256'] or digest(batch)!=release['jobs_sha256']:
        raise BudgetStop('Changed population or requests')
    if batch != [review_job(pop)] + jobs(pop): raise BudgetStop('Reconstructed schedule differs')
    manifest={'release_sha256':digest(release),'jobs_sha256':digest(batch)}
    save(folder/'execution_manifest.json',manifest)
    with Ledger(root,release) as ledger:
        if ledger.state['failed'] or ledger.state['pending']: raise BudgetStop('Unresolved dispatch')
        seen=set()
        def dispatch(j):
            r,called=ledger.dispatch(j,digest(manifest),responder,replay)
            if charge(r['raw'],j,False)!=r['accounted_nano']: raise BudgetStop('Cost replay mismatch')
            seen.add(digest(j['slot']))
            return r['parsed']
        review=review_value(dispatch(batch[0]))
        print(json.dumps({'review':review,'accounted_usd':ledger.state['recognition_nano']/1e9}),flush=True)
        if review['verdict']=='accept':
            rows=[]
            for i,j in enumerate(batch[1:],1):
                rows.append({**j['cell'],'value':action(dispatch(j),j['cell'])})
                if i%56==0: print(json.dumps({'completed':i,'assigned':len(batch)-1,'accounted_usd':ledger.state['recognition_nano']/1e9}),flush=True)
            result=analyze(rows,pop['n_agents']); save(folder/'scored_rows.json',rows)
        else:
            result={'study':STUDY,'decision':'review_stop','participant_calls':0,'phase3_pass':None}
        if set(ledger.state['reservations'])-set(release['historical_keys'])!=seen:
            raise BudgetStop('Unmanifested dispatch')
        result.update(review=review,calls=len(seen),accounted_nano=ledger.state['recognition_nano'],
                      provider_totals_nano=ledger.state['providers'],release_sha256=digest(release))
        save(folder/'results.json',result)
    return result


def archive():
    result=collect(True,responder=lambda _:(_ for _ in ()).throw(AssertionError('Replay network')))
    release=read_checked(FOLDER/'release.json')
    with Ledger(LEDGER,release) as ledger:
        archived_evidence(read_checked(PARENT/'CHECKPOINT.json'),LEDGER)
        members={p.relative_to(LEDGER).as_posix():sha(p) for p in LEDGER.rglob('*') if p.is_file() and p.suffix in ('.json','.jsonl')}
        path=ROOT/f'output/phase3_{STUDY}_20260913.zip'
        if not path.exists():
            with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED) as z:
                for name in sorted(members): z.write(LEDGER/name,name)
        with zipfile.ZipFile(path) as z:
            if z.testzip() or set(z.namelist())!=set(members) or any(hashlib.sha256(z.read(k)).hexdigest()!=v for k,v in members.items()):
                raise BudgetStop('Archive mismatch')
        check={'new_calls_during_verification':0,'historical_records_preserved':1814,
               'total_paid_records':len(ledger.state['reservations']),'study_accounted_nano':result['accounted_nano'],
               'provider_totals_nano':ledger.state['providers'],'phase3_accounted_nano':sum(ledger.state['providers'].values()),
               'package_accounted_nano':POLICY['prior_package_nano']+sum(ledger.state['providers'].values()),
               'archive':path.relative_to(ROOT).as_posix(),'archive_members':len(members),'archive_sha256':sha(path),
               'results_sha256':digest(result),'off_device_backup_verified':False}
    save(FOLDER/'CHECKPOINT.json',check)
    return check


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('command',choices=('prepare','run','verify')); parser.add_argument('--yes',action='store_true'); args=parser.parse_args()
    if args.command=='prepare':
        r,p,b=prepare(True); print(json.dumps({'maximum_usd':r['recognition_cap_nano']/1e9,'participant_calls':len(b)-1,'root_seed':SEEDS['population']}))
    elif args.command=='run':
        if not args.yes: raise BudgetStop('Explicit execution flag required')
        print(json.dumps(collect()))
    else: print(json.dumps(archive()))
