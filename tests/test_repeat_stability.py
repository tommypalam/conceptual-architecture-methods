from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import audit_validity_repeat_stability as audit


def rows(key,run,answers):
    return [{'prompt_key':key,'run':run,'problem':'S2','first':v,'timestamp_utc':f'2026-09-12T00:00:{i:02d}Z',
             'api_call_id':f'{run}-{i}','profile_hash':'profile','fingerprint':None,'service_tier':'default',
             'prompt_tokens':100,'cached_tokens':0,'response_text_hash':str(v)} for i,v in enumerate(answers)]


def test_key_preserves_exact_text_and_generation_settings():
    args=('model',1.,600,('A','B'))
    k=audit.prompt_key([{'role':'user','content':'x'}],*args)
    assert k!=audit.prompt_key([{'role':'user','content':'x '}],*args)
    assert k!=audit.prompt_key([{'role':'system','content':'x'}],*args)
    assert k!=audit.prompt_key([{'role':'user','content':'x'}],'model',0.,600,('A','B'))
    assert k!=audit.prompt_key([{'role':'user','content':'x'}],'model',1.,300,('A','B'))


def test_all_pairs_and_separate_temporal_family():
    data=rows('shift','a',[False]*20)+rows('shift','b',[True]*20)
    data+=rows('stable','a',[False,True]*10)+rows('stable','b',[False,True]*10)
    data+=rows('half','a',[False]*10+[True]*10)+rows('half','b',[False,True]*10)
    data+=rows('small','a',[False]*19)+rows('small','b',[True]*20)
    summaries,repeated,pairs,within=audit.summarize(data)
    assert len(summaries)==8 and len(repeated)==3 and len(pairs)==3 and len(within)==6
    assert [p['prompt_key'] for p in pairs if p['difference_detected']]==['shift']
    assert [(p['prompt_key'],p['run']) for p in within if p['difference_detected']]==[('half','a')]
    assert next(p for p in pairs if p['prompt_key']=='shift')['effect']['difference']==1


def test_legacy_bare_label_scoring_is_preserved():
    assert audit.parse_output('ADOPT',('ADOPT','WAIT'),'user_prefix_bare')==('ADOPT','ok')
    assert audit.parse_output('ADOPT',('ADOPT','WAIT'),'full_harness')[1]!='ok'
