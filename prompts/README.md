# Prompt sources

[Back to the project](../README.md)

| Source | Where to find it |
|---|---|
| Canonical agent template | [System-prompt template](system_prompt_template.md) |
| Original locked dilemmas | [Phase 0 questions](../experiments/phase0_baseline_calibration/questions/) |
| Separate recalibrated dilemmas | [Phase 0b questions](../experiments/phase0b_calibration/questions/) |
| Approved Phase 1.5 paraphrases | [Final reviewed bundle](../experiments/phase1_5_encoding_validity/claude_paraphrases_20260909_theory_r5/) |
| Reviewed PD endpoints | [PD endpoint package](../experiments/phase1_5_encoding_validity/pd_endpoints_20260910/) |
| Retired calibration candidates | [Phase 0b candidate archive](../archive/phase0b/prompt_candidates/) |

A study's frozen manifest determines which source it actually used. Approval of
a wording variant does not imply that the variant passed behavioural validation.
See the [Phase 1.5 findings](../experiments/phase1_5_encoding_validity/README.md).

Existing filenames and prompt bytes remain unchanged. In particular, the legacy
S3 filename does not authorise renaming or rewriting the locked question.
