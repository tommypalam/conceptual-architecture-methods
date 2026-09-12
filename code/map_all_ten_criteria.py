"""Map every parameter to the three agreed evidence categories; no API calls."""
from hashlib import sha256
import json
import logging
from pathlib import Path
import pandas as pd
import utils
from run_validity_claude import save_new

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'experiments/phase1_5_encoding_validity'
DEST=BASE/'all_ten_criteria_20260912'
SOURCES={
    'historical':BASE/'fixed_encoding_assessment_20260911/evidence_matrix.json',
    'sweep':BASE/'structural_encoding_20260912/sweep/analysis/result_f87bac164d8bfc5d.json',
    'exact':BASE/'structural_encoding_20260912/sweep/analysis/discrete_uncertainty_sensitivity.json',
    'diagnostics':BASE/'structural_encoding_20260912/diagnostics/analysis/result_313c5ea5a071ca14.json',
    'audit':BASE/'structural_encoding_20260912/audit_schema_r3/analysis/prevalence_summary.json',
    'confirmation':BASE/'structural_encoding_20260912/pd_confirmation/analysis/result_12d9e5a5cda25ae3.json',
}


def build(sources):
    old=sources['historical']['rows'];sweep=sources['sweep']['groups']
    audit=sources['audit']['parameters'];diag=sources['diagnostics']['groups']
    expected={(p,s) for p in utils.PARAM_NAMES for s in ('S1','S2','S3')}
    if len(old)!=30 or {(r['parameter'],r['problem']) for r in old}!=expected:raise ValueError('Historical coverage mismatch')
    if len(sweep)!=30 or {(r['parameter'],r['problem']) for r in sweep}!=expected:raise ValueError('Fresh coverage mismatch')
    if len(audit)!=10 or {r['parameter'] for r in audit}!=set(utils.PARAM_NAMES):raise ValueError('Audit coverage mismatch')
    rows=[]
    for p in utils.PARAM_NAMES:
        historical=[r for r in old if r['parameter']==p]
        current=[r for r in sweep if r['parameter']==p]
        coding=next(r for r in audit if r['parameter']==p)
        eligible=[r for r in historical if r['numeric_only']['eligible_from_source']]
        row={
            'parameter':p,'fresh_sweep_problems':[r['problem'] for r in current],
            'fresh_n_per_level':20,'fresh_levels':[.1,.3,.5,.7,.9],
            'original_directional_problems':[r['problem'] for r in historical if r['prespecified_direction'] is not None],
            'historical_full_gradient_criterion_met':[r['problem'] for r in historical if r['canonical_criterion']=='met'],
            'fresh_bootstrap_predicted_endpoint_flags':[r['problem'] for r in current if r['predicted_endpoint_supported']],
            'fresh_exact_endpoint_signals':[{'problem':r['problem'],'effect':r['effect'],'p_holm':r['p_holm']} for r in sources['exact']['comparisons'] if r['parameter']==p and r['contrast']=='endpoint' and r['p_holm']<.05],
            'historical_paraphrase_equivalent_problems':[r['problem'] for r in historical if r['paraphrase_all_pairs_equivalent']],
            'historical_retention_eligible_problems':[r['problem'] for r in eligible],
            'historical_numeric_retention_met':[r['problem'] for r in eligible if r['numeric_only']['criterion_met']],
            'historical_verbal_retention_met':[r['problem'] for r in eligible if r['verbal_only']['criterion_met']],
            'fresh_six_representation_diagnostic_problems':sorted({r['problem'] for r in diag if r['parameter']==p}),
            'fresh_representation_gaps':[s for s in ('S1','S2','S3') if not any(r['parameter']==p and r['problem']==s for r in diag)],
            'fresh_audit_active_n':20,'fresh_audit_accuracy':coding['active_accuracy'],
            'fresh_audit_balanced_accuracy':coding['active_balanced_accuracy'],
            'fresh_audit_p_holm_supplement':coding['active_p_holm_supplement'],
            'fresh_audit_all_accuracy':coding['all_accuracy'],
            'fresh_audit_all_majority_baseline':coding['all_majority_baseline'],
            'independent_endpoint_confirmation':sources['confirmation']['groups'] if p=='PD' else [],
            'all_three_categories_established':False,
        }
        # This is coverage and existing-evidence reporting, not a new pass rule.
        rows.append(row)
    return rows


