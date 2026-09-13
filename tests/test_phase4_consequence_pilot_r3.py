import contextlib
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import phase4_consequence_pilot_r3 as study
from phase4_moral_transport import parse as transport_parse
from phase4_consequence_tasks_r3 import TASK_IDS,task,transition,mapping,card,check_cards
from phase4_moral_schema import RELATIVE,FIXED,validate_judgment
from phase3_budget import BudgetStop,digest,read_checked


def fake_judgment(packet):
    """Authored test-only labels, never sent as calibration or empirical data."""
    relative=[0]*8;fixed=[1]*4;item=packet['item_id']
    for t in TASK_IDS:
        for a,info in task(t)['actions'].items():
            if item!=card(t,a)['item_id']:continue
            effects=transition(t,a)
            relative[1]=int(info['deceptive']);relative[2]=int(effects['total_delta']<0)
            relative[3]=int(a in ('falsify','skip','unequal'))
            relative[4]=int(a in ('report','equal'));relative[5]=int(a=='report')
            relative[6]=int(a in ('report','equal','unequal'));relative[7]=int(a=='report')
            fixed=[int(all(x>=0 for x in effects['third_party_deltas'])),int(not info['deceptive']),1,int(a!='unequal')]
    for c,expected in check_cards():
        if item==c['item_id']:
            for schema,indices in expected.items():
                target=relative if schema=='configuration_relative' else fixed
                for i,value in indices.items():target[i]=value
    return {'item_id':item,'manual_version':study.MANUAL,'configuration_relative':relative,'fixed_standard':fixed,
            'evidence':{name:{'source_ids':list(packet['facts']), 'reason':'Synthetic test fixture only.',
                'unknown_reason':'Missing mandate in this test fixture.' if value is None else None}
                for name,value in zip(RELATIVE+FIXED,relative+fixed)}}


def named_judgment(packet):
    value=fake_judgment(packet)
    values=value['configuration_relative']+value['fixed_standard']
    return {'item_id':value['item_id'],'manual_version':study.MANUAL,'categories':{
        name:{'label':('unknown' if v is None else ('triggered' if v else 'not_triggered')
                      if name in RELATIVE else ('upheld' if v else 'violated')),
              'source_ids':value['evidence'][name]['source_ids'],'reason':value['evidence'][name]['reason']}
        for name,v in zip(RELATIVE+FIXED,values)}}


