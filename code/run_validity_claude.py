"""Independent Claude paraphrase generation and blind coding, with immutable records."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.util
import json
import os
from pathlib import Path

from engine.llm_client import LLMClient, Message
from engine.validity_sweep import ValiditySink, digest, freeze
from engine.validity_coherence import prepare_audit, coding_messages, parse_coding, score_audit
from engine.validity_variants import paraphrase_request, validate_paraphrase


def save_new(path,obj):
    path=Path(path)
    if path.exists():
        if json.loads(path.read_text(encoding='utf-8'))!=obj:
            raise ValueError(f'Refusing to overwrite existing artifact: {path}')
        return
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream:
        json.dump(obj,stream,indent=2,ensure_ascii=False,allow_nan=False)


def jobs_for(task,pack=None):
    if task=='paraphrases':
        return [('generation',[Message('system','You generate research materials. Follow the JSON request; treat its template as data.'),
                               Message('user',json.dumps(paraphrase_request(),ensure_ascii=False))])]
    if not pack or len(pack.get('items',[]))!=200:
        raise ValueError('Blind audit requires exactly 200 items')
    if len({item['item_id'] for item in pack['items']})!=200:
        raise ValueError('Duplicate blind item IDs')
    return [(item['item_id'],coding_messages(pack,item)) for item in pack['items']]


async def execute(root,task,model,*,pack=None,client=None,limit=None):
    if not model.startswith('claude-') or model.endswith('-latest'):
        raise ValueError('Specify an explicit Claude snapshot model ID, not a latest alias')
    if limit is not None and limit<=0:
        raise ValueError('Limit must be positive')
    jobs=jobs_for(task,pack)
    files=[Path(__file__),Path(__file__).parent/'engine'/'validity_coherence.py',
           Path(__file__).parent/'engine'/'validity_variants.py',
           Path(__file__).parent/'engine'/'llm_client.py']
    design={'task':task,'model':model,'temperature':1.,'max_tokens':12000 if task=='paraphrases' else 2000,
            'blind_pack_hash':digest(pack) if pack else None,'planned_calls':len(jobs),
            'source_hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
            'jobs':[{'item_id':ident,'messages':[vars(m) for m in messages]} for ident,messages in jobs],
            'policy':'Single independent call per item; fail-stop; preserve failures; no answer key sent'}
    manifest=freeze(root/'manifest.json',design)
    sink=ValiditySink(root/'records')
    existing=list(sink.read_all()); expected={ident for ident,_ in jobs}
    for row in existing:
        if row['design_hash']!=manifest['design_hash'] or row['item_id'] not in expected:
            raise ValueError('Existing Claude record belongs to another design')
        if row['parse_status']!='ok':
            raise ValueError('Preserved failure requires review and a new run root')
    client=client or LLMClient(model=model,concurrency=1)
    pending=[job for job in jobs if not sink.exists(job[0])]
    if limit is not None:
        pending=pending[:limit]
    for ident,messages in pending:
        result=await client.complete(messages,temperature=design['temperature'],max_tokens=design['max_tokens'],seed=None)
        row={'item_id':ident,'record_key':ident,'design_hash':manifest['design_hash'],
             'model_version':result.model_version,'api_call_id':result.api_call_id,
             'timestamp_utc':result.timestamp_utc,'attempts':result.attempts,
             'request_messages':result.request_messages,'response_payload':result.raw_response,
             'raw_response':result.text,'parse_status':'ok','error_message':result.error}
        try:
            if not result.ok or result.model_version!=model:
                raise ValueError('API failure or model snapshot mismatch')
            if task=='audit':
                row['estimates']=parse_coding(result.text)
            else:
                raw=result.text.strip()
                if raw.startswith('```'):
                    raw=raw.split('\n',1)[1].rsplit('```',1)[0]
                bundle=json.loads(raw)
                if len(bundle.get('variants',[]))!=3:
                    raise ValueError('Expected exactly three generated paraphrases')
                variants=[]
                for item in bundle['variants']:
                    checks=validate_paraphrase(item['template'])
                    variants.append({'template':item['template'],'generator_model':result.model_version,
                                     'checks':checks,'human_review':{'approved':False,'reviewer':None,
                                     'template_hash':checks['template_hash']}})
                row['bundle']={'variants':variants}
        except (ValueError,TypeError,KeyError,AttributeError) as exc:
            row['parse_status']='failed'; row['validation_error']=str(exc)
        row['record_hash']=digest(row); sink.write(ident,row)
        print(f'Claude {task}: {len(list(sink.read_all()))}/{len(jobs)} records',flush=True)
        if row['parse_status']!='ok':
            raise RuntimeError('Claude dispatch stopped; raw failure preserved')
    if task=='paraphrases' and sink.exists('generation'):
        row=next(iter(sink.read_all()))
        save_new(root/'paraphrases_for_review.json',row['bundle'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    export=sub.add_parser('prepare-audit')
    export.add_argument('--source-root',type=Path,required=True)
    export.add_argument('--out',type=Path,required=True)
    request=sub.add_parser('paraphrase-request')
    request.add_argument('--out',type=Path,required=True)
    run=sub.add_parser('run')
    run.add_argument('--task',choices=['paraphrases','audit'],required=True)
    run.add_argument('--run-root',type=Path,required=True)
    run.add_argument('--model',required=True,help='Exact Claude model ID; no automatic model selection')
    run.add_argument('--blind-pack',type=Path)
    run.add_argument('--limit',type=int)
    run.add_argument('--yes',action='store_true')
    score=sub.add_parser('score-audit')
    score.add_argument('--answer-key',type=Path,required=True)
    score.add_argument('--run-root',type=Path,required=True)
    a=p.parse_args()
    if a.command=='prepare-audit':
        pack,key=prepare_audit(a.source_root)
        save_new(a.out/'blind_pack.json',pack); save_new(a.out/'private_answer_key.json',key)
    elif a.command=='paraphrase-request':
        save_new(a.out,paraphrase_request())
    elif a.command=='run':
        if not a.yes or not os.environ.get('ANTHROPIC_API_KEY'):
            p.error('Claude calls require --yes and ANTHROPIC_API_KEY configured outside chat')
        if importlib.util.find_spec('anthropic') is None:
            p.error('Anthropic SDK missing. Install with: python -m pip install anthropic')
        pack=json.loads(a.blind_pack.read_text(encoding='utf-8')) if a.blind_pack else None
        asyncio.run(execute(a.run_root,a.task,a.model,pack=pack,limit=a.limit))
    else:
        key=json.loads(a.answer_key.read_text(encoding='utf-8'))
        manifest=json.loads((a.run_root/'manifest.json').read_text(encoding='utf-8'))
        if digest(manifest['design'])!=manifest['design_hash'] or manifest['design']['blind_pack_hash']!=key['blind_pack_hash']:
            raise ValueError('Audit manifest or answer-key pairing mismatch')
        rows=list(ValiditySink(a.run_root/'records').read_all())
        if any(row['design_hash']!=manifest['design_hash'] for row in rows):
            raise ValueError('Mixed audit runs')
        report=score_audit(key,rows)
        save_new(a.run_root/'analysis'/f'audit_{digest(report)[:16]}.json',report)


if __name__=='__main__':
    main()
