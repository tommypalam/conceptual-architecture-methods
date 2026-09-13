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
import phase3_context_diagnostic_r2 as study
from phase3_budget import BudgetStop, digest, read_checked


class Diagnostic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=study.FOLDER/'release.json'
        cls.data = tuple(read_checked(study.FOLDER/f) for f in ('release.json','population.json','requests.json')) if path.exists() else study.prepare()

    def fixture(self,tmp):
        root,folder=Path(tmp)/'ledger',Path(tmp)/'study'
        with zipfile.ZipFile(study.ROOT/read_checked(study.PARENT/'CHECKPOINT.json')['archive']) as z: z.extractall(root)
        release,pop,batch=copy.deepcopy(self.data)
        pop['agents']=pop['agents'][:2]; pop['n_agents']=2
        batch=[study.review_job(pop)]+study.jobs(pop)
        slots={j['slot'] for j in batch}
        release['slots']={k:v for k,v in release['slots'].items() if k in slots}
        release['slots'][batch[0]['slot']]['request_sha256']=digest(batch[0]['request'])
        release['population_sha256']=digest(pop); release['jobs_sha256']=digest(batch)
        return root,folder,tuple(json.loads(study.canonical(x)) for x in (release,pop,batch))

    def response(self,req,text):
        if req['model']==study.JUDGE:
            return {'model':req['model'],'usage':{'input_tokens':100,'output_tokens':20},
                    'stop_reason':'end_turn','content':[{'type':'text','text':text}]}
        return {'model':req['model'],'usage':{'prompt_tokens':100,'completion_tokens':20},
                'choices':[{'finish_reason':'stop','message':{'content':text}}]}

    def test_full_frozen_schedule_pairing_and_bounds(self):
        release,pop,batch=self.data
        self.assertEqual(len(batch),577)
        saved_pop=json.loads(study.canonical(pop))
        saved_batch=json.loads(study.canonical(batch))
        self.assertEqual(saved_batch,[study.review_job(saved_pop)]+study.jobs(saved_pop))
        self.assertLessEqual(release['recognition_cap_nano'],study.CAP)
        self.assertEqual(len({j['slot'] for j in batch}),577)
        for j in batch[1:]:
            self.assertEqual(len(j['request']['messages']),2)
            self.assertEqual(j['request']['max_completion_tokens'],64)
            self.assertIn('JSON object',j['request']['messages'][0]['content'])
            self.assertEqual(digest(j['request']),release['slots'][j['slot']]['request_sha256'])
        a=pop['agents'][0]['parameters']; b=pop['agents'][1]['parameters']
        self.assertEqual(study.system(a,0,'U'),study.system(b,0,'U'))
        self.assertNotEqual(study.system(a,0,'E'),study.system(b,0,'E'))
        self.assertNotIn('decision-making profile',study.system(a,0,'U'))
        self.assertIn('Justice:   LOW',study.system(a,0,'E'))
        self.assertIn('Justice:   HIGH',study.system(a,1,'E'))

    def test_full_mock_invalid_action_replay_and_preservation(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root,folder,data=self.fixture(tmp); calls=[]
            def mock(req):
                calls.append(req)
                if req['model']==study.JUDGE: text='```json\n{"verdict":"accept","blocking_issues":[],"limits":[]}\n```'
                elif len(calls)==2: text='{"action":"maybe"}'
                elif 'proposer. Return' in req['messages'][-1]['content']: text='{"offer_to_other":40}'
                else: text='{"action":"reject"}'
                return self.response(req,text)
            result=study.collect(root=root,folder=folder,test_data=data,responder=mock)
            self.assertEqual(len(calls),49)
            self.assertEqual(result['invalid_actions'],1)
            self.assertIsNone(result['phase3_pass'])
            self.assertEqual(study.collect(True,root=root,folder=folder,test_data=data,responder=lambda _:self.fail('Network in replay')),result)
            for name,expected in data[0]['preserved_files'].items(): self.assertEqual(study.sha(root/name),expected)
            bad=copy.deepcopy(data); bad[2][1]['request']['temperature']=0
            with self.assertRaises(BudgetStop): study.collect(root=root,folder=folder,test_data=bad,responder=lambda _:self.fail('Changed request dispatched'))

    def test_review_stop_and_transport_failure_no_retry(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root,folder,data=self.fixture(tmp)
            result=study.collect(root=root,folder=folder,test_data=data,responder=lambda req:self.response(req,'{"verdict":"revise","blocking_issues":["Synthetic issue"],"limits":[]}'))
            self.assertEqual(result['calls'],1); self.assertEqual(result['participant_calls'],0)
        with tempfile.TemporaryDirectory() as tmp:
            root,folder,data=self.fixture(tmp)
            def fail(_): raise TimeoutError()
            with self.assertRaises(BudgetStop): study.collect(root=root,folder=folder,test_data=data,responder=fail)
            with self.assertRaises(BudgetStop): study.collect(root=root,folder=folder,test_data=data,responder=lambda _:self.fail('Retry'))

    def test_exact_scoring_missingness_and_interaction(self):
        cell={'role':'proposer'}
        for text in ('{"offer_to_other":true}','{"offer_to_other":3.5}','{"offer_to_other":101}',
                     '{"offer_to_other":10,"offer_to_other":20}','```json\n{"offer_to_other":10}\n```'):
            self.assertIsNone(study.action(text,cell))
        self.assertEqual(study.action('{"offer_to_other":0}',cell),0)
        self.assertEqual(study.action('{"offer_to_other":100}',cell),1)
        self.assertIsNone(study.action('{"action":"accept","reason":"x"}',{'role':'responder'}))
        effect=study.contrast([[1,1],[0,0],[0,0],[1,1]],[1,-1,-1,1],1)
        self.assertEqual(effect['estimate'],2)
        self.assertEqual(effect['identification_interval'],[2,2])
        self.assertTrue(effect['bootstrap_degenerate'])
        self.assertLess(effect['hoeffding_95_interval'][0],2)
        missing=study.contrast([[None],[None],[None],[None]],[1,-1,-1,1],1)
        self.assertEqual(missing['identification_interval'],[-2,2]); self.assertIsNone(missing['estimate'])
        rows=[]
        for block in ('1','2'):
            for c in (0,1):
                for arm in ('E','U'):
                    for role,offer in study.TASKS:
                        rows.append({'block':block,'context':c,'arm':arm,'role':role,'offer':offer,'value':int(c==0 and arm=='E')})
        result=study.analyze(rows,2)
        self.assertEqual(result['primary']['interaction']['estimate'],1)
        self.assertEqual(sum(x['nonmonotone'] for x in result['monotonicity']),0)
        with self.assertRaises(BudgetStop): study.analyze(rows[:-1],2)
        with self.assertRaises(BudgetStop): study.analyze(rows+[rows[0]],2)


if __name__=='__main__': unittest.main()
