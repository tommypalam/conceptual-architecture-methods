# Claude screen: unchanged prompts, gross wording failure detected

The 80-call screen detected a large wording effect without a full sweep. Changing to the tested Claude/provider setup did not resolve the known PD/S3 failure. Original prompt files and every dispatched message stayed unchanged.

All 80 responses are valid, with no API/model failures and one attempt per call. Recorded-token cost: **$0.156395** (about 16 cents), within the approved $0.75 cap. **Zero OpenAI calls.**

Configuration neutral; one fixed profile at PD=.8; S3; model `claude-haiku-4-5-20251001`; temperature 1; output cap 600. Twenty calls per formulation, in shuffled four-formulation blocks. Schedule seed 20260914 controls order only; no sampling seed is sent to Anthropic.

| Formulation | ADOPT / valid N | ADOPT rate | Pointwise Wilson 95% interval |
|---|---:|---:|---|
| canonical | 13/20 | 65% | 43.3% to 81.9% |
| paraphrase_1 | 14/20 | 70% | 48.1% to 85.5% |
| paraphrase_2 | 19/20 | 95% | 76.4% to 99.1% |
| paraphrase_3 | 6/20 | 30% | 14.5% to 51.9% |

Prespecified P2-minus-P3 difference: **65%**; conservative exact interval with at least 95% coverage: **14.7% to 89.7%**. The lower bound exceeds the .10 margin, meeting the fixed gross-failure detection rule. All four cells meet the validity floor; there are no unknown decisions.

This is an early rejection signal, not a complete cross-model battery. It supports withholding this provider switch from a larger rerun. No broad model ranking, ethical-competence claim or phase closure follows. The original Phase 1.5 gate remains unmet.

The problem and primary wording pair were selected from previous development evidence. Haiku generated the prior paraphrases; it is the behavioural subject here, not an independent wording judge. Model and provider transport changed together. Historical OpenAI responses were not pooled or used as concurrent controls. Valid means the decision parsed under the expected model, not that its explanation faithfully operationalises the theory.

The [retrospective OpenAI example](../offline/RETROSPECTIVE_SCREEN.md) illustrates why a small screen that does not detect a failure must remain inconclusive. This new Claude result crosses the fixed detection threshold; no allocation or threshold was changed to obtain it.

Next: review the [illustrative reasoning notes](QUALITATIVE_NOTES.md) against the original theory and options, using existing records. No original prompt edits, further paid study or automatic expansion is authorised by this result.

Evidence: [screen_54e26825057964be.json](screen_54e26825057964be.json); [verification](verification.json); [protocol](../PROTOCOL.md); [exact approval](../dispatch_approved.json); [record inventory](../record_checksums.json); [local ZIP](../local_backup.json). Same-computer storage is not off-device backup.
Cost uses reported input/output tokens at the [verified Anthropic rates](https://platform.claude.com/docs/en/about-claude/pricing), before taxes or provider-only adjustments.