def main():
    sources={k:json.loads(p.read_bytes()) for k,p in SOURCES.items()};rows=build(sources)
    logging.basicConfig(level=logging.INFO)
    utils.log_dataframe_summary(pd.DataFrame(rows),'All ten parameters retained; no pooled observations or exclusions',logging.getLogger('coverage'))
    result={'scope':'All ten parameters; three researcher-confirmed evidence categories retain four original tests.',
        'new_API_calls':0,'no_new_composite_pass_rule':True,
        'historical_and_fresh_not_pooled':True,'historical_summary_join_not_new_raw_reaudit':True,
        'source_sha256':{p.relative_to(ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in SOURCES.values()},
        'rows':rows}
    save_new(DEST/'coverage.json',result)
    fmt=lambda xs:', '.join(xs) if xs else 'None established'
    lines=['# All ten parameters, all three evidence categories','',
        'Scope confirmed by the researcher on 2026-09-12. Category1: causal and graded decision effects (thesis8.1.1). Category2: wording robustness (8.1.3) plus numeric/verbal retention (8.1.4), kept as separate tests. Category3: blind explanation recovery (8.1.2). No threshold changes or new combined gate.',
        '', '**All ten were tested in the historical battery. All ten also have fresh canonical sweeps and fresh audit results. Fresh six-representation diagnostics cover only MoR/S3 and MS/S2. No parameter currently establishes the complete set.**',
        '', 'Historical tests use fixed-background designs; recent canonical sweeps vary the other nine coordinates across20 backgrounds. Historical paraphrase results concern fixed .8 rotations, not full fresh-profile curves. Results are displayed alongside one another, never pooled or treated as interchangeable replications.',
        '', '| Parameter | Historical full gradient criterion | Fresh endpoint evidence | Historical paraphrase equivalence /3 dilemmas | Historical numeric / verbal retention | Fresh six-representation diagnostics | Fresh active audit correct /20; supplementary Holm p |',
        '|---|---|---|---|---|---|---|']
    for r in rows:
        fresh='; '.join([('bootstrap flag '+fmt(r['fresh_bootstrap_predicted_endpoint_flags'])) if r['fresh_bootstrap_predicted_endpoint_flags'] else '',('exact '+fmt([x['problem'] for x in r['fresh_exact_endpoint_signals']])) if r['fresh_exact_endpoint_signals'] else '']).strip('; ')
        if not fresh:fresh='None established'
        if r['parameter']=='MoR':fresh+='; exact sensitivity does not confirm'
        if r['parameter']=='PD':fresh+='; both independently confirmed'
        retention=(fmt(r['historical_numeric_retention_met'])+' / '+fmt(r['historical_verbal_retention_met'])) if r['historical_retention_eligible_problems'] else 'Not eligible under original rule'
        historical=fmt(r['historical_full_gradient_criterion_met']) if r['original_directional_problems'] else 'No original directional hypothesis'
        diagnostics=fmt(r['fresh_six_representation_diagnostic_problems']) if r['fresh_six_representation_diagnostic_problems'] else 'Not collected'
        lines.append(f"| {r['parameter']} | {historical} | {fresh} | {len(r['historical_paraphrase_equivalent_problems'])}/3 ({fmt(r['historical_paraphrase_equivalent_problems'])}) | {retention} | {diagnostics} | {round(20*r['fresh_audit_accuracy'])}/20; {r['fresh_audit_p_holm_supplement']:.3f} |")
    lines+=['', 'Fresh sweep coverage is identical for every parameter: S1/S2/S3 at .1/.3/.5/.7/.9,20 backgrounds per condition. Endpoint flags alone are not full graded-response passes. Lack of significance is not proof of no effect; near-ceiling S1 responses limit identification. LL/CS/AW have no original simple-dilemma directional hypotheses, so inventing signs or counting missing predictions as failed tests would be incorrect.',
        '', 'All ten have20 active audit items across the three dilemmas, not20 per dilemma. Permutation p-values are the existing problem-stratified diagnostics with supplementary Holm10; repeated-background dependence and self-explanation limitations remain. Aggregate accuracy is compared to the observed majority baseline in the JSON. PD is the only fresh active signal surviving that correction; this does not pass the aggregate audit.',
        '', 'Equivalence needs a sufficiently narrow interval inside the unchanged +/-0.10 margin. Non-significance does not establish robustness. Historical retention is conditional on an eligible canonical gradient; every numeric/verbal curve was collected, but ineligible comparisons cannot be promoted to passes.',
        '', '## Follow-up scope',
        '', 'Keep all ten parameters and all three locked dilemmas. Assess the four component tests separately, then report the three agreed categories for each parameter. Use canonical plus all three approved paraphrases, numeric-only and verbal-only; retain current model, definitions, endpoints, Beta/R and locked questions. Freeze sample size, exact comparisons, multiplicity treatment and budget before new collection. Any per-parameter directional hypothesis absent from the original theory must remain exploratory unless prospectively specified and justified.',
        '', 'A full20-background, five-level, six-representation fresh screen would use18,000 behavioral calls. Applying the existing exact reservation formula to the completed20 backgrounds gives $111.662258 before coding, with a rough usage extrapolation of $19.512009. Those are planning estimates, not new frozen requests or authorization. A new draw changes verbal prompt lengths slightly. That N would still be inadequate for strong +/-0.10 equivalence claims near balanced decision rates; do not label it a gate-clearing study.',
        '', 'The existing [precision diagnosis](../offline_diagnosis_20260909/FINDINGS_AND_NEXT_STEP.md) simulated four truly equivalent balanced formulations: all-pair equivalence succeeded in 0/10,000 repetitions at N=50, about35% at N=400 and about91% at N=800 per formulation. These simulations are planning evidence under equal true rates, not predictions of empirical wording equivalence. Increasing N cannot cure a real wording discrepancy.',
        '', 'The researcher has been asked for the additional spending envelope before a new design is frozen. No new calls have been dispatched. Existing studies stay immutable; this table is an offline assessment, not a new experiment.',
        '', '[Machine-readable coverage](coverage.json) | [Completed structural assessment](../structural_encoding_20260912/FINAL_ASSESSMENT.md) | [Original evidence map](../fixed_encoding_assessment_20260911/EVIDENCE_MAP.md)','']
    (DEST/'COVERAGE.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'parameters':len(rows),'fresh_representation_parameter_problem_gaps':sum(len(r['fresh_representation_gaps']) for r in rows),'new_API_calls':0}))


if __name__=='__main__':main()
