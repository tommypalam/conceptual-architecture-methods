"""Offline audit verification and transparent, prevalence-aware report."""
from hashlib import sha256
import json
from pathlib import Path
import zipfile
import pandas as pd
import logging
import run_structural_encoding_audit_schema_r3 as audit


def report():
    root=audit.ROOT;m=json.loads((root/'manifest.json').read_bytes());audit.check(m)
    rows=list(audit.ValiditySink(root/'records').read_all())
    if len(rows)!=200 or any(r['parse_status']!='ok' for r in rows):raise ValueError('Audit incomplete')
    jobs={j['item_id']:j for j in m['design']['jobs']}
    pack=json.loads((root/'blind_pack.json').read_bytes())
    if audit.digest(pack)!=m['design']['blind_pack_hash']:raise ValueError('Pack mismatch')
    for item in pack['items']:
        if jobs[item['item_id']]['messages']!=[vars(v) for v in audit.brief_messages(pack,item)]:raise ValueError('Blind request differs')
    for r in rows:
        if audit.digest({k:v for k,v in r.items() if k!='record_hash'})!=r['record_hash']:raise ValueError('Record hash mismatch')
        if r['request_messages']!=jobs[r['item_id']]['messages'] or r['output_config']!=audit.OUTPUT_CONFIG:raise ValueError('Request mismatch')
        if r['model_version']!=audit.MODEL or r['temperature']!=1 or r['max_tokens']!=1000 or r['attempts']!=1:raise ValueError('Setting mismatch')
        payload=r['response_payload']
        if payload['id']!=r['api_call_id'] or payload['model']!=audit.MODEL:raise ValueError('Raw identity mismatch')
        if ''.join(v['text'] for v in payload['content'] if v['type']=='text')!=r['raw_response']:raise ValueError('Raw text mismatch')
        if audit.parse_brief(r['raw_response'])[0]!=r['estimates']:raise ValueError('Reparse mismatch')
    ids=[r['api_call_id'] for r in rows]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate coder IDs')
    reports={}
    for key_file,pattern,name in [('private_answer_key.json','audit_*.json','primary'),('private_answer_key_rendered.json','rendered_truth_sensitivity_*.json','rendered')]:
        key=json.loads((root/key_file).read_bytes())
        if key['blind_pack_hash']!=m['design']['blind_pack_hash']:raise ValueError('Key mismatch')
        paths=list((root/'analysis').glob(pattern))
        if len(paths)!=1:raise ValueError('Expected one scoring result')
        r=json.loads(paths[0].read_bytes())
        if audit.score_audit(key,rows,permutations=1999)!=r:raise ValueError('Score differs on recomputation')
        reports[name]=r
    backup=json.loads((root/'local_backup.json').read_bytes());p=Path(backup['path'])
    if sha256(p.read_bytes()).hexdigest()!=backup['sha256']:raise ValueError('Archive mismatch')
    with zipfile.ZipFile(p) as z:
        if z.testzip():raise ValueError('Corrupt archive')
        for folder in ('records','dispatches'):
            for f in (root/folder).rglob('*.json'):
                if z.read(f.relative_to(root).as_posix())!=f.read_bytes():raise ValueError('Archived raw file differs')
        for name in ('manifest.json','blind_pack.json','private_answer_key.json','private_answer_key_rendered.json'):
            if z.read(name)!=(root/name).read_bytes():raise ValueError('Archived key/manifest differs')
    parameters=reports['primary']['parameters']
    order=sorted(range(10),key=lambda i:parameters[i]['active_stratified_permutation_p']);last=0.;holm={}
    for rank,i in enumerate(order):
        last=max(last,min(1.,(10-rank)*parameters[i]['active_stratified_permutation_p']))
        holm[parameters[i]['parameter']]=last
    tab=[]
    for r in parameters:
        tab.append({'parameter':r['parameter'],'all_accuracy':r['all_items']['accuracy'],
            'all_majority_baseline':r['all_items']['majority_class_baseline'],
            'active_accuracy':r['active_parameter_items']['accuracy'],
            'active_balanced_accuracy':r['active_parameter_items']['balanced_accuracy'],
            'active_majority_baseline':r['active_parameter_items']['majority_class_baseline'],
            'active_p_unadjusted':r['active_stratified_permutation_p'],'active_p_holm_supplement':holm[r['parameter']],
            'abstentions':sum(x['estimates'][r['parameter']]['quartile'] is None for x in rows)})
    logging.basicConfig(level=logging.INFO)
    audit.run.utils.log_dataframe_summary(pd.DataFrame(tab),'200 codings -> ten parameter summaries; no exclusion',logging.getLogger('audit'))
    audit.save_new(root/'analysis/prevalence_summary.json',{'parameters':tab,
        'holm_note':'Supplementary ten-test multiplicity qualification; original scoring unchanged. No gate replacement.'})
    audit.save_new(root/'analysis/verification.json',{'status':'PASS','records':200,'unique_api_ids':200,
        'exact_blind_requests_schema_settings_verified':True,'both_keys_scores_recomputed':True,'raw_zip_byte_equality_verified':True,'off_device_backup_verified':False})
    r=reports['primary'];lines=['# Independent blind audit, schema R3','',
        f"200/200 valid codings. Literal historical threshold met: **{r['literal_spec_thresholds_met']}**. No prior failed-designation codings pooled.",
        'Same pinned Haiku4.5, brief messages, stratified selection seed20261011 and scoring. Schema-constrained JSON and max1000 are disclosed format changes. Behavioral responses were already generated independently.',
        '', '| Parameter | All-item accuracy | Majority baseline | Active accuracy (N20) | Active balanced accuracy | Active permutation p | Supplementary Holm p | Abstentions /200 |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for x in tab:lines.append(f"| {x['parameter']} | {x['all_accuracy']:.1%} | {x['all_majority_baseline']:.1%} | {x['active_accuracy']:.1%} | {x['active_balanced_accuracy']:.1%} | {x['active_p_unadjusted']:.4f} | {x['active_p_holm_supplement']:.4f} | {x['abstentions']} |")
    lines+=['',f"Primary literal counts: {sum(x['literal_spec_above_035'] for x in parameters)}/10 above35% with the historical p criterion (six required); {sum(x['literal_spec_at_least_050'] for x in parameters)}/10 at least50% (four required).",
        f"Rendered-value sensitivity literal threshold: {reports['rendered']['literal_spec_thresholds_met']}. Rounding changes27/2000 background truths, zero active truths; primary key remains full precision. Decimal literals detected in {r['n_decimal_literal_traces']}/200 source explanations.",
        '', 'All-item prevalence is not uniform: a25% chance reference alone cannot establish profile recovery. Each active trait has20 selected traces spanning all three dilemmas, including contexts where that trait may have little visible role. Abstention counts as incorrect. These data assess recovery from brief self-explanations, which neither reveal internal computations nor exhaust the evidence of causal parameter influence.',
        '', 'Original Wilson intervals and permutation outputs are retained. Repeated source backgrounds create dependence; the existing problem-stratified permutation does not additionally cluster by background. Treat these as the frozen audit diagnostics, not a proof of independent mechanistic access. The ten-test Holm supplement qualifies nominal p-values and does not replace the original rule.',
        '', 'Raw records, exact public messages, both answer keys, reparsing,200 distinct API IDs and same-computer archive equality verified. Private profiles/answer keys were not supplied to the coder. No off-device backup claimed.',
        '', '[Repair protocol](../PROTOCOL.md) | [Verification](verification.json) | [Prevalence summary](prevalence_summary.json)','']
    (root/'analysis/REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'literal_threshold':r['literal_spec_thresholds_met'],'above035':sum(x['literal_spec_above_035'] for x in parameters),'atleast050':sum(x['literal_spec_at_least_050'] for x in parameters),'parameters':tab}))


if __name__=='__main__':report()
