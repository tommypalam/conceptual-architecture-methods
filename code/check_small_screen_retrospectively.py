"""One fixed retrospective 80-record check; no API use, selection search or new validation."""
import hashlib
import json
import logging
from pathlib import Path

import pandas as pd
import utils
from engine.validity_analysis import wilson
from engine.validity_sweep import verify_record,digest
from run_validity_claude import save_new
from run_validity_claude_screen import exact,ROOT


def main():
    source=ROOT/'experiments/phase1_5_encoding_validity/axis_instruction_20260911_assembled'
    out=ROOT/'experiments/phase1_5_encoding_validity/claude_screen_20260911/offline'
    names=['canonical','paraphrase_1','paraphrase_2','paraphrase_3'];rows=[]
    for name in names:
        for k in range(1,21):
            key=f'equivalence/baseline_{name}/PD/S3/0.8/call_{k:04d}'
            r=json.loads((source/'records'/(key+'.json')).read_text(encoding='utf-8'));verify_record(r)
            if r['wording']!=name or r['arm']!='baseline' or r['call_index']!=k:raise ValueError('Unexpected source slot')
            rows.append(r)
    logging.basicConfig(level=logging.INFO);logger=logging.getLogger('retrospective-screen')
    utils.log_dataframe_summary(pd.DataFrame([{k:r[k] for k in ('wording','record_key','parsed_decision','parse_status')} for r in rows]),
        'Exactly first 20 call indices per baseline wording; no outcome filter',logger)
    cells=[]
    for name in names:
        group=[r for r in rows if r['wording']==name]
        good=[r for r in group if r['parse_status']=='ok' and r['parsed_decision'] in r['labels']]
        k=sum(r['parsed_decision']=='ADOPT' for r in good)
        cells.append({'wording':name,'n_recorded':len(group),'n_valid':len(good),'adopt':k,'rate':k/len(good) if good else None,
                      'ci95':wilson(k,len(good))})
    utils.log_dataframe_summary(pd.DataFrame(cells),'Four retrospective cells; exclusions counted explicitly',logger)
    a,b=cells[2:4];ai=exact(a['adopt'],20,20-a['n_valid']);bi=exact(b['adopt'],20,20-b['n_valid'])
    interval=[ai[0]-bi[1],ai[1]-bi[0]]
    result={'source_root':str(source),'selection':'First 20 call indices in each of four original baseline formulations; selected once after full outcomes were known. No search over indices, sizes or seeds.',
        'n_selected':80,'cells':cells,'primary_pair':['paraphrase_2','paraphrase_3'],
        'difference':a['rate']-b['rate'],'conservative_95_interval':interval,
        'gross_failure_detected':bool(interval[0]>.10 or interval[1]<-.10),
        'record_index':[{'record_key':r['record_key'],'record_hash':r['record_hash']} for r in rows],
        'source_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'limits':'Retrospective worked example only; no new responses, no independent validation, no general power estimate and no evidence about Claude.'}
    path=out/f'retrospective_{digest(result)[:16]}.json';save_new(path,result)
    text=['# A small screen applied to existing OpenAI data','',
        'This one retrospective worked example uses the first 20 call indices of each original baseline formulation: 80 existing responses, zero new API calls. The full-sample outcomes were already known. No alternative subsets, seeds or sample sizes were searched.','',
        '| Wording | ADOPT / valid | Rate | Pointwise Wilson 95% interval |','|---|---:|---:|---|']
    for c in cells:text.append(f'| {c["wording"]} | {c["adopt"]}/{c["n_valid"]} | {c["rate"]:.3f} | {c["ci95"][0]:.3f} to {c["ci95"][1]:.3f} |')
    text+=['',f'P2 minus P3: {result["difference"]:.3f}; conservative exact interval {interval[0]:.3f} to {interval[1]:.3f}.',
        f'The proposed gross-failure rule detects an effect beyond the .10 margin in this subset: **{result["gross_failure_detected"]}**.','',
        'This illustrates the screening procedure on a known failure. It does not estimate general power, validate the chosen sample size or predict Claude performance. Failure to detect a gap in a future small sample would remain inconclusive, not evidence of equivalence.',
        f'Numerical evidence and all selected hashes: [{path.name}]({path.name}).','']
    report=out/'RETROSPECTIVE_SCREEN.md';content='\n'.join(text)
    if report.exists() and report.read_text(encoding='utf-8')!=content:raise ValueError('Existing report differs')
    report.write_text(content,encoding='utf-8');print(content)


if __name__=='__main__':main()
