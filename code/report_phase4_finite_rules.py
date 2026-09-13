"""Independent offline accounting, raw-choice and arithmetic report checks."""
from collections import Counter
import json
import math
from pathlib import Path

from phase3_budget import digest,read_checked
from phase3_variant_round import save

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'experiments/phase4_coding/consequence_rule_pilot_r1'


def report():
    result=read_checked(FOLDER/'results.json');check=read_checked(FOLDER/'CHECKPOINT.json')
    assert result['accounted_nano']==check['study_accounted_nano']
    assert check['provider_totals_nano']==result['provider_totals_nano']
    assert sum(result['provider_totals_nano'].values())==check['allocation_accounted_nano']
    assert check['allocation_accounted_nano']+22906073025==check['package_accounted_nano']
    assert check['total_paid_records']==2338+result['calls']
    assert check['new_calls_during_verification']==0
    output={'status':'pass','new_api_calls':0,'integer_accounting_verified':True,
        'results_sha256':digest(result),'checkpoint_sha256':digest(check)}
    if result['decision']=='pilot_complete':
        analysis=read_checked(FOLDER/'analysis.json');rows=analysis['rows']
        jobs=read_checked(FOLDER/'requests.json');indexed={(r['block'],r['task'],r['arm']):r for r in rows}
        assert len(rows)==len(indexed)==result['participant_calls']==96
        for j in jobs[1:]:
            raw=read_checked(ROOT/'data/raw/phase3_20260913_budget/records'/(digest(j['slot'])+'.json'))
            row=indexed[j['cell']['block'],j['cell']['task'],j['cell']['arm']]
            try:
                pairs=json.loads(raw['parsed'],object_pairs_hook=lambda x:x)
                action=j['cell']['mapping'][pairs[0][1]] if len(pairs)==1 and pairs[0][0]=='choice' else None
            except (ValueError,TypeError,KeyError,IndexError):action=None
            assert action==row['action']
            if action is None:assert row['outcome'] is None;continue
            o=row['outcome'];e=o['effects'];r=o['configuration_relative'];f=o['fixed_standard'];h=o['headlines']
            assert e['actor_delta']+sum(e['third_party_deltas'])==e['total_delta']
            assert h['fixed_headline']==('good' if all(f) else 'not_good')
            assert h['relative_headline']==('not_good' if any(r[:4]) else 'good' if any(r[4:]) else 'neutral')
            assert h['net_score_bounds']==[sum(r[4:])-sum(r[:4])]*2
            assert h['weighted_score_bounds']==[sum(r[4:])-1.5*sum(r[:4])]*2
        assert sum(r['action'] is not None for r in rows)==analysis['valid']==result['valid']
        lines=['# Finite-rule pilot: descriptive results','',
            'Six assigned choices per task/arm. E: numeric profile; V: equivalent written percentages;',
            'U: no profile; G: no profile plus ethical guidance. Credits are simulated units.',
            'Good/not_good labels follow stipulated standards. They are not human moral judgments.',
            'Bounds below identify the assigned mean if choices are missing; they are not confidence intervals.','',
            '| Task / arm | Action counts | Valid | Actor mean | Recipient means | Total mean | Fixed-good bounds | Relative-good bounds |',
            '|---|---|---:|---:|---|---:|---|---|']
        cells={}
        for c in analysis['cells']:
            selected=[r for r in rows if (r['task'],r['arm'])==(c['task'],c['arm'])]
            valid=[r['outcome'] for r in selected if r['outcome'] is not None]
            assert len(selected)==6 and len(valid)==c['valid']
            counts=Counter(v['action'] for v in valid)
            assert all(counts[k]==v for k,v in c['action_counts'].items())
            for field in ('actor_delta','total_delta','completed'):
                expected=sum(v['effects'][field] for v in valid)/len(valid) if valid else None
                actual=c[field+'_available_mean']
                assert expected==actual or math.isclose(expected,actual,abs_tol=1e-12)
            for method in ('relative','fixed','net','weighted'):
                if len(valid)==6:
                    for label,b in c['headline_rate_bounds'][method].items():
                        expected=sum(v['headlines'][method+'_possible']==[label] for v in valid)/6
                        assert b==[expected,expected]
            cells[c['task'],c['arm']]=c
            lines.append('| '+c['task']+' / '+c['arm']+' | '+', '.join(f'{k}: {v}' for k,v in c['action_counts'].items())+
                f' | {c["valid"]} | {c["actor_delta_available_mean"]} | {c["third_party_available_means"]} | '+
                f'{c["total_delta_available_mean"]} | {c["headline_rate_bounds"]["fixed"]["good"]} | '+
                f'{c["headline_rate_bounds"]["relative"]["good"]} |')
        lines+=['','## All planned paired contrasts','',
            'Bootstrap intervals use only six blocks and are conditional on these four tasks and rules.',
            'Degenerate bootstrap intervals do not establish certainty; conservative bounds are also shown.',
            'All category and aggregation rates, including not_good and neutral, remain in analysis.json.','',
            '| Task / contrast | Metric | Estimate | Bootstrap 95% | Hoeffding 95% |',
            '|---|---|---:|---|---|']
        for key,pair in analysis['contrasts'].items():
            t,arms=key.split('/');left,right=arms.split('-')
            for metric,v in pair.items():
                if v['missing_blocks']==0:
                    getter=(lambda c:c['total_delta_available_mean']) if metric=='total_credits' else (lambda c:c['headline_rate_bounds']['fixed']['good'][0])
                    assert math.isclose(v['estimate'],getter(cells[t,left])-getter(cells[t,right]),abs_tol=1e-12)
                lines.append(f'| {key} | {metric} | {v["estimate"]} | {v["bootstrap_95_interval"]} | {v["hoeffding_95_interval"]} |')
        content='\n'.join(lines)+'\n';p=FOLDER/'TABLES.md'
        if p.exists():assert p.read_text(encoding='utf-8')==content
        else:p.write_bytes(content.encode('utf-8'))
        output.update(raw_choices_checked=96,cell_rows_checked=16,paired_metric_contrasts_checked=32,
            valid_participant_decisions=analysis['valid'],analysis_sha256=digest(analysis))
    save(FOLDER/'REPORT_CHECKS.json',output)
    return output


if __name__=='__main__':print(json.dumps(report()))