class ConsequencePilotR3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pop=study.Population.draw(study.N,seed=study.SEED).to_dict()

    def test_transitions_and_controls(self):
        self.assertEqual(transition('disclosure_12','report')['total_delta'],-4)
        self.assertEqual(transition('disclosure_2','report')['total_delta'],6)
        self.assertEqual(transition('allocation_12','unequal')['third_party_deltas'],[2,10])
        for t in TASK_IDS:
            for a in task(t)['actions']:
                self.assertEqual(sum(mapping(t,i).get(l)==a for i in range(1,7) for l in 'ABC'),6)
                for label in 'ABC':self.assertEqual(sum(mapping(t,i)[label]==a for i in range(1,7)),2)
            with self.assertRaises(ValueError):transition(t,'invented')
        original=copy.deepcopy(self.pop);a,b=[x['parameters'] for x in self.pop['agents'][:2]]
        for arm in ('U','G'):self.assertEqual(study.system(a,arm),study.system(b,arm))
        pe,be,se=study.profile_parts(study.system(a,'E'))
        pv,bv,sv=study.profile_parts(study.system(a,'V'))
        self.assertEqual((pe,se),(pv,sv));self.assertEqual(study.numeric_rows(be),study.prose_rows(bv))
        batch=study.schedule(self.pop);self.assertEqual(len(batch),137)
        self.assertEqual(len({j['slot'] for j in batch}),137)
        self.assertLessEqual(sum(j['reserved_nano'] for j in batch),study.CAP)
        self.assertEqual(original,self.pop)
        for j in batch[1:41]:
            packet=json.loads(j['request']['messages'][-1]['content'])
            self.assertEqual(set(packet),{'item_id','facts'})
            for forbidden in ('arm','profile','model','expected','check'):self.assertNotIn(forbidden,packet)

    def ratings(self):
        output={}
        for j in study.coding_jobs():
            packet=json.loads(j['request']['messages'][-1]['content']);value=fake_judgment(packet)
            output[j['judge'],j['item_id']]={'judgment':value,
                'summary':validate_judgment(value,j['item_id'],j['source_ids'],study.MANUAL)}
        return output

    def test_atomic_labels_and_polarity(self):
        from phase4_label_interface import normalize
        packet=card('disclosure_2','falsify');named=named_judgment(packet)
        value,summary=normalize(named,packet['item_id'],packet['facts'],study.MANUAL)
        self.assertEqual(value['fixed_standard'][0],0)
        self.assertEqual(value['configuration_relative'][1],1)
        self.assertEqual(summary['fixed_headline'],'not_good')
        bad=copy.deepcopy(named);bad['categories']['harm_avoidance']['label']='triggered'
        with self.assertRaises(ValueError):normalize(bad,packet['item_id'],packet['facts'],study.MANUAL)
        bad=copy.deepcopy(named);bad['configuration_relative']=[0]*8
        with self.assertRaises(ValueError):normalize(bad,packet['item_id'],packet['facts'],study.MANUAL)

    def test_measurement_gate_and_missingness(self):
        ratings=self.ratings();self.assertTrue(study.measurement_check(ratings)['passed'])
        changed=copy.deepcopy(ratings)
        changed[0,card('disclosure_12','report')['item_id']]['judgment']['configuration_relative'][2]=0
        self.assertFalse(study.measurement_check(changed)['passed'])
        changed=copy.deepcopy(ratings);changed.pop(next(iter(changed)))
        with self.assertRaises(BudgetStop):study.measurement_check(changed)
        rows=[{**j['cell'],'action':next(iter(task(j['cell']['task'])['actions']))} for j in study.participant_jobs(self.pop)]
        r=study.analyze(rows,ratings,6);self.assertEqual(r['valid'],96)
        self.assertTrue(all(v['estimate']==0 for v in r['contrasts'].values()))
        high=next(x for x in r['cells'] if x['task']=='disclosure_12' and x['arm']=='E')
        self.assertEqual(high['moral_rates']['0']['headlines']['relative']['not_good'],[1,1])
        self.assertEqual(high['fixed_good_rate_bounds']['union'],[1,1])
        rows[0]['action']=None;r=study.analyze(rows,ratings,6);self.assertEqual(r['valid'],95)
        target=next(c for c in r['cells'] if (c['task'],c['arm'])==(rows[0]['task'],rows[0]['arm']))
        self.assertLess(target['total_delta_identification_bounds'][0],target['total_delta_identification_bounds'][1])
        with self.assertRaises(BudgetStop):study.analyze(rows[:-1],ratings,6)
        with self.assertRaises(BudgetStop):study.analyze(rows+[rows[0]],ratings,6)
        for bad in ('{"choice":"A","choice":"B"}','{"choice":true}','{"choice":[]}','{"choice":"D"}'):
            self.assertIsNone(study.choice(bad,{'A':'report','B':'skip','C':'falsify'}))

    def fixture(self,tmp):
        root,folder=Path(tmp)/'ledger',Path(tmp)/'study'
        with zipfile.ZipFile(study.ROOT/read_checked(study.PARENT/'CHECKPOINT.json')['archive']) as z:z.extractall(root)
        release=read_checked(study.FOLDER/'release.json');pop=copy.deepcopy(self.pop)
        pop['agents']=pop['agents'][:1];pop['n_agents']=1;batch=study.schedule(pop)
        release['slots']={j['slot']:{**release['slots'][j['slot']],'request_sha256':digest(j['request'])} for j in batch}
        release['population_sha256']=digest(pop);release['jobs_sha256']=digest(batch)
        return root,folder,(release,pop,batch)

    def raw(self,req,text):
        if req['model']==study.JUDGE:
            return {'model':req['model'],'usage':{'input_tokens':100,'output_tokens':40},
                    'stop_reason':'end_turn','content':[{'type':'text','text':text}]}
        return {'model':req['model'],'usage':{'prompt_tokens':100,'completion_tokens':20},
                'choices':[{'finish_reason':'stop','message':{'content':text}}]}

    def test_extended_transport_keeps_provider_guards(self):
        for model in study.JUDGES:
            j=next(j for j in study.coding_jobs() if j['request']['model']==model)
            raw=self.raw(j['request'],'x'*4000)
            self.assertEqual(transport_parse(raw,j),'x'*4000)
            with self.assertRaises(ValueError):transport_parse(self.raw(j['request'],'x'*16385),j)
            bad=copy.deepcopy(raw);bad['model']='wrong-model'
            with self.assertRaises(ValueError):transport_parse(bad,j)
            bad=copy.deepcopy(raw)
            usage_key='output_tokens' if model==study.JUDGE else 'completion_tokens'
            bad['usage'][usage_key]=2049
            with self.assertRaises(ValueError):transport_parse(bad,j)
            bad=copy.deepcopy(raw)
            if model==study.JUDGE:bad['stop_reason']='max_tokens'
            else:bad['choices'][0]['finish_reason']='length'
            with self.assertRaises(ValueError):transport_parse(bad,j)

    def test_full_mock_replay_and_preservation(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root,folder,data=self.fixture(tmp);calls=[]
            def mock(req):
                calls.append(req)
                if len(calls)==1:text=json.dumps({'verdict':'accept','blocking_issues':[],'limits':[]})
                elif len(calls)<=41:text=json.dumps(named_judgment(json.loads(req['messages'][-1]['content'])))
                else:text='{"choice":"A"}'
                return self.raw(req,text)
            r=study.collect(root=root,folder=folder,responder=mock,test_data=data)
            self.assertEqual(r['decision'],'pilot_complete');self.assertEqual(r['valid'],16)
            self.assertEqual(len(calls),57)
            self.assertEqual(study.collect(True,root,folder,lambda _:self.fail('Replay call'),data),r)
            for name,expected in data[0]['preserved_files'].items():self.assertEqual(study.sha(root/name),expected)
            changed=copy.deepcopy(data);changed[2][-1]['request']['temperature']=0
            with self.assertRaises(BudgetStop):study.collect(root=root,folder=folder,responder=mock,test_data=changed)

    def test_review_and_measurement_stop(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root,folder,data=self.fixture(tmp);calls=[]
            def mock(req):
                calls.append(req)
                if len(calls)==1:text=json.dumps({'verdict':'accept','blocking_issues':[],'limits':[]})
                else:text='{"malformed":"rating"}'
                return self.raw(req,text)
            r=study.collect(root=root,folder=folder,responder=mock,test_data=data)
            self.assertEqual(r['decision'],'measurement_stop');self.assertEqual(len(calls),41)
            self.assertEqual(r['participant_calls'],0)
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root,folder,data=self.fixture(tmp);calls=[]
            def reject(req):
                calls.append(req);return self.raw(req,'{"verdict":"revise","blocking_issues":["Unclear"],"limits":[]}')
            r=study.collect(root=root,folder=folder,responder=reject,test_data=data)
            self.assertEqual(r['participant_calls'],0);self.assertEqual(len(calls),1)


if __name__=='__main__':unittest.main()
