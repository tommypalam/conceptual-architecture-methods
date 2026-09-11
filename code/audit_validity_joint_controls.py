"""Post-score provenance audit of fresh versus previous canonical endpoint cells."""
from collections import Counter
import json
import logging
from pathlib import Path

import pandas as pandas

import run_validity_joint_wording as run
from run_validity_claude import save_new
import utils


def main():
    current=run.curve.BASE/'joint_wording_20260911';previous=run.PREVIOUS
    m=json.loads((current/'manifest.json').read_bytes())
    old=json.loads((previous/'manifest.json').read_bytes())
    new_plan,new_rows,_=run.base.inventory(current,m)
    old_plan,old_rows,_=run.base.inventory(previous,old)
    settings=('model','provider','temperature','max_tokens','configuration','transport_timeout_seconds')
    assert all(m['design'][k]==old['design'][k] for k in settings)
    rows=[];keys=[];all_selected=[]
    for pd in (.1,.9):
        for mor in (.1,.9):
            a=next(c for c in m['design']['cells'] if (c['arm'],c['pd_value'],c['value'])==('canonical',pd,mor))
            b=next(c for c in old['design']['cells'] if (c['background_value'],c['value'])==(pd,mor))
            assert a['messages']==b['messages'] and a['profile']==b['profile']
            for label,root,plan,records,cell in [('previous',previous,old_plan,old_rows,b),('current',current,new_plan,new_rows,a)]:
                group=[r for r in records if plan[r['record_key']][0]==cell]
                assert len(group)==30
                for r in group:
                    payload=r['response_payload']
                    assert payload['choices'][0]['message']['content']==r['raw_response']
                    assert payload['id']==r['api_call_id'] and payload['model']==run.base.MODEL
                    assert run.base.parse_decision(r['raw_response'],('ADOPT','WAIT'))==(r['parsed_decision'],r['parse_status'])
                    assert r['parse_status']=='ok' and not r['terminal_failure'] and r['attempts']==1
                    keys.append({'run':label,'record_key':r['record_key'],
                                 'sha256':run.sha256((root/'records'/(r['record_key']+'.json')).read_bytes()).hexdigest()})
                all_selected.extend(group)
                rows.append({'run':label,'pd_value':pd,'mor_value':mor,'n':30,
                             'adopt':sum(r['parsed_decision']=='ADOPT' for r in group),
                             'messages_hash':run.digest(cell['messages'])})
    assert len({r['api_call_id'] for r in all_selected})==240
    assert len({r['seed'] for r in all_selected})==240
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pandas.DataFrame(rows),
        f'Previous{len(old_rows)} ->120 endpoint records; current{len(new_rows)} ->120 canonical records; other{len(old_rows)+len(new_rows)-len(all_selected)} retained in original analyses',logging.getLogger('control-audit'))
    save_new(current/'analysis/canonical_repeat_audit.json',{
        'purpose':'Post-score provenance check prompted by23/30 versus8/30 at PD=.9/MoR=.9; not a preregistered stability test.',
        'design_hash':m['design_hash'],'previous_design_hash':old['design_hash'],
        'exact_profiles_messages_and_declared_settings_match':True,
        'unique_api_ids_and_requested_seeds':240,'raw_payload_text_and_record_parse_agree':True,
        'backend_fingerprint_counts':dict(Counter(str(r['response_payload'].get('system_fingerprint')) for r in all_selected)),
        'changed_conditions':'Different requested seeds, schedule, collection time and surrounding experimental allocation. No cause is identified.',
        'data_not_pooled':True,'script_sha256':run.sha256(Path(__file__).read_bytes()).hexdigest(),
        'cells':rows,'record_checksums':keys})
    print(json.dumps(rows,indent=2))


if __name__=='__main__':main()
