# Phase 0 Prompt Archive

This folder preserves earlier prompt versions so Phase 0 prompt tuning remains fully auditable. One subfolder per archived state, named `{problem}_{nN}_{outcome}_{descriptor}_{date}`.

**Naming scheme:** `{problem}` prefix (e.g. `s1`, `s2s3`, `c1`) · `n{N}` sample size · outcome slug (e.g. `a57`, `approve68`, `wait91`) · short descriptor of what varied · date `YYYY-MM-DD`. Status words (`accepted`, `retired`, `failed`, `overshoot`) appear after the outcome slug.

---

## S1/S2/S3 — Multi-problem states

- `s1s2s3_original_protocol_pdf_2026-04-21/`: original S1–S3 prompts extracted from `experimental_problems_protocol.pdf`.
- `s1s2s3_pre_rebalance_2026-04-30/`: bare-reply prompts live immediately before the 2026-04-30 rebalance pass.
- `s1s2s3_n10_rebalance_v1_2026-04-30/`: rebalance v1. S1 overcorrected toward A; S2 REPORT-only; S3 PIVOT-only.
- `s1s2s3_n10_rebalance_v2_2026-04-30/`: rebalance v2. S1 A-only; S2 REPORT-only; S3 8/2 PIVOT/PERSIST.
- `s1s2s3_n10_rebalance_v3_2026-04-30/`: rebalance v3. S1 B-only; S2 9/1 QUIET/REPORT; S3 acceptable at N=10.
- `s1s2s3_n10_rebalance_v4_2026-04-30/`: rebalance v4. S2 and S3 calibrated and frozen; S1 remained A-dominant.
- `s1s2s3_n10_rebalance_v5_2026-04-30/`: rebalance v5. S1 B-only; S2 and S3 frozen.
- `s1s2s3_n10_rebalance_v6_2026-04-30/`: rebalance v6. S1 8/2 B/A; S2 and S3 frozen.
- `s1s2s3_n10_rebalance_v7_2026-04-30/`: rebalance v7. S1 9/1 B/A; rolled back to v6.
- `s1s2s3_n10_rebalance_v8_pre_final_tweak_2026-04-30/`: rollback state before final S1-only tweak. Prior result: 8/2 B/A.
- `s1s2s3_n10_accepted_smoke_2026-04-30/`: accepted smoke result: S1 7/3 B/A; S2 calibrated; S3 calibrated.
- `s1s2s3_n20_accepted_2026-04-30/`: accepted before N=50 retry. S1 12/8 B/A; S2 11/9 QUIET/REPORT; S3 25/25.
- `s1s2s3_n50_2026-04-30/`: N=50 result. S1 45/5 B/A; S2 36/14 QUIET/REPORT; S3 25/25.
- `s1s2s3_n700_large_n_2026-04-30/`: N=700 large-N check. S1 385/315 A/B; S2 437/263 QUIET/REPORT; S3 416/284 PIVOT/PERSIST.

---

## S1/S2 — Joint states

- `s1s2_n20_overshoot_2026-04-30/`: failed retune after N=50. S1 20/0 A/B; S2 20/0 REPORT/QUIET.
- `s1s2_n20_retune_after_overshoot_2026-04-30/`: retune after overshoot. S1 18/2 A/B; S2 18/2 QUIET/REPORT.
- `s1s2_n20_second_overshoot_2026-04-30/`: second failed retune. S1 20/0 A/B; S2 20/0 REPORT/QUIET.
- `s1s2_n20_explicit_conflict_2026-04-30/`: explicit-conflict retune. S1 16/4 B/A; S2 11/9 QUIET/REPORT — S2 frozen here.
- `s1s2_accepted_final_2026-04-30/`: final accepted frozen S1 and S2. S1 385/315 A/B at N=700; S2 102/98 REPORT/QUIET at N=200.
- `s1s2_n200_accepted_final_2026-05-01/`: N=200 frozen validation. S1 106/94 A/B; S2 102/98 REPORT/QUIET. Both WELL-CALIBRATED.

---

## S1

- `s1_n20_a_overshoot_2026-04-30/`: failed S1 retune after explicit-conflict version. S1 18/2 A/B.

---

## S2

