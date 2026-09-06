"""Run the frozen Phase 1.5 Option-C comparison. Mock by default; old pilot untouched."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine.llm_client import LLMClient, MockClient
from engine.validity_sweep import build_design, freeze, execute, digest, ValiditySink
from engine.validity_analysis import analyze, markdown
import utils

ROOT = Path(__file__).resolve().parent.parent


def mock_response(messages, seed):
    user = messages[-1].content
    match = re.search(r'DECISION:\s*\[([^]]+)\]', user)
    labels = match.group(1).split('|') if match else re.search(r'Reply with only: (.+)', user).group(1).split(' or ')
    decision = labels[seed % 2].strip()
    return f'DECISION: {decision}\nREASONING: Mock output for plumbing verification.' if match else decision


def score(root):
    manifest = json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    d = manifest['design']
    if digest(d) != manifest['design_hash']:
        raise ValueError('Manifest integrity failure')
    records = list(ValiditySink(root/'records').read_all())
    if any(r.get('design_hash') != manifest['design_hash'] for r in records):
        raise ValueError('Record belongs to another protocol')
    report = analyze(records, params=d['params'], problems=d['problems'], arms=d['arms'], n=d['n'])
    report['provider'] = d['provider']
    report['design_hash'] = manifest['design_hash']
    if d['provider'] == 'mock':
        report['battery_status'] = 'MOCK DATA ONLY - NO EMPIRICAL VALIDITY CLAIM'
    # Version by content: resumable scoring never overwrites earlier summaries.
    version = digest(report)[:16]
    folder = root/'analysis'
    folder.mkdir(exist_ok=True)
    for suffix, content in [('json', json.dumps(report, indent=2, allow_nan=False)),
                            ('md', markdown(report))]:
        target = folder/f'summary_{version}.{suffix}'
        if not target.exists():
            with target.open('x', encoding='utf-8') as stream:
                stream.write(content)
    print(f'Analysis: {folder / ("summary_"+version+".md")}', flush=True)
    return report


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--provider', choices=['mock', 'openai'], default='mock')
    p.add_argument('--model', default='gpt-5.4-mini-2026-03-17')
    p.add_argument('--params', nargs='+', choices=utils.PARAM_NAMES, default=list(utils.PARAM_NAMES))
    p.add_argument('--problems', nargs='+', choices=['S1','S2','S3'], default=['S1','S2','S3'])
    p.add_argument('--n', type=int, default=50)
    p.add_argument('--seed', type=int, default=20260604)
    p.add_argument('--concurrency', type=int, choices=range(1,6), default=5)
    p.add_argument('--run-root', type=Path, required=True)
    p.add_argument('--prepare-only', action='store_true')
    p.add_argument('--score-only', action='store_true')
    p.add_argument('--limit', type=int, help='Checkpoint after this many NEW calls; fixed target N remains unchanged')
    p.add_argument('--yes', action='store_true')
    args = p.parse_args()
    if args.n <= 0 or (args.limit is not None and args.limit <= 0):
        p.error('n and limit must be positive')
    if len(set(args.params)) != len(args.params) or len(set(args.problems)) != len(args.problems):
        p.error('Duplicate parameters or problems')
    root = args.run_root.resolve()
    forbidden = [ROOT/'experiments'/name for name in
                 ('phase0_baseline_calibration','phase0b_calibration','phase0c_locked_holdout','phase1_pilot')]
    forbidden.append(ROOT/'experiments'/'phase1_5_encoding_validity'/'sweeps_pilot')
    if any(root == path or path in root.parents for path in forbidden):
        p.error('Run root overlaps a preserved experiment')
    if args.score_only:
        score(root)
        return
    if not args.prepare_only and args.provider == 'openai' and not os.environ.get('OPENAI_API_KEY'):
        p.error('OPENAI_API_KEY is unavailable; configure it outside chat, or use --prepare-only')
    model = args.model if args.provider == 'openai' else 'mock-model'
    design = build_design(params=args.params, problems=args.problems, n=args.n,
                          seed=args.seed, provider=args.provider, model=model)
    print(f'Configuration: neutral | {len(args.params)} parameters | problems {args.problems} | '
          f'N={args.n}/cell | 2 deliveries | {design["planned_calls"]} calls | root seed {args.seed} | model {model}', flush=True)
    if args.provider == 'openai' and not args.prepare_only and not args.yes:
        if input('Run paid API calls under this frozen protocol? [y/N] ').lower().strip() != 'y':
            return
    manifest = freeze(root/'manifest.json', design)
    if args.prepare_only:
        print(f'Frozen protocol: {root / "manifest.json"}; no API calls made')
        return
    client = (MockClient(responder=mock_response, concurrency=args.concurrency) if args.provider == 'mock'
              else LLMClient(model=model, concurrency=args.concurrency))
    try:
        asyncio.run(execute(manifest, client=client, sink=ValiditySink(root/'records'),
                            concurrency=args.concurrency, limit=args.limit))
    finally:
        score(root)


if __name__ == '__main__':
    main()
