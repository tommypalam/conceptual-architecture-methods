# Phase 0 Simple Prompt Archive

This folder preserves earlier S1-S3 prompt versions so Phase 0 prompt tuning remains auditable.

- `pre_tweak_2026-04-30/`: the bare-reply markdown prompts that were live immediately before the gpt-5.4-mini rebalance pass on 2026-04-30.
- `rebalance_v1_2026-04-30/`: the first rebalance pass. User-reported result: S1 overcorrected toward A; S2 stayed REPORT-only; S3 stayed PIVOT-only.
- `rebalance_v2_2026-04-30/`: the second rebalance pass. User-reported result: S1 stayed A-only; S2 stayed REPORT-only; S3 moved to 8/2 PIVOT/PERSIST.
- `rebalance_v3_2026-04-30/`: the third rebalance pass. User-reported result: S1 moved to B-only; S2 moved to 9/1 QUIET/REPORT; S3 looked acceptable at N=10.
- `rebalance_v4_2026-04-30/`: the fourth rebalance pass. User-reported result: S2 and S3 calibrated well and frozen; S1 remained A-dominant.
- `rebalance_v5_2026-04-30/`: the fifth rebalance pass. User-reported result: S1 moved to B-only; S2 and S3 remained frozen.
- `rebalance_v6_2026-04-30/`: the sixth rebalance pass. User-reported result: S1 moved to 8/2 B/A; S2 and S3 remained frozen.
- `rebalance_v7_2026-04-30/`: the seventh rebalance pass. User-reported result: S1 moved to 9/1 B/A; rolled back to v6.
- `rebalance_v8_pre_final_tweak_2026-04-30/`: rollback state before final S1-only tweak. User-reported prior result: 8/2 B/A.
- `accepted_simple_2026-04-30/`: accepted frozen simple-problem prompt set. User-reported smoke results: S1 7/3 B/A; S2 calibrated; S3 calibrated.
- `accepted_simple_n20_2026-04-30/`: accepted simple prompt set before N=50 retry. User-reported results: S1 12/8 B/A at N=20; S2 11/9 QUIET/REPORT at N=20; S3 25/25 at N=50.
- `accepted_s1_s2_final_2026-04-30/`: final accepted frozen prompt set for S1 and S2 only. User-reported results: S1 385/315 A/B across 700 files; S2 102/98 REPORT/QUIET at N=200. S3 is not frozen in this archive.
- `frozen_s1_s2_n200_2026-05-01/`: frozen-set N=200 validation for S1 and S2. User-reported results: S1 106/94 A/B; S2 102/98 REPORT/QUIET. Both WELL-CALIBRATED.
- `n700_large_n_2026-04-30/`: large-N calibration state. User-reported results: S1 385/315 A/B and frozen; S2 437/263 QUIET/REPORT; S3 416/284 PIVOT/PERSIST.
- `n50_s2s3_retune_overshoot_2026-04-30/`: failed/light retune state. User-reported results: S2 39/11 REPORT/QUIET; S3 32/18 PIVOT/PERSIST.
- `n50_s2s3_close_retune_2026-04-30/`: close retune state. User-reported results: S2 31/19 QUIET/REPORT; S3 33/17 PIVOT/PERSIST.
- `n500_s2_report_lean_2026-04-30/`: large-N S2 retune state. User-reported result: S2 307/193 REPORT/QUIET.
- `n500_s2_quiet_lean_2026-04-30/`: large-N S2 retune state. User-reported result: S2 384/116 QUIET/REPORT.
- `n200_s2_quiet_lean_2026-04-30/`: S2 midpoint retune state. User-reported result: S2 139/61 QUIET/REPORT.
- `n200_s2_document_quiet_lean_2026-04-30/`: S2 retune state. User-reported result: S2 163/37 QUIET/REPORT.
- `n200_s2_if_needed_2026-04-30/`: S2 state using "classification record if needed" before midpoint phrase change.
- `n500_s2_classification_note_report_lean_2026-04-30/`: S2 state using "make an independent classification note"; user-reported dominant share 58% at N=200 and 65% at N=500.
- `s2_wrong_direction_add_note_2026-04-30/`: mistaken S2 retune after direction misunderstanding; used "add an independent classification note."
- `s2_enter_note_audit_trail_2026-04-30/`: S2 state using "enter an independent classification note in the audit trail."
- `n200_s2_create_note_report_lean_2026-04-30/`: S2 state using "create an independent classification note"; user-reported REPORT at 59% for N=200.
- `n200_s2_draft_note_quiet_lean_2026-04-30/`: S2 state using "draft an independent classification note"; user-reported result: S2 143/57 QUIET/REPORT.
- `n200_s3_persist_overshoot_2026-04-30/`: failed S3 retune. User-reported result: S3 169/31 PERSIST/PIVOT at N=200.
- `n200_s3_pivot_acceptable_2026-04-30/`: acceptable but PIVOT-leaning S3 state. User-reported result: S3 114/86 PIVOT/PERSIST at N=200.
- `n200_s3_pivot_overshoot_possibly_2026-04-30/`: failed S3 one-word retune using "possibly necessary change." User-reported result: S3 156/44 PIVOT/PERSIST at N=200.
- `n200_s3_pivot_overshoot_unproven_2026-04-30/`: failed S3 retune using "but still unproven" in the pivot sentence. User-reported result: S3 162/38 PIVOT/PERSIST at N=200.
- `n200_s3_pivot_overshoot_time_limited_2026-04-30/`: failed S3 retune using "time-limited" in the persist sentence. User-reported result: S3 147/53 PIVOT/PERSIST at N=200.
- `n200_s3_pivot_overshoot_paid_pilot_2026-04-30/`: failed S3 retune using "paid pilot" in the persist sentence. User-reported result: S3 140/60 PIVOT/PERSIST at N=200.
- `n200_s3_pivot_overshoot_still_has_time_2026-04-30/`: failed S3 retune using "while the company still has time." User-reported result: S3 149/51 PIVOT/PERSIST at N=200.
- `n200_s3_pivot_overshoot_fraction_cost_2026-04-30/`: failed S3 retune using "six of your fourteen employees" in the final pivot sentence. User-reported result: S3 176/24 PIVOT/PERSIST at N=200.
- `n200_s3_pivot_close_base_2026-04-30/`: close restored S3 base state. User-reported result: S3 123/77 PIVOT/PERSIST at N=200.
- `n200_s3_persist_overshoot_before_committing_2026-04-30/`: failed S3 retune using "before committing to a pivot" in the persist sentence. User-reported result: S3 169/31 PERSIST/PIVOT at N=200.
- `n200_s3_base_repeat_64_pivot_2026-04-30/`: repeated S3 base-state check. User-reported result: S3 128/72 PIVOT/PERSIST at N=200.
- `n200_s3_raised_concerns_pivot_lean_2026-04-30/`: light S3 retune using "raised concerns." User-reported result: S3 133/67 PIVOT/PERSIST at N=200.
- `s3_failed_revenue_has_been_2026-04-30/`: failed final S3 micro-retune using "Revenue has been flat." User reported it was worse.
- `n200_s3_pivot_lean_61_2026-05-01/`: final state of the startup-pivot scenario family before scenario-level rewrite. User-reported result: 122 PIVOT / 78 PERSIST at N=200, 95% Wilson CI [54.1%, 67.5%] on PIVOT — outside the 60/40 acceptable band lower bound. After ~20 documented variants the scenario family was retired and replaced by `The Department Reorganisation` (ADOPT/WAIT). See `meta.md` 2026-05-01 entries for the rationale.
- `n50_result_2026-04-30/`: N=50 result state. User-reported results: S1 45/5 B/A; S2 36/14 QUIET/REPORT; S3 25/25 PIVOT/PERSIST.
- `n20_overshoot_2026-04-30/`: failed retune after N=50. User-reported results: S1 20/0 A/B; S2 20/0 REPORT/QUIET.
- `n20_retune_aquiet_2026-04-30/`: retune after overshoot. User-reported results: S1 18/2 A/B; S2 18/2 QUIET/REPORT.
- `n20_second_overshoot_2026-04-30/`: failed retune. User-reported results: S1 20/0 A/B; S2 20/0 REPORT/QUIET.
- `n20_explicit_conflict_2026-04-30/`: explicit-conflict retune. User-reported results: S1 16/4 B/A; S2 11/9 QUIET/REPORT and frozen.
- `n20_s1_a_overshoot_2026-04-30/`: failed S1 retune after explicit-conflict version. User-reported result: S1 18/2 A/B.
- `protocol_pdf_2026-04-21/`: the original simple-problem prompts extracted from `C:\Users\tommy\Downloads\experimental_problems_protocol.pdf`.