- `s2_n200_quiet139_2026-04-30/`: S2 retune. 139/61 QUIET/REPORT.
- `s2_n200_quiet163_document_wording_2026-04-30/`: "document" wording. 163/37 QUIET/REPORT.
- `s2_n200_if_needed_wording_2026-04-30/`: "classification record if needed" before midpoint phrase change.
- `s2_n200_report59_create_note_wording_2026-04-30/`: "create an independent classification note." 59% REPORT at N=200.
- `s2_n200_quiet143_draft_note_wording_2026-04-30/`: "draft an independent classification note." 143/57 QUIET/REPORT.
- `s2_enter_note_audit_trail_wording_2026-04-30/`: "enter an independent classification note in the audit trail."
- `s2_add_note_wrong_direction_2026-04-30/`: mistaken retune using "add an independent classification note" after direction misunderstanding.
- `s2_n500_report307_2026-04-30/`: N=500 retune. 307/193 REPORT/QUIET.
- `s2_n500_quiet384_2026-04-30/`: N=500 retune. 384/116 QUIET/REPORT.
- `s2_n500_report65_classification_note_wording_2026-04-30/`: "make an independent classification note." 58% dominant at N=200; 65% at N=500.

---

## S2/S3 — Joint states

- `s2s3_n50_retune_overshoot_2026-04-30/`: failed S2/S3 retune. S2 39/11 REPORT/QUIET; S3 32/18 PIVOT/PERSIST.
- `s2s3_n50_close_retune_2026-04-30/`: close retune. S2 31/19 QUIET/REPORT; S3 33/17 PIVOT/PERSIST.

---

## S3 — Startup-pivot family (PIVOT/PERSIST labels, retired 2026-05-01)

All entries below belong to the startup-pivot scenario. This family was retired after ~20 variants failed to produce a balanced split: stable ~59% PIVOT mode at N=700, any risk cue overshot to 70–88% PERSIST. Replaced by the Department Reorganisation family (ADOPT/WAIT). See `meta.md` 2026-05-01 for full rationale.

- `s3_n200_pivot114_acceptable_2026-04-30/`: acceptable PIVOT-lean state. 114/86 PIVOT/PERSIST.
- `s3_n200_pivot123_close_base_2026-04-30/`: close restored base. 123/77 PIVOT/PERSIST.
- `s3_n200_pivot128_base_repeat_2026-04-30/`: repeated base-state check. 128/72 PIVOT/PERSIST.
- `s3_n200_pivot133_raised_concerns_wording_2026-04-30/`: "raised concerns" wording. 133/67 PIVOT/PERSIST.
- `s3_n200_pivot140_paid_pilot_wording_2026-04-30/`: "paid pilot" in persist sentence. 140/60 PIVOT/PERSIST.
- `s3_n200_pivot147_time_limited_wording_2026-04-30/`: "time-limited" in persist sentence. 147/53 PIVOT/PERSIST.
- `s3_n200_pivot149_still_has_time_wording_2026-04-30/`: "while the company still has time." 149/51 PIVOT/PERSIST.
- `s3_n200_pivot156_possibly_wording_2026-04-30/`: "possibly necessary change." 156/44 PIVOT/PERSIST.
- `s3_n200_pivot162_unproven_wording_2026-04-30/`: "but still unproven." 162/38 PIVOT/PERSIST.
- `s3_n200_pivot176_fraction_cost_wording_2026-04-30/`: "six of your fourteen employees" in pivot sentence. 176/24 PIVOT/PERSIST.
- `s3_n200_persist169_overshoot_2026-04-30/`: failed retune, persist overshoot. 169/31 PERSIST/PIVOT.
- `s3_n200_persist169_before_committing_wording_2026-04-30/`: "before committing to a pivot." 169/31 PERSIST/PIVOT.
- `s3_revenue_has_been_wording_failed_2026-04-30/`: failed micro-retune using "Revenue has been flat."
- `s3_n200_pivot122_final_startup_family_retired_2026-05-01/`: final state before scenario-level rewrite. 122/78 PIVOT/PERSIST, CI [54.1%, 67.5%] — outside 60/40 band. Startup-pivot family retired here.

---

## S3 — Department Reorganisation family (ADOPT/WAIT labels)

