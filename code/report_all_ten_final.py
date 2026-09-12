"""Offline reporting of frozen all-ten results; no model calls or gate revisions."""
import json
import logging
from hashlib import sha256
from pathlib import Path
import pandas as pd
import run_all_ten_segment3 as run

ROOT=run.old.BASE/'all_ten_assessment_20260912'


def main():
    logging.basicConfig(level=logging.INFO)
    source=next((run.ROOT/'analysis').glob('result_*.json'))
    result=json.loads(source.read_bytes())
    ledger=json.loads((run.ROOT/'budget_ledger.json').read_bytes())
    audit_path=run.old.PACKAGE/'audit_schema_r3/analysis/prevalence_summary.json'
    audit=json.loads(audit_path.read_bytes())['parameters']
    verification=json.loads((run.ROOT/'analysis/verification.json').read_bytes())
    assert sha256(source.read_bytes()).hexdigest()==verification['result_sha256']
    assert result['n_records']==ledger['n_records']==17247
    assert ledger['n_dispatched']==17250 and ledger['pending_requests']==3 and ledger['never_dispatched']==0
    archive_checks=[]
    for root in (*run.PARENTS,run.ROOT):
        backup=json.loads((root/'local_backup.json').read_bytes())
        assert sha256(Path(backup['path']).read_bytes()).hexdigest()==backup['sha256']
        archive_checks.append({'segment':root.name,'archive_sha256':backup['sha256']})
    sens=result['gradient_sensitivity'];exact=sens['exact_paired_180_comparisons']
    retention=sens['representation_retention_diagnostic'];word=result['wording_analysis']
    signals=[dict(x) for x in exact if x['complete_pairs'] and x['p_holm']<.05]
    for x in signals:
        # Added after collection for readable effect uncertainty, not a new test.
        effects=[1]*x['positive_pairs']+[-1]*x['negative_pairs']+[0]*(25-x['positive_pairs']-x['negative_pairs'])
        x['pointwise_ci95_supplement']=run.original.paired_interval(effects,alpha=.05)['ci90_conservative']
    params=['LL','CS','RT','MoR','RE','PD','TfA','ID','MS','AW'];coverage=[]
    for p in params:
        words=[w for w in word if w['parameter']==p]
        a=next(a for a in audit if a['parameter']==p)
        coverage.append({'parameter':p,'canonical_paired_signals':'; '.join(f"{x['problem']} {x['contrast']} {x['effect']:+.2f}" for x in signals if x['parameter']==p and x['variant']=='canonical') or 'None established',
            'other_representation_signals':'; '.join(f"{x['variant']} {x['problem']} {x['contrast']} {x['effect']:+.2f}" for x in signals if x['parameter']==p and x['variant']!='canonical') or 'None established',
            'wording_complete':sum(w['complete'] for w in words),'wording_equivalent':sum(w['all_pairs_equivalent'] for w in words),
            'active_audit_accuracy':a['active_accuracy'],'active_audit_holm_p':a['active_p_holm_supplement']})
    run.old.utils.log_dataframe_summary(pd.DataFrame(coverage),'All ten parameters retained; no parameter filtering',logging.getLogger('report'))
    run.old.utils.log_dataframe_summary(pd.DataFrame(signals),'180 contrasts -> 8 Holm-significant complete contrasts; all 180 remain in source; 8 incomplete assigned p=1',logging.getLogger('report'))
    independent=sum(w['complete'] and all(p['original_independent_TOST_sensitivity']['equivalent'] for p in w['pairs']) for w in word)
    summary={'source_sha256':sha256(source.read_bytes()).hexdigest(),'ledger':ledger,'all_ten':coverage,
        'significant_paired_contrasts':signals,'complete_paired_contrasts':sum(x['complete_pairs'] for x in exact),
        'wording_equivalent':sum(w['all_pairs_equivalent'] for w in word),'wording_complete':sum(w['complete'] for w in word),
        'independent_wording_sensitivity_equivalent':independent,
        'retention_eligible':sum(x['assessment']=='eligible' for x in retention),
        'retention_passed':sum(x['assessment']=='eligible' and x['criterion_met'] for x in retention),
        'archive_checks':archive_checks,'original_gate_passed':False}
    lines=['# All-ten encoding follow-up: final assessment','',
        '**The dispatch allocation is complete. Evidence supports local, delivery-dependent parameter effects; the full encoding-validity gate remains unmet. Phase 1.5 stays open and Phase 2 remains held.**','',
        'All 17,250 planned requests were dispatched across three execution segments. There are 17,247 saved records: 17,234 valid, ten parse failures, three recorded API failures, plus three further dispatched requests with no saved response. Nothing was retried or replaced. There are no never-dispatched slots.',
        f"Total accounted cost: **${ledger['total_accounted_usd']:.6f} / $25**, including ${ledger['unknown_followup_reserved_usd']:.8f} follow-up unknown bounds and the prior package. No provider-balance or off-device-backup claim.",
        '', '## Design and coverage','',
        'Neutral configuration; 50 unselected backgrounds sampled from the original Beta/Gaussian copula. First 25 backgrounds for 10 parameters × 3 dilemmas × 5 levels × canonical/numeric-only/verbal-only (11,250 requests); all 50 for 10 × 3 × canonical/three approved paraphrases at .8 (6,000 requests). One response per condition. Draw/schedule/analysis seeds 20261020/20261021/20261022; pinned gpt-5.4-mini-2026-03-17, temperature 1, max 600. Recovery is the separate completed prior-cohort 200-item audit, not a new audit of this cohort.',
        '', '## Causal and graded effects','',
        'The frozen global bootstrap assessment reports INCOMPLETE_OR_INVALID because missing or invalid slots prevent its complete-data primary analysis. This is a data-completeness result, not a demonstration of zero effects. The prespecified supplementary exact paired analysis retains all 180 endpoint/interior contrasts in Holm correction; 172 are complete, eight incomplete contrasts receive p=1, and eight complete contrasts survive correction.',
        '', '| Parameter / dilemma | Representation | Contrast | Change in first-option probability | Supplementary pointwise 95% CI | Holm180 p |','|---|---|---|---:|---|---:|']
    for x in signals:
        lo,hi=x['pointwise_ci95_supplement']
        lines.append(f"| {x['parameter']} / {x['problem']} | {x['variant']} | {x['contrast']} | {x['effect']:+.0%} | [{lo:+.1%}, {hi:+.1%}] | {x['p_holm']:.6f} |")
    lines+=['', 'First options are the frozen problem labels: S2 FORMAL_REPORT and S3 ADOPT. Thus a negative S3 contrast means a shift toward WAIT. Endpoint means .9 minus .1; interior means .7 minus .3. Each complete contrast pairs 25 backgrounds. The supplementary pointwise conservative 95% intervals were added after collection for reporting: exact binomial bounds on positive and negative discordances, using the existing interval helper with alpha=.05. They are not simultaneous intervals, do not replace the unavailable primary bootstrap, and do not determine the Holm-significance flags.',
        '', '**PD:** canonical reporting on S2 rises 4% → 4% → 16% → 40% → 68%; canonical ADOPT on S3 falls 100% → 80% → 64% → 40% → 32%. Both endpoint effects survive Holm180. Verbal PD has significant endpoint and interior effects on both dilemmas. This extends the earlier local PD evidence to a second delivery form. These PD/simple-task signs were exploratory in the original theory matrix; the previous separately frozen PD confirmation remains distinct evidence.',
        '', '**MoR:** canonical S3 ADOPT rises 32% → 48% → 60% → 76% → 84%, with a Holm-significant endpoint. Canonical interior does not survive Holm180. The ordered observed curve is encouraging but does not independently establish the full validity battery.',
        '', '**Counterevidence:** numeric-only RT/S3 decreases ADOPT by 56pp, opposite to the original positive directional prediction. Do not count any significant influence as correct encoding. MS/S2 canonical rates 16% → 20% → 12% → 28% → 32% remain non-ordered; no MS contrast survives Holm180. Lack of a significant contrast for other parameters is not proof of no effect.',
        '', '## Representation and wording robustness','',
        'Only MoR/S3 meets the original canonical eligibility rule in the legacy comparability diagnostic. Its numeric-only slope retains 15.6% of canonical magnitude; verbal-only retains 42.3%. **Both eligible retention tests fail (0/2).** These grouped-binomial fits treat repeated backgrounds as independent; they are diagnostics, with the exact paired sensitivity retained separately.',
        '', 'PD has useful verbal effects, but no formal original-rule retention pass is assigned to PD/S2 or PD/S3: those cells lack original directional predictions and are ineligible in that rule. Descriptively, verbal slopes retain 68.5% (S2) and97.3% (S3) of canonical magnitude; numeric slopes retain 4.6% and47.9%. Do not turn ineligibility into a negative empirical finding or relabel these ratios as passes.',
        '', '**Wording equivalence: 1/30 cells establishes all-six-pair equivalence (CS/S1).** Twenty-five cells are complete; 24 complete cells do not establish equivalence, and five are incomplete (RE/S1, RE/S2, PD/S2, PD/S3, TfA/S1). The original independent-binomial TOST sensitivity establishes 3/30 (LL/S1, CS/S1, PD/S1). Neither calculation supports a broad robustness claim.',
        '', 'Failure to establish equivalence is not proof of non-equivalence. N=50 and the conservative paired interval limit precision. These comparisons estimate average wording differences over sampled profiles at .8; they are not the original fixed-mean battery, so the historical 8/30 and this 1/30 should not be presented as a direct improvement/worsening comparison. Near-ceiling S1 agreement is a weak discriminator of encoding.',
        '', '## All ten parameters and separate recovery evidence','',
        '| Parameter | Canonical paired signals | Other representation paired signals | Wording equivalent / complete cells (of3) | Prior active-audit accuracy | Prior audit Holm10 p |','|---|---|---|---|---:|---:|']
    for x in coverage:
        lines.append(f"| {x['parameter']} | {x['canonical_paired_signals']} | {x['other_representation_signals']} | {x['wording_equivalent']} / {x['wording_complete']} | {x['active_audit_accuracy']:.0%} | {x['active_audit_holm_p']:.3f} |")
    lines+=['', 'The existing audit still fails its literal aggregate gate. PD is the only active-trait result surviving the supplementary Holm10 check (11/20, 55%, p=.03). Short self-explanations and repeated-background dependence limit interpretation; explanations do not establish an internal moral mechanism. No other parameter is removed from reporting.',
        '', '## Defensible claim and decision','',
        'Under the tested model, harness and dilemmas, explicit normative profile inputs can produce systematic, context-dependent changes in raw decisions. PD provides the clearest normative case, with canonical and verbal effects. The experiment does not establish that all ten parameters are robustly encoded, that effects are independent of wording or representation, or that the model has intrinsic ethical understanding. It provides evidence about conditional agent behavior, not AGI.',
        '', 'No threshold, prompt, theory, Beta marginal, correlation or phase-release rule is changed. The original gate remains unmet. All requests are dispatched and no further paid run is queued.',
        '', 'Synthetic review: Linden limits the claim to operational normative inputs; Osei retains incomplete slots and independent-cohort boundaries; Tanaka keeps Holm180 and labels added intervals and legacy fits correctly; Renna treats cross-form PD agreement as local evidence while retaining RT counterevidence; Okafor requires saved provenance and no silent retries. The tension is promising local evidence versus broad delivery robustness. Resolution: preserve both findings and keep Phase 1.5 open, without calling the whole architecture validated. These are synthetic roles, not external expert review.',
        '', '[Frozen full result](../all_ten_followup_20260912_segment3/analysis/'+source.name+') | [Execution status](../all_ten_followup_20260912_segment3/STATUS.md) | [Original follow-up protocol](../all_ten_followup_20260912/PROTOCOL.md) | [Prior audit](../structural_encoding_20260912/audit_schema_r3/analysis/REPORT.md)','']
    ROOT.mkdir(exist_ok=True)
    run.save_new(ROOT/'summary.json',summary)
    (ROOT/'ASSESSMENT.md').write_text('\n'.join(lines),encoding='utf-8')
    run.save_new(ROOT/'provenance.json',{'sources':{p.relative_to(run.old.ROOT).as_posix():sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),source,run.ROOT/'budget_ledger.json',audit_path]},'no_api_calls':True,'original_gate_changed':False})
    print(json.dumps({k:summary[k] for k in ['complete_paired_contrasts','wording_equivalent','wording_complete','independent_wording_sensitivity_equivalent','retention_eligible','retention_passed']}))


if __name__=='__main__':main()
