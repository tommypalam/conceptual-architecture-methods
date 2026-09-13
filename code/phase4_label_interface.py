"""Prospective named-label rating interface; r1 numeric outputs are not repaired."""
from phase4_moral_schema import RELATIVE,FIXED,validate_judgment

RELATIVE_LABELS={'triggered':1,'not_triggered':0,'unknown':None}
FIXED_LABELS={'upheld':1,'violated':0,'unknown':None}


def normalize(value,item_id,source_ids,version):
    if not isinstance(value,dict) or set(value)!={'item_id','manual_version','categories'}:
        raise ValueError('Invalid named-label schema')
    if value['item_id']!=item_id or value['manual_version']!=version:
        raise ValueError('Wrong item/manual')
    categories=value['categories']
    if not isinstance(categories,dict) or set(categories)!=set(RELATIVE+FIXED):
        raise ValueError('Missing or extra category')
    relative=[];fixed=[];evidence={}
    for name in RELATIVE+FIXED:
        c=categories[name];labels=RELATIVE_LABELS if name in RELATIVE else FIXED_LABELS
        if not isinstance(c,dict) or set(c)!={'label','source_ids','reason'}:
            raise ValueError('Invalid category entry')
        if not isinstance(c['label'],str) or c['label'] not in labels:
            raise ValueError('Invalid label or category polarity')
        result=labels[c['label']]
        (relative if name in RELATIVE else fixed).append(result)
        evidence[name]={'source_ids':c['source_ids'],'reason':c['reason'],
                        'unknown_reason':c['reason'] if result is None else None}
    normalized={'item_id':item_id,'manual_version':version,'configuration_relative':relative,
                'fixed_standard':fixed,'evidence':evidence}
    summary=validate_judgment(normalized,item_id,source_ids,version)
    return normalized,summary


def schema(version):
    return {'item_id':'COPY_PACKET_ID','manual_version':version,'categories':{
        name:{'label':'CHOOSE: triggered / not_triggered / unknown' if name in RELATIVE else
                     'CHOOSE: upheld / violated / unknown',
              'source_ids':['COPY_RELEVANT_FACT_ID'],'reason':'brief justification; if unknown identify the missing fact'}
        for name in RELATIVE+FIXED}}
