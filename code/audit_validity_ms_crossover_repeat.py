"""Post-result audit of four repeated MS/S2 endpoint controls; no new calls."""
import ast
from hashlib import sha256
import json
import logging
from pathlib import Path
import pandas as pd
from scipy.stats import fisher_exact
import utils
import run_validity_ms_stanza_crossover as new
import run_validity_original_expanded as old
from run_validity_claude import save_new


def main():
    root = new.BASE / 'ms_stanza_crossover_20260912'
    previous = new.PREVIOUS
    nm, om = [json.loads((p/'manifest.json').read_bytes()) for p in (root, previous)]
    _, nr, _ = new.inventory(root,nm); _, orows, _ = old.inventory(previous,om)
    selected=[]; comparisons=[]
    for wording in new.WORDINGS:
        for value in (.1,.9):
            oc=next(c for c in om['design']['cells'] if (c['parameter'],c['wording'],c['value']) == ('MS',wording,value))
            nc=next(c for c in nm['design']['cells'] if (c['background'],c['ms_stanza'],c['value']) == (wording,wording,value))
            for k in ('messages','profile','labels','problem','value'):
                if oc[k] != nc[k]: raise ValueError('Repeated control mismatch: '+k)
            groups=[]
            for designation, rows, cell in ((previous.name,orows,oc),(root.name,nr,nc)):
                group=[r for r in rows if r['cell_id']==cell['id']]
                if len(group)!=20 or any(r['terminal_failure'] for r in group): raise ValueError('Incomplete control')
                for r in group:
                    if (r['model_version'] != new.base.MODEL or r['temperature'] != 1 or r['max_tokens'] != 600
                        or r['provider'] != 'openai' or r['attempts'] != 1): raise ValueError('Settings differ')
                    path=new.BASE/designation/'records'/(r['record_key']+'.json')
                    selected.append({'run':designation,'wording':wording,'value':value,'key':r['record_key'],
                        'sha256':sha256(path.read_bytes()).hexdigest(),'id':r['api_call_id'],'seed':r['seed'],
                        'decision':r['parsed_decision'],'timestamp_utc':r['timestamp_utc'],
                        'system_fingerprint':r['response_payload'].get('system_fingerprint'),
                        'service_tier':r['response_payload'].get('service_tier'),
                        'prompt_tokens':r['response_payload']['usage']['prompt_tokens']})
                k=sum(r['parsed_decision']=='FORMAL_REPORT' for r in group)
                groups.append({'adopt':k,'n_expected':20,'n_valid':20,'rate':k/20})
            a,b=groups
            comparisons.append({'wording':wording,'value':value,'old_count':a['adopt'],'new_count':b['adopt'],
                'new_minus_old':new.base.contrast([(b,1),(a,-1)]),
                'posthoc_two_sided_fisher_p':float(fisher_exact([[b['adopt'],20-b['adopt']],[a['adopt'],20-a['adopt']]]).pvalue),
                'exact_messages_profiles_labels_equal':True})
    if len({r['id'] for r in selected})!=160 or len({r['seed'] for r in selected})!=160:
        raise ValueError('Duplicate IDs or seeds across matched controls')
    for c,p in zip(comparisons,new.holm([c['posthoc_two_sided_fisher_p'] for c in comparisons])):
        c['posthoc_holm_four_p']=p
    def executor(module):
        tree=ast.parse(Path(module.__file__).read_text())
        return ast.dump(next(n for n in tree.body if isinstance(n,ast.AsyncFunctionDef) and n.name=='execute'))
    if executor(new)!=executor(old): raise ValueError('Executor source differs')
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(selected),
        'Post-result selection: prior640 ->80 matched controls; new160 ->80 matched controls; all160 retained, no validity exclusions',logging.getLogger('ms-repeat-audit'))
    result={'scope':'Post-result diagnostic, not a prespecified primary or pooled replication. Four matching endpoint controls.',
        'records_checked':160,'comparisons':comparisons,'records':selected,
        'executor_ast_identical':True,'same_sdk_client_class':new.base.SingleAttemptOpenAI is old.base.SingleAttemptOpenAI,
        'timestamps':{name:sorted(r['timestamp_utc'] for r in selected if r['run']==name)[::79] for name in (previous.name,root.name)},
        'limits':'Requested seeds, run times and interleaved allocation differ by design. Returned model identifier/settings and exact messages match; backend fingerprints unavailable. Does not identify the cause or prove backend drift.',
        'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    save_new(root/'analysis/repeat_audit.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))


if __name__=='__main__': main()
