import contextlib
import copy
import io
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import phase3_transfer_pilot as study
from phase3_budget import BudgetStop, digest, read_checked


class TransferPilot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=tuple(read_checked(study.FOLDER/f) for f in ('release.json','population.json','requests.json'))

    def test_design_and_interventions(self):
        release,pop,batch=self.data
        before=copy.deepcopy(pop)
        self.assertEqual(len(batch),449)
        self.assertLessEqual(release['recognition_cap_nano'],2_000_000_000)
        self.assertEqual(len({j['slot'] for j in batch}),449)
        self.assertEqual(study.fidelity(pop)['backgrounds'],8)
        self.assertEqual(pop,before)
        first,second=pop['agents'][0]['parameters'],pop['agents'][1]['parameters']
        self.assertEqual(study.system(first,None,'U'),study.system(second,None,'U'))
        self.assertEqual(study.system(first,.1,'S'),study.system(second,.1,'S'))
        self.assertNotEqual(study.system(first,.1,'E'),study.system(second,.1,'E'))
        for j in batch[1:]:
            req=j['request']
            self.assertLessEqual(sum(len(m['content'].encode()) for m in req['messages'])+1024,j['input_token_bound'])
            self.assertEqual(digest(req),release['slots'][j['slot']]['request_sha256'])
        for d in study.DOMAINS:
            for p in (0,1):
                for o in (0,1):
                    group=[j for j in batch[1:] if (j['cell']['domain'],j['cell']['procedure'],j['cell']['outcome'],j['cell']['arm'],j['cell']['pd'])==(d,p,o,'U',None)]
                    self.assertEqual(sum(j['cell']['support_label']=='A' for j in group),4)
        for p in (0,1):
            a=study.task('workshop',p,0)
            b=study.task('workshop',p,1)
            self.assertEqual(a.replace('net loss of 40','net gain of 40'),b)

    def test_scoring_and_known_tradeoff(self):
        cell={'support_label':'B'}
        self.assertEqual(study.action('{"choice":"B"}',cell),1)
        self.assertEqual(study.action('{"choice":"A"}',cell),0)
        for bad in ('{"choice":"A","choice":"B"}','{"choice":true}','{"choice":"B","why":"x"}','[]','{"choice":"C"}'):
            self.assertIsNone(study.action(bad,cell))
        rows=[]
        for j in self.data[2][1:]:
            c=j['cell']
            # High PD follows procedure; low PD follows outcome. T must equal 2.
            value=c['procedure'] if c['pd']==.9 else c['outcome']
            rows.append({**c,'value':value})
        result=study.analyze(rows,8)
        self.assertTrue(all(t['estimate']==2 for t in result['tradeoffs'].values()))
        with self.assertRaises(BudgetStop): study.analyze(rows[:-1],8)
        with self.assertRaises(BudgetStop): study.analyze(rows+[rows[0]],8)
        for r in rows:
            if (r['block'],r['domain'],r['procedure'],r['outcome'],r['arm'],r['pd'])==('1','workshop',1,0,'E',.9):
                r['value']=None
        missing=study.analyze(rows,8)['tradeoffs']['workshop/E']
        self.assertIsNone(missing['estimate'])
        self.assertEqual(missing['missing_blocks'],1)

    def fixture(self,tmp):
        root,folder=Path(tmp)/'ledger',Path(tmp)/'study'
        with zipfile.ZipFile(study.ROOT/read_checked(study.PARENT/'CHECKPOINT.json')['archive']) as saved:
            saved.extractall(root)
        release,pop,_=copy.deepcopy(self.data)
        pop['agents']=pop['agents'][:1]; pop['n_agents']=1
        batch=[study.review_job(pop)]+study.jobs(pop)
        release['slots']={j['slot']:{**release['slots'][j['slot']],'request_sha256':digest(j['request'])} for j in batch}
        release['population_sha256']=digest(pop); release['jobs_sha256']=digest(batch)
        return root,folder,(release,pop,batch)

    def response(self,req,text):
        if req['model']==study.JUDGE:
            return {'model':req['model'],'usage':{'input_tokens':100,'output_tokens':40},
                    'stop_reason':'end_turn','content':[{'type':'text','text':text}]}
        return {'model':req['model'],'usage':{'prompt_tokens':100,'completion_tokens':20},
                'choices':[{'finish_reason':'stop','message':{'content':text}}]}

    def test_full_mock_and_zero_call_replay(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root,folder,data=self.fixture(tmp); calls=[]
            def mock(req):
                calls.append(req)
                text='{"verdict":"accept","blocking_issues":[],"limits":[]}' if req['model']==study.JUDGE else '{"choice":"A"}'
                if len(calls)==2: text='{"choice":"invalid"}'
                return self.response(req,text)
            result=study.collect(root=root,folder=folder,responder=mock,test_data=data)
            self.assertEqual(len(calls),57)
            self.assertEqual(result['valid_responses'],55)
            self.assertEqual(study.collect(True,root,folder,lambda _:self.fail('Replay network'),data),result)
            for name,expected in data[0]['preserved_files'].items(): self.assertEqual(study.sha(root/name),expected)
            changed=copy.deepcopy(data); changed[2][1]['request']['temperature']=0
            with self.assertRaises(BudgetStop): study.collect(root=root,folder=folder,responder=mock,test_data=changed)

    def test_rejected_review_stops_before_participants(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root,folder,data=self.fixture(tmp); calls=[]
            def reject(req):
                calls.append(req)
                return self.response(req,'{"verdict":"revise","blocking_issues":["Ambiguous procedure"],"limits":[]}')
            result=study.collect(root=root,folder=folder,responder=reject,test_data=data)
            self.assertEqual(len(calls),1); self.assertEqual(result['participant_calls'],0)


if __name__=='__main__': unittest.main()
