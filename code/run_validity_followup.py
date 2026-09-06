"""Prepare/run robustness comparisons; mock by default, source sweep preserved."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from engine.llm_client import LLMClient, MockClient
from engine.validity_sweep import ValiditySink, digest, freeze
from engine.validity_followup import comparison_design, execute_comparison, summarize_cells, load_source, paraphrase_equivalence, gradient_comparison
from engine.validity_analysis import analyze
from engine.validity_variants import load_reviewed_paraphrases
from run_validity_sweep import mock_response


def score(root,baseline_root=None):
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    if digest(manifest['design'])!=manifest['design_hash']:
        raise ValueError('Manifest integrity failure')
    report=summarize_cells(manifest,list(ValiditySink(root/'records').read_all()))
    d=manifest['design']
    report['battery_status']='OPEN: all subtests and scientific review still required'
    if d['experiment']=='gradients':
        source=load_source(d['source_root']); sd=source['design']
        if source['design_hash']!=d['source_design_hash']:
            raise ValueError('Wrong hybrid source')
        source_rows=list(ValiditySink(Path(d['source_root'])/'records').read_all())
        if any(r['design_hash']!=source['design_hash'] for r in source_rows):
            raise ValueError('Mixed source protocols')
        analysis=analyze(source_rows,params=sd['params'],problems=sd['problems'],arms=sd['arms'],n=sd['n'])
        report['gradients']=gradient_comparison(report['cells'],analysis['sweeps'])
    if baseline_root is not None:
        baseline=load_source(baseline_root); bd=baseline['design']
        if d['experiment']!='paraphrases' or bd.get('experiment')!='rotations':
            raise ValueError('Paraphrases require a rotations baseline')
        for field in ('source_design_hash','model','provider','n','temperature','max_tokens'):
            if d[field]!=bd[field]:
                raise ValueError(f'Incompatible baseline: {field}')
        baseline_cells=summarize_cells(baseline,list(ValiditySink(baseline_root/'records').read_all()))['cells']
        report['paraphrase_equivalence']=paraphrase_equivalence(report['cells']+baseline_cells)
        report['baseline_design_hash']=baseline['design_hash']
    if d['provider']=='mock':
        report['battery_status']='MOCK DATA ONLY - NO EMPIRICAL VALIDITY CLAIM'
    folder=root/'analysis'; folder.mkdir(exist_ok=True)
    target=folder/f'cells_{digest(report)[:16]}.json'
    if not target.exists():
        target.write_text(json.dumps(report,indent=2,allow_nan=False),encoding='utf-8')
    print(f'Cell report: {target}')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--run-root',type=Path,required=True)
    p.add_argument('--experiment',choices=['rotations','gradients','paraphrases'],required=True)
    p.add_argument('--provider',choices=['mock','openai'],default='mock')
    p.add_argument('--paraphrases',type=Path)
    p.add_argument('--baseline-root',type=Path,help='Rotations run supplying canonical .8 cells for paraphrase scoring')
    p.add_argument('--n',type=int,default=50)
    p.add_argument('--concurrency',type=int,choices=range(1,6),default=5)
    p.add_argument('--limit',type=int)
    p.add_argument('--prepare-only',action='store_true')
    p.add_argument('--score-only',action='store_true')
    p.add_argument('--yes',action='store_true')
    a=p.parse_args(); root=a.run_root.resolve(); source=a.source_root.resolve()
    if root==source or source in root.parents or root in source.parents:
        p.error('Follow-up root must be separate from the source experiment')
    if a.n<=0 or (a.limit is not None and a.limit<=0):
        p.error('n and limit must be positive')
    if a.score_only:
        score(root,a.baseline_root); return
    paraphrases=load_reviewed_paraphrases(a.paraphrases) if a.paraphrases else None
    design=comparison_design(source,a.experiment,n=a.n,provider=a.provider,paraphrases=paraphrases)
    manifest=freeze(root/'manifest.json',design)
    print(f'{a.experiment}: {design["planned_calls"]} planned calls; model {design["model"]}')
    if a.prepare_only:
        return
    if a.provider=='openai' and (not a.yes or not os.environ.get('OPENAI_API_KEY')):
        p.error('Real calls require --yes and OPENAI_API_KEY configured outside chat')
    client=(MockClient(responder=mock_response,concurrency=a.concurrency) if a.provider=='mock'
            else LLMClient(model=design['model'],concurrency=a.concurrency))
    try:
        asyncio.run(execute_comparison(manifest,client=client,sink=ValiditySink(root/'records'),
                                       concurrency=a.concurrency,limit=a.limit))
    finally:
        score(root,a.baseline_root)


if __name__=='__main__':
    main()
