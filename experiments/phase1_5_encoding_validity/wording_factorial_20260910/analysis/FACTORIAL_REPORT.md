# PD/S3 wording attribution: completed diagnostic

The approved experiment collected all **1,200 responses**, 300 per condition.
All parsed successfully; there were no terminal API errors or returned-model
mismatches. The numerical profile and dilemma stayed fixed. The results show
a large PD endpoint-wording effect, an additional effect from the other nine
descriptions, and evidence that these effects depend on their combination.

## Collection and outcome

Configuration: neutral full harness. One fixed profile, PD=.8 and the other
nine parameters at their existing Beta means; no new population draws. Model
`gpt-5.4-mini-2026-03-17`, temperature 1, output cap 600, root seed 20260910.
Collection ran September 10, 00:47:01 to 00:56:44 UTC, in 300 randomized blocks
of four requests. The primary outcome is the fixed first option, ADOPT.

| Condition | PD endpoint wording | Other nine descriptions | ADOPT / valid N | ADOPT rate | Simultaneous rate interval |
|---|---|---|---:|---:|---:|
| A | P2 | P2 | 255 / 300 | 85.0% | 79.2% to 89.8% |
| B | P3 | P2 | 45 / 300 | 15.0% | 10.2% to 20.8% |
| C | P2 | P3 | 161 / 300 | 53.7% | 46.3% to 60.9% |
| D | P3 | P3 | 25 / 300 | 8.3% | 4.8% to 13.1% |

All four cells meet the 98% parse floor, with zero missing or invalid responses.
Rate intervals above are the prespecified Bonferroni exact bounds with at least
95% simultaneous coverage under the binomial assumptions. The machine-readable
cell summaries additionally retain ordinary pointwise Wilson intervals; those
are not the simultaneous intervals used for the contrasts below.

## Prespecified contrasts

Effects are in percentage points, with P2 minus P3 orientation. The three
intervals are jointly covered by the same simultaneous rate bounds.

| Contrast | Estimate | Simultaneous 95% interval | Interpretation |
|---|---:|---:|---|
| PD wording, averaged across both backgrounds | +57.7 | +45.7 to +67.8 | Large PD wording effect; interval entirely above the 20-point planning target |
| Other nine descriptions, averaged across both PD versions | +19.0 | +7.7 to +29.7 | Background wording also matters; uncertainty spans the 20-point planning target |
| Interaction, difference of PD effects | +24.7 | +2.2 to +46.4 | PD wording effect depends on background; interaction size remains imprecise |

All three intervals exclude zero. Within the P2 background, changing just
the PD endpoint pair from P2 to P3 changes ADOPT from 85% to 15%, a 70-point
observed difference. Within the P3 background, the same swap changes ADOPT
from 53.7% to 8.3%, a 45.3-point observed difference. Their difference is the
24.7-point interaction. These within-background differences are explanatory
decompositions of the prespecified contrasts, not extra hypothesis tests.

The exact PD endpoint strings were:

| Version | Low endpoint | High endpoint |
|---|---|---|
| P2 | outcomes predominate; methods carry subordinate but meaningful standing | fair procedure possesses independent normative standing |
| P3 | results dominate; procedural considerations retain secondary though substantive value | adherence to fair procedure carries worth independent of realized outcome |

Both endpoints move together in this design. The result cannot identify
whether the low endpoint, high endpoint, a particular word, or their combination
causes the difference. Likewise, the other-nine manipulation is a bundle:
it does not identify the responsible background parameter descriptions.

## What follows for the project

This fresh controlled test localises a substantial presentation sensitivity to
the PD endpoint pair while showing that surrounding descriptions contribute too.
The original 8/30 equivalence count therefore included a real wording problem;
increasing sample size alone cannot remove the demonstrated effect here.

The earlier P2/P3 ADOPT rates were 32/50 (64%) and 2/50 (4%). The fresh unmixed
A/D rates preserve their ordering but differ in magnitude. These are separate
collections with different seeds/times; no observations are pooled and exact
cross-session rate stability is not established. This single selected profile
cannot diagnose all 30 profiles or establish global encoding validity.

The theory, parameter definitions and original gate remain unchanged. Phase
1.5's current gate is still unmet and Phase 2 remains on hold. A reasonable next
decision is a narrowly specified PD wording control that separates the low and
high endpoint contributions, or a reviewed operational wording revision followed
by independent validation. Neither has been launched or treated as a solution.
Any change to intended theoretical meaning still requires researcher consultation.

## Provenance, cost and limitations

- Frozen [protocol](../PROTOCOL.md), [manifest](../manifest.json), and
  [exact prompts](../HUMAN_REVIEW.md). The original preparation documents
  retain their historical pending status; [recorded approval](../review_approved.json)
  supersedes that status for execution, with unchanged template/message hashes.
- Full numerical result: [factorial_a82caff690cae94b.json](factorial_a82caff690cae94b.json).
- Raw records remain in this experiment's ignored `records/` directory.
  [Checksum inventory](../record_checksums.json) and
  [completion verification](../completion_verification.json) cover all 1,200.
  [Backup metadata](../local_backup.json) identifies the verified ZIP in
  `output/validity_backups`; this is a same-computer copy, not off-device storage.
- Recorded usage: 1,077,000 input tokens, 109,683 output tokens, zero cached
  tokens. Estimated token cost **$1.3013235**, before taxes, from
  [OpenAI's published rates](https://developers.openai.com/api/docs/models/gpt-5.4-mini)
  checked September 10 ($0.75/million input, $4.50/million output).
- Profile/pair selection was post-hoc; this is exploratory diagnosis. The
  binomial model assumes independent responses with stable probabilities in
  each condition. Randomized collection blocks reduce temporal confounding but
  do not establish those assumptions or expose internal model reasoning.
- The planned experiment had weak power for smaller effects in its balanced
  scenarios. Detecting an interaction here does not remove that design limitation
  or justify a claim of adequate power for every other profile.
