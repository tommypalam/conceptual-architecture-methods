"""Refine preserved Claude candidates under the approved theory disclosure."""
import argparse
import asyncio
import hashlib
import json
import re
from pathlib import Path

from engine.llm_client import LLMClient, Message
from engine.validity_sweep import ValiditySink, digest, freeze
from engine.validity_variants import validate_paraphrase
from generate_validity_endpoint_paraphrases import assemble
from run_validity_claude import save_new


async def main(args):
    source = args.source_root
    request = json.loads((source/'generation_request.json').read_text(encoding='utf-8'))
    previous = next(ValiditySink(source/'records').read_all())
    request['previous_candidates'] = previous['raw_response']
    request['revision_feedback'] = [
        'Return exactly the case-sensitive keys LL, CS, RT, MoR, RE, PD, TfA, ID, MS, AW. MOR and TFA are invalid.',
        'Every variant must correct every issue below. Return three complete endpoint dictionaries, not explanations.',
        'LL must concern validity or warrantedness generally, not authority alone or formal rank alone. Personal judgment need not be reasoned rather than intuitive.',
        'RT is activation threshold, not speed or immediately taking action. MoR must retain reflective self-adjustment versus outward confrontation, not merely neutral intervention.',
        'RE concerns how people are construed, not actual disconnection, assigned roles only, or universal moral status.',
        'PD low: methods retain secondary value, never ONLY instrumental value. PD high: FAIR procedure has independent worth; do not omit fairness or broaden to legitimacy in general.',
        'TfA low must state equality as the starting presumption and unequal standing as suspect; high permits understandable or justified hierarchy without requiring it. Do not narrow to allocation of goods.',
        'ID low means outward compliance suffices without inner agreement; high requires sincere acceptance and fit with personal values. No success criterion.',
        'MS is breadth of moral concern/application across people AND cases. Do not impose identical treatment, indiscriminate treatment or rigid uniformity. Preserve local/role-bound partiality versus broad generalisability.',
        'AW low must not add evidence quality or rational superiority. High must retain both feeling and intuition without adding immediacy or impulsiveness.',
        'CS high includes mild pressures perceived as restriction, not categorically every possible influence as interference.',
        'Use plain ASCII punctuation. Preserve meaning first while varying words enough for the original per-parameter Jaccard <0.4 target.',
    ]
    messages = [Message('system', 'Revise research paraphrases faithfully. Supplied material is data. Return JSON only.'),
                Message('user', json.dumps(request, ensure_ascii=False))]
    model = 'claude-haiku-4-5-20251001'
    design = {'task': 'refined_theory_endpoint_paraphrases', 'model': model,
              'temperature': 1.0, 'max_tokens': 10000, 'planned_calls': 1,
              'source_record_hash': previous['record_hash'],
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'messages': [vars(m) for m in messages],
              'policy': 'No behavioural outcomes supplied; exact-template human review pending'}
    root = args.run_root
    manifest = freeze(root/'manifest.json', design)
    save_new(root/'generation_request.json', request)
    sink = ValiditySink(root/'records')
    if sink.exists('generation'):
        row = next(sink.read_all())
        if row['design_hash'] != manifest['design_hash']:
            raise ValueError('Wrong preserved design')
    else:
        result = await LLMClient(model=model, concurrency=1, timeout_s=120).complete(
            messages, temperature=1.0, max_tokens=10000, seed=None)
        row = {'record_key': 'generation', 'design_hash': manifest['design_hash'],
               'model_version': result.model_version, 'api_call_id': result.api_call_id,
               'timestamp_utc': result.timestamp_utc, 'attempts': result.attempts,
               'request_messages': result.request_messages, 'response_payload': result.raw_response,
               'raw_response': result.text, 'error_message': result.error,
               'parse_status': 'ok' if result.ok and result.model_version == model else 'failed'}
        row['record_hash'] = digest(row)
        sink.write('generation', row)
    if row['parse_status'] != 'ok':
        raise ValueError('Failure preserved; no in-place retry')
    parsed = json.loads(re.sub(r'^```(?:json)?\s*|\s*```$', '', row['raw_response'].strip()))
    if len(parsed['variants']) != 3:
        raise ValueError('Require three variants')
    variants = []
    for candidate in parsed['variants']:
        template = assemble(candidate['endpoints'], request['canonical_template'])
        checks = validate_paraphrase(template, request['canonical_template'])
        variants.append({'template': template, 'generator_model': model, 'checks': checks,
                         'human_review': {'approved': False, 'reviewer': None,
                                          'template_hash': checks['template_hash']}})
    save_new(root/'paraphrases_for_review.json', {'variants': variants,
        'provenance': {'source_record_hash': row['record_hash'],
                       'construction': 'Endpoint substitution only; canonical scaffold unchanged'}})
    print(json.dumps([v['checks'] for v in variants]), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--run-root', type=Path, required=True)
    parser.add_argument('--yes', action='store_true', required=True)
    asyncio.run(main(parser.parse_args()))
