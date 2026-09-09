"""Ask the pinned Claude model to rewrite flagged endpoints from semantic feedback."""
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
    previous = next(ValiditySink(source/'records').read_all())
    prior_request = json.loads((source/'generation_request.json').read_text(encoding='utf-8'))
    candidates = json.loads(re.sub(r'^```(?:json)?\s*|\s*```$', '', previous['raw_response'].strip()))
    corrections = json.loads(args.corrections.read_text(encoding='utf-8'))
    request = {
        'task': 'Rewrite ONLY the flagged endpoints using your own words to resolve each issue. Preserve every unlisted endpoint verbatim. Return the full corrected three-variant JSON and nothing else. Each parameter pair must keep word-set Jaccard below 0.4 versus canonical; preserve meaning first.',
        'canonical_template': prior_request['canonical_template'],
        'theory_section_3_1': prior_request['theory_section_3_1'],
        'previous_candidates': candidates,
        'corrections': corrections,
        'provenance': 'Claude-generated wording revised from assistant semantic feedback; no behavioural outcomes supplied. Human semantic approval remains pending.'}
    model = 'claude-haiku-4-5-20251001'
    messages = [Message('system', 'Correct flagged research paraphrases according to semantic feedback. Generate the replacement words yourself; preserve unflagged endpoints. Return JSON only.'),
                Message('user', json.dumps(request, ensure_ascii=False))]
    manifest = freeze(args.run_root/'manifest.json', {
        'task': 'claude_apply_explicit_semantic_corrections', 'model': model,
        'temperature': 1.0, 'max_tokens': 10000, 'planned_calls': 1,
        'source_record_hash': previous['record_hash'],
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'messages': [vars(m) for m in messages], 'policy': request['provenance']})
    save_new(args.run_root/'generation_request.json', request)
    sink = ValiditySink(args.run_root/'records')
    if sink.exists('generation'):
        row = next(sink.read_all())
        if row['design_hash'] != manifest['design_hash']:
            raise ValueError('Wrong preserved design')
    else:
        result = await LLMClient(model=model, concurrency=1, timeout_s=120).complete(messages,
            temperature=1.0, max_tokens=10000, seed=None)
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
    if len(parsed.get('variants', [])) != 3:
        raise ValueError('Require exactly three variants')
    flagged={(e['variant'],e['parameter'],e['endpoint']) for e in corrections}
    for number,candidate in enumerate(candidates['variants'],1):
        for code,pair in candidate['endpoints'].items():
            for pole,text in pair.items():
                if (number,code,pole) not in flagged and parsed['variants'][number-1]['endpoints'][code][pole]!=text:
                    raise ValueError('Unflagged wording changed; preserve and review')
    variants=[]
    for candidate in parsed['variants']:
        template=assemble(candidate['endpoints'], request['canonical_template'])
        checks=validate_paraphrase(template, request['canonical_template'])
        variants.append({'template': template, 'generator_model': model, 'checks': checks,
            'human_review': {'approved': False, 'reviewer': None, 'template_hash': checks['template_hash']}})
    save_new(args.run_root/'paraphrases_for_review.json', {'variants': variants,
        'provenance': {'source_record_hash': row['record_hash'], 'construction': request['provenance'],
                       'corrections_hash': digest(corrections)}})
    print(json.dumps([v['checks'] for v in variants]), flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root', type=Path, required=True)
    p.add_argument('--run-root', type=Path, required=True)
    p.add_argument('--corrections', type=Path, required=True)
    p.add_argument('--yes', action='store_true', required=True)
    asyncio.run(main(p.parse_args()))