- `s3_dept_n70_adopt71_v1_2026-05-01/`: v1. 50/20 ADOPT/WAIT at N=70 (71% ADOPT). WAIT lacked concrete upside.
- `s3_dept_n50_wait100_v2_2026-05-01/`: v2. 50/0 WAIT/ADOPT at N=50 (100% WAIT). "Difficult to reverse" on ADOPT was the cliff trigger.
- `s3_dept_n50_adopt92_v3_2026-05-01/`: v3. 46/4 ADOPT/WAIT at N=50 (92% ADOPT). WAIT had no positive upside.
- `s3_dept_n50_wait82_v4_2026-05-01/`: v4. 41/9 WAIT/ADOPT at N=50 (82% WAIT). Observe-peer-results recreated information-gain trigger.
- `s3_dept_n200_wait57_v5_2026-05-01/`: v5. 115/85 WAIT/ADOPT at N=200 (57.5% WAIT). Acceptable near-boundary.
- `s3_dept_n200_wait91_v6_modest_wording_failed_2026-05-01/`: v6 failed. 183/17 WAIT/ADOPT at N=200 (91.5% WAIT). "Modest early gains" sharply over-favoured WAIT.
- `s3_dept_n200_wait67_v5_repeat_2026-05-01/`: v5 repeated. 135/65 WAIT/ADOPT at N=200 (67.5% WAIT). v7 weakens WAIT planning benefit.
- `s3_dept_n200_accepted_v7_2026-05-01/`: **ACCEPTED — LOCKED.** 100/100 ADOPT/WAIT at N=200. WELL-CALIBRATED.

---

## C1 — Resource Allocation

- `c1_original_continuous_allocation_spec_retired_2026-05-02/`: original continuous-allocation design. Retired — budget averaging is not a clean 50/50 baseline target.
- `c1_n20_a63_v1_2026-05-02/`: v1 binary-package. Agent-level 63/37 PACKAGE_A/B.
- `c1_n20_a64_v2_2026-05-02/`: v2. 64/36 A/B. Arithmetic nudge failed.
- `c1_n20_a60_v3_2026-05-02/`: v3. 60/40 A/B. Acceptable flag.
- `c1_n20_a60_v4_no_move_2026-05-02/`: v4. Unchanged at 60/40 A/B. v5 applies structural rebalance.
- `c1_n20_a57_v5_2026-05-02/`: v5. 57/43 A/B (run-level 19/1 A/B). v6 applies small final B nudge.
- `c1_n20_b80_v6_overshoot_2026-05-02/`: v6 failed. 80/20 B/A. "Credible/sufficient" wording caused semantic cliff.
- `c1_n20_a61_v7_2026-05-02/`: v7. 61/39 A/B. v8 switches to agent-level final votes as primary metric.
- `c1_n20_a70_direct_2026-05-02/`: direct-method smoke. 70% A.
- `c1_n20_a70_direct_v2_2026-05-02/`: direct v2. 70% A.
- `c1_n20_a75_direct_2026-05-02/`: direct. 75% A.
- `c1_n20_a75_direct_v2_2026-05-02/`: direct v2. 75% A.
- `c1_n20_a80_direct_2026-05-02/`: direct. 80% A.
- `c1_n20_a80_direct_v2_2026-05-02/`: direct v2. 80% A.
- `c1_n20_a85_direct_2026-05-02/`: direct. 85% A.
- `c1_n20_a90_direct_2026-05-02/`: direct. 90% A.
- `c1_n20_a95_direct_2026-05-02/`: direct. 95% A.
- `c1_n20_a100_direct_2026-05-02/`: direct. 100% A.
- `c1_n20_b80_direct_2026-05-02/`: direct. 80% B.
- `c1_n20_b85_direct_2026-05-02/`: direct. 85% B.
- `c1_n20_b90_direct_2026-05-02/`: direct. 90% B.
- `c1_n20_b100_direct_2026-05-02/`: direct. 100% B.
- `c1_n20_b100_direct_v2_2026-05-02/`: direct v2. 100% B.
- `c1_n200_a57_direct_2026-05-02/`: N=200 direct. 57% A.
- `c1_n200_a64_direct_2026-05-02/`: N=200 direct. 64% A.
- `c1_n200_a64_direct_pre_csr_shift_2026-05-02/`: N=200 direct, before CSR shift. 64% A.
- `c1_n200_a69_direct_halfstep_failed_2026-05-02/`: N=200 failed halfstep retune. 69% A.
- `c1_n200_a69_direct_bonus_plus1_failed_2026-05-02/`: N=200 failed B bonus +1 retune. 69% A.
- `c1_n200_a70_direct_reserve_shift_failed_2026-05-02/`: N=200 failed B reserve shift. 70% A.
- `c1_n200_a71_direct_csr_plus2_failed_2026-05-02/`: N=200 failed B CSR +2 retune. 71% A.
- `c1_n200_b61_direct_2026-05-02/`: N=200 direct. 61% B.
- `c1_accepted_direct_prompt_2026-05-02/`: **ACCEPTED — LOCKED.** Final validation N=200: 103/97 PACKAGE_A/B (51.5%). WELL-CALIBRATED.

