"""Consolidate completed structural studies without changing any gate or data."""
import json
from pathlib import Path
from hashlib import sha256
import run_structural_encoding_validation as run


def one(root,pattern):
    paths=list(root.glob(pattern))
    if len(paths)!=1:raise ValueError(f'Expected one {pattern}')
    return json.loads(paths[0].read_bytes())


def main():
    root=run.PACKAGE
    diagnostic=one(root/'diagnostics/analysis','result_*.json')
    sweep=one(root/'sweep/analysis','result_*.json')
    pd=one(root/'pd_confirmation/analysis','result_*.json')
    audit=one(root/'audit_schema_r3/analysis','audit_*.json')
    if diagnostic['status']!='COMPLETE' or sweep['status']!='COMPLETE' or not pd['complete'] or not audit['complete']:raise ValueError('Package not complete')
    stages=('diagnostics','sweep','audit','audit_schema_r2','audit_schema_r3','pd_confirmation')
    ledgers={s:json.loads((root/s/'budget_ledger.json').read_bytes()) for s in stages}
    known=sum(l['known_cost_usd'] for l in ledgers.values());unknown=sum(l['unknown_usage_reserved_usd'] for l in ledgers.values())
    pending=sum(l['pending_requests'] for l in ledgers.values())
    m=json.loads((root/'pd_confirmation/manifest.json').read_bytes())['design']
    reserved=m['full_dispatch_reserve_usd']+m['other_package_reserved_usd']
    if pending or reserved>25 or known+unknown>reserved:raise ValueError('Budget inconsistency')
    for s in ('diagnostics','sweep','audit_schema_r3','pd_confirmation'):
        if json.loads((root/s/'analysis/verification.json').read_bytes())['status']!='PASS':raise ValueError('Missing verification')
    budget={'cap_usd':25,'full_conservative_package_reservation_usd':reserved,'known_token_estimate_usd':known,
        'unknown_usage_reserved_usd':unknown,'known_plus_unknown_bound_usd':known+unknown,'pending_requests':pending,
        'completed_behavioral_responses':3580,'completed_final_audit_codings':200,
        'separately_preserved_audit_attempts':14,'ledgers':ledgers,'provider_balance_verified':False,
        'note':'Original reservations retained for completed behavioral stages; undispatched failed-audit slots released. Unknown HTTP400 retains its bound. These estimates are not a provider invoice.'}
    run.save_new(root/'FINAL_BUDGET.json',budget)
    mor=next(g for g in sweep['groups'] if g['parameter']=='MoR' and g['problem']=='S3')
    counts=(sum(x['literal_spec_above_035'] for x in audit['parameters']),sum(x['literal_spec_at_least_050'] for x in audit['parameters']))
    lines=['# Structural encoding: completed evidence package','',
        '**The theory supports the architectural objective, and fresh data support local normative parameterization. The complete ten-parameter validity gate is still unmet. Phase1.5 remains open; Phase2 remains on hold.**',
        '', 'Thesis v0.6 sections3.5,4,4.2 and8.3 put concepts and profiles upstream of decision generation. Sections4.1/4.1.1 allow prompt injection and external state, so an architectural interpretation does not require weight-level learning. The theory was not edited. [Passage-by-passage alignment](THEORY_ALIGNMENT.md).',
        '', '## Completed work',
        '', '| Stage | Design | Complete valid records |',
        '|---|---|---:|',
        '| Diagnostics | MoR/S3 and MS/S2; five levels; six representations; eight new backgrounds | 480 |',
        '| Full canonical sweep | All ten parameters, three locked dilemmas, five levels; twenty different new backgrounds | 3,000 |',
        '| Independent PD confirmation | Two endpoints in S2/S3; twenty-five further new backgrounds | 100 |',
        '| Independent blind audit | Same200 stratified source explanations; Claude Haiku4.5 schema-R3 | 200 |',
        '', 'All behavioral calls used gpt-5.4-mini-2026-03-17, temperature1, max600 and unchanged canonical content except the exact previously approved diagnostic representations. The audit observes already-generated reasoning and cannot replace decisions. This is full parameter/problem/value coverage, not the original15,000-call allocation or a full rerun of the four-part validity battery.',
        '', '## What the evidence establishes',
        '', '**PD provides the strongest new normative result.** Both exploratory effects from the all-ten sweep replicated in a separate prospectively frozen study, using new unselected backgrounds and exact paired inference.',
        '', '| Target | PD .1 to .9 rates | Change | Simultaneous95% CI | Holm p |',
        '|---|---|---|---|---|']
    for g in pd['groups']:
        lo,hi=g['simultaneous95']
        lines.append(f"| {g['problem']} / {g['target_label']} | {g['rates'][0]:.0%} to {g['rates'][1]:.0%} | +{100*g['effect']:.0f}pp | [{100*lo:.1f}, {100*hi:.1f}]pp | {g['p_holm']:.8g} |")
    lines+=['', 'The same coordinate changes different actions across the two contexts. It is consistent with a process/outcome orientation participating in generating decisions, rather than an external rule evaluating and replacing a completed answer. The architecture and numerical intervention support a causal input effect under this harness. They do not uniquely identify the model\'s internal computation.',
        '', 'S2 contains a real normative tradeoff between formal independent classification and proportionate local correction. S3 WAIT allows preparing a written plan, but also expresses caution or preservation; a uniquely procedural mechanism is unresolved. Neither action is labeled morally superior. The test uses familiar dilemmas with new profiles, not unseen-task transfer. [Independent confirmation](pd_confirmation/analysis/REPORT.md).',
        '', f"**MoR shows an ordered observed curve on the all-ten sweep:** {', '.join(f'{100*x:.0f}%' for x in mor['rates'])} ADOPT across .1/.3/.5/.7/.9. Frozen bootstrap endpoint +65pp, adjusted interval[20,100]; interior +50pp,[5,90]. However, MoR does not survive the supplementary exact paired Holm60 check. This disagreement must accompany the primary positive flag; response style alone does not establish normative content.",
        '', '**Coverage does not imply validation of every coordinate.** Only one of the nine original directional predictions has a positive frozen adjusted endpoint flag. The other21 parameter/dilemma combinations were exploratory. S1 is largely at ceiling, sharply limiting identifiability. MS has an ordered but small canonical S2 curve in this sweep; its adjusted endpoint interval includes0. Report all30 curves, including weak, opposite and non-monotonic patterns. [Full sweep](sweep/analysis/REPORT.md) and [exact sensitivity](sweep/analysis/discrete_uncertainty_sensitivity.json).',
        '', '**Representation robustness remains incomplete.** MoR endpoint direction agrees across all six diagnostic representations, but the eight-background panel is imprecise. MS numeric-only reverses direction. None of the24 diagnostic contrasts survives the supplementary exact paired Holm check. This panel cannot establish the original24/30 paraphrase-equivalence gate. [Diagnostics](diagnostics/analysis/INTERPRETATION.md).',
        '', f"**Blind recoverability:** the completed200-item audit meets the literal historical rule: {audit['literal_spec_thresholds_met']}. It has {counts[0]}/10 traits above35% with the historical p criterion (six required), and {counts[1]}/10 at least50% (four required). Report active-trait and empirical-majority comparisons alongside aggregate accuracy. Short explanations are not direct observations of hidden reasoning. [Full audit](audit_schema_r3/analysis/REPORT.md).",
        '', 'PD is also the clearest active-trait signal in this audit:11/20 quartiles correct (55%; balanced accuracy56.25%), problem-stratified permutation p=.003 and supplementary Holm10 p=.03. This is converging but limited evidence: the audit uses short model explanations and its permutation does not additionally cluster repeated backgrounds. All2000 estimates were non-null despite permission to abstain, so do not infer that every estimate had adequate evidence. AW aggregate56% accuracy exactly matches its56% majority baseline.',
        '', '## Thesis-ready claim and remaining limits',
        '', '> Explicit, normatively grounded profile parameters can be implemented as generative inputs to an LLM-based agent and can produce reproducible, context-dependent changes in selected decisions. Independent matched-profile confirmation supports a local effect of Procedural Dependence. The evidence supports a limited architectural feasibility claim; it does not validate the entire ten-parameter representation or establish intrinsic ethical understanding.',
        '', 'A broader claim requires stronger evidence of construct-specific interpretation, expression robustness, recovery and generalization. The original8/30 equivalence result, deficient representation retention and earlier audit limitations remain in the record. No thresholds were relaxed to produce a pass; the later PD confirmation has its own prospective local rule and does not amend the original gate. Persistent internalization, moral improvement, collective dynamics and AGI are not established here.',
        '', 'The requested diagnostic, all-parameter sweep and independent-audit sequence is complete. No further calls are queued. A future pass-with-revision proposal would need to explicitly reconcile the limited empirical claim with the original gate before Phase2; it is not silently enacted by this report.',
        '', '## Provenance, failures and cost',
        '', 'Initial coder batch stopped after12 valid responses plus one malformed TD code. The first schema attempt returned HTTP400 on its first request. All14 attempts are retained separately. R3 used the same200 items, messages, keys, model and scoring, with a corrected JSON schema and max1000. The provider adds a format instruction and constrains sampling: this is a disclosed rater-instrument change, with no pooling or in-place repair of earlier outcomes.',
        '', f"Known token-cost estimate for this package: **${known:.6f}**, plus **${unknown:.6f}** retained for unknown usage. All conservative stage/repair reservations total **${reserved:.6f}**, below the **$25** cap. Zero pending requests. [Budget ledger](FINAL_BUDGET.json). Provider balance/invoice not verified.",
        '', 'All complete stages passed exact request/settings and returned-ID checks, raw reparsing, statistical recomputation where applicable, and same-computer ZIP byte equality. Eighteen relevant offline tests passed; sweep and confirmation figures were visually inspected. Raw per-call records and private audit packs remain local and excluded from Git; checksum inventories are committed. Same-computer backups are not off-device backups.',
        '', 'The original locked prompts, theory text, Beta marginals and R are unchanged. Draw/schedule/analysis seeds are respectively20261005/6/7 for diagnostics,20261008/9/10 for the sweep,20261011 for audit selection, and20261012/13/14 for confirmation (exact primary inference uses no simulated draws).','']
    narrative='\n'.join(lines)
    for before,after in {'Phase1.5': 'Phase 1.5', 'Phase2': 'Phase 2', 'sections3.5,4,4.2 and8.3': 'sections 3.5, 4, 4.2 and 8.3', 'Sections4.1/4.1.1': 'Sections 4.1/4.1.1', 'Same200': 'Same 200', 'Haiku4.5': 'Haiku 4.5', 'temperature1': 'temperature 1', 'max600': 'maximum 600', 'original15,000': 'original 15,000', 'Simultaneous95%': 'Simultaneous 95%', 'other21': 'other 21', 'includes0': 'includes 0', 'all30': 'all 30', 'the24': 'the 24', 'original24/30': 'original 24/30', 'completed200-item': 'completed 200-item', 'above35%': 'above 35%', 'least50%': 'least 50%', 'audit:11/20': 'audit: 11/20', 'accuracy56.25%': 'accuracy 56.25%', 'All2000': 'All 2,000', 'aggregate56%': 'aggregate 56%', 'its56%': 'its 56%', 'original8/30': 'original 8/30', 'after12': 'after 12', 'HTTP400': 'HTTP 400', 'All14': 'All 14', 'same200': 'same 200', 'max1000': 'maximum 1,000', 'respectively20261005/6/7': 'respectively 20261005/20261006/20261007', 'diagnostics,20261008/9/10': 'diagnostics, 20261008/20261009/20261010', 'sweep,20261011': 'sweep, 20261011', 'and20261012/13/14': 'and 20261012/20261013/20261014', 'meets the literal historical rule: False': 'does not meet the literal historical rule', 'Holm60': 'Holm correction across 60 tests', 'Holm10': 'Holm correction across 10 tests', 'interval[20,100]': 'interval [20, 100]'}.items():narrative=narrative.replace(before,after)
    (root/'FINAL_ASSESSMENT.md').write_text(narrative,encoding='utf-8')
    print(json.dumps({'complete':True,'known_cost_usd':known,'unknown_bound_usd':unknown,'reserved_usd':reserved,'audit_literal_rule':audit['literal_spec_thresholds_met']}))


if __name__=='__main__':main()