Current prompts remain in `../S1_promotion_decision.md`, `../S2_quiet_error.md`, and `../S3_strategic_pivot.md`.

## S3 scenario family transition (2026-05-01)

Entries above through `n200_s3_pivot_lean_61_2026-05-01/` belong to the **startup-pivot** scenario family (PIVOT/PERSIST labels). That family was retired on 2026-05-01 after ~20 documented retunes failed to produce a balanced split: the model held a stable ~59% PIVOT mode at N=700 in the neutral wording, and any risk cue added to the pivot side overshot to 70-88% PERSIST.

The current live `../S3_strategic_pivot.md` uses a structurally different scenario (**The Department Reorganisation**, ADOPT/WAIT labels). New retune entries in this archive should be tagged with the scenario family they belong to so the two histories don't get mixed.

- `n70_s3_dept_adopt_lean_71_2026-05-01/`: Department Reorganisation v1 (ADOPT/WAIT). User-reported result: 50 ADOPT / 20 WAIT at N=70 (71.4% ADOPT). WAIT lacked a concrete upside — described purely as avoidance.
- `n50_s3_dept_wait_100_2026-05-01/`: Department Reorganisation v2. User-reported result: 50 WAIT / 0 ADOPT at N=50 (100% WAIT). "Difficult to reverse" on ADOPT was the cliff trigger; information-gain framing on WAIT also stacked. v3 removes both and uses symmetric cost framing (each side has one concrete cost + one uncertain downside).
- `n50_s3_dept_adopt_92_v3_2026-05-01/`: Department Reorganisation v3. User-reported result: 46 ADOPT / 4 WAIT at N=50 (92.0% ADOPT). WAIT had no positive upside, so v4 restores a bounded observe-peer-results upside without reintroducing irreversibility.
- `n50_s3_dept_wait_82_v4_2026-05-01/`: Department Reorganisation v4. User-reported result: 41 WAIT / 9 ADOPT at N=50 (82.0% WAIT). Observe-peer-results recreated an information-gain trigger; v5 replaces it with a smaller written-plan upside.
- `n200_s3_dept_v5_wait_57_2026-05-01/`: Department Reorganisation v5. User-reported result: 115 WAIT / 85 ADOPT at N=200 (57.5% WAIT). Acceptable near-boundary baseline before one final micro-retune.
- `n200_s3_dept_wait_91_v6_modest_2026-05-01/`: failed Department Reorganisation v6. User-reported result: 183 WAIT / 17 ADOPT at N=200 (91.5% WAIT). "Modest early gains" sharply over-favored WAIT.
- `n200_s3_dept_v5_repeat_wait_67_2026-05-01/`: repeated Department Reorganisation v5 check. User-reported result: 135 WAIT / 65 ADOPT at N=200 (67.5% WAIT). Live prompt matched archived v5 exactly; v7 weakens the WAIT planning benefit.
- `accepted_s3_dept_v7_n200_2026-05-01/`: accepted frozen Department Reorganisation v7 prompt. User-reported result: 100 ADOPT / 100 WAIT at N=200. WELL-CALIBRATED.