---

## C2 — Restructuring Decision

- `c2_original_three_option_amend_trap_2026-05-02/`: original three-option design showing AMEND collapse.
- `c2_three_option_direct_retired_2026-05-02/`: three-option direct baseline retired. AMEND attracted ~100% of responses.
- `c2_n20_amend100_direct_2026-05-02/`: direct, three options. 100% AMEND.
- `c2_n20_amend100_binding_timing_wording_2026-05-02/`: "binding timing" wording. 100% AMEND.
- `c2_n20_amend100_cautious_update_wording_2026-05-02/`: "cautious update" wording. 100% AMEND.
- `c2_n20_amend100_nonbinding_review_wording_2026-05-02/`: "non-binding review" wording. 100% AMEND.
- `c2_n20_amend100_partial_approval_payfreeze_wording_2026-05-02/`: "partial approval + pay freeze" wording. 100% AMEND.
- `c2_n20_amend100_reject_half_savings_wording_2026-05-02/`: "reject half savings" wording. 100% AMEND.
- `c2_n20_amend100_same_layoffs_support_wording_2026-05-02/`: "same layoffs + support" wording. 100% AMEND.
- `c2_n20_amend100_weak_hybrid_wording_2026-05-02/`: "weak hybrid" wording. 100% AMEND.
- `c2_n20_amend65_approve35_direct_2026-05-02/`: 65% AMEND / 35% APPROVE.
- `c2_n20_amend80_reject_part_gap_failed_2026-05-02/`: failed retune. 80% AMEND, reject/part gap.
- `c2_n20_amend90_approve10_direct_2026-05-02/`: 90% AMEND / 10% APPROVE.
- `c2_n20_approve100_no_revised_plan_wording_2026-05-02/`: "no revised plan" wording. 100% APPROVE.
- `c2_n200_approve68_binary_2026-05-02/`: N=200 binary. 68% APPROVE.
- `c2_n200_approve80_binary_half_savings_failed_2026-05-02/`: N=200 binary failed. 80% APPROVE. "Half savings" wording.
- `c2_n200_approve72_deeper_cuts_wording_2026-05-02/`: N=200 direct. 72% APPROVE. "Deeper cuts" wording.
- `c2_accepted_binary_prompt_2026-05-02/`: **ACCEPTED — LOCKED.** Final validation N=200: 100/100 APPROVE/REJECT (50.0%). WELL-CALIBRATED.

---

## C3 — Scientific Approach

- `c3_n20_pivot70_v1_2026-05-02/`: v1. 14/6 PIVOT/CONTINUE at N=20 (70% PIVOT).
- `c3_n20_continue_overshoot_incomplete_v2_2026-05-02/`: v2 incomplete, quota-limited. Parseable finals overcorrected toward CONTINUE.
- `c3_n20_continue100_direct_2026-05-02/`: direct. 100% CONTINUE.
- `c3_n20_continue100_replication_after_funding_wording_2026-05-02/`: "replication after funding" wording. 100% CONTINUE.
- `c3_n20_continue100_review_3_3_wording_2026-05-02/`: "3 successes / 3 failures" review wording. 100% CONTINUE.
- `c3_n20_continue75_direct_2026-05-02/`: direct. 75% CONTINUE.
- `c3_n20_pivot100_direct_2026-05-02/`: direct. 100% PIVOT.
- `c3_n20_pivot65_slowing_wording_2026-05-02/`: "slowing" wording. 65% PIVOT.
- `c3_n20_pivot85_limited_pilot_wording_2026-05-02/`: "limited pilot" wording. 85% PIVOT.
- `c3_accepted_spec_2026-05-02/`: accepted frozen C3 spec/definition, before N=200 direct-method calibration.
- `c3_accepted_direct_prompt_2026-05-02/`: **ACCEPTED — LOCKED.** Final validation N=200: 102/98 CONTINUE/PIVOT (51.0%). WELL-CALIBRATED.
