# S3 endpoint sensitivity diagnostic

Prepared September 11 before dispatch. Same model, original dilemma, endpoint
meanings, response schema and previously prepared overlays. New designation;
no frozen source code, prior response or original prompt is modified.

## Purpose and allocation

The previous screen narrowed the targeted wording gap, but repetition alone
also did so and grounding favoured WAIT. Check whether the candidate still
responds to parameter values before spending on equivalence confirmation.

**540 calls = 3 arms x 6 profile cells x 30 repeats.** Every call is an independent
single-decision request, not a new randomly drawn population agent.

| Probe | Wording | Values | Interpretation |
|---|---|---|---|
| PD/S3 | Previously approved P2 and P3 | .1, .9 | Descriptive parameter response and wording gap; no prespecified PD/S3 direction |
| MoR/S3 | Canonical | .1, .9 | Previously prespecified positive direction for ADOPT; historical full-harness criterion met |

All other nine parameters stay at their original source means within each
probe. Therefore the MoR cells use PD's source mean, not the preceding screen's
PD=.8. This is the original one-parameter-at-a-time design, not a combined
PD/MoR profile. Canonical and P1 are not tested for PD here; that limited screen
coverage cannot support all-wording equivalence or removal of those conditions.

Arms are original, repetition alone, and repetition plus grounding. Copy each
arm's user message exactly from the completed 450-call screen; the only PD
system-message edits substitute the displayed numeric value from .80 to .10
or .90. MoR system messages and profiles are copied exactly from the original
September 9 full-harness sweep. No new instruction or action-scoring rule.
Exact cells are frozen in [request_preview.json](request_preview.json) and
[manifest.json](manifest.json). The optional tool is not used.

Model `gpt-5.4-mini-2026-03-17`, neutral normative context, temperature 1,
600 maximum completion tokens, root seed **20260916**. Thirty shuffled complete
18-cell blocks, concurrency 3, unique derived requested seeds. Requested seeds
do not guarantee provider reproducibility. No outcome-based allocation changes.

## Budget and transport

Allocate **$4 maximum** from the existing $9 total new allowance. The previous
screen's recorded full-rate token estimate was $0.5022225; no requests remain
pending there. This full new schedule conservatively reserves **$3.652020**.
Even the previous full reservations ($2.867265) plus this screen's $4 cap remain
below $9. The cap uses reservations, not just successful reported usage.

The frozen prior screen provides the executor, record verification, exact
single-attempt OpenAI transport, crash reservations, unknown-sensitive interval
calculation and raw-backup writer. No monkeypatching or modification of those
components. The new wrapper provides the design, analysis and entry point.
Its 30-repeat contract is explicitly checked against the reused scheduler.

One HTTP attempt per slot, no SDK retries or parameter fallback. Stop after the
active batch on API/model/provenance/usage failure or before a reservation would
exceed the cap. Preserve every failure and ambiguous dispatch; no in-place
replacement. Record messages, profiles, seed, ID, raw response and usage. Verify
all raw ZIP bytes; same-computer backups only, no publication.

## Analysis and decision rules

Primary: **grounding-arm canonical MoR .9-minus-.1 ADOPT-rate difference**.
Two exact 97.5% binomial intervals yield a conservative >=95% difference
interval, including every invalid or missing decision through the unknown
envelope. Complete allocation and >=98% valid per cell (all 30 at this N) are
required for an informative completed-screen classification.

- Lower bound >0: positive response detected locally, not validated encoding.
- Upper bound <0: opposite response detected locally, not a theoretical refutation.
- Otherwise: sensitivity unresolved; do not equate non-detection with zero effect.

Original/repetition MoR endpoint contrasts, PD endpoint contrasts within each
wording, and P2-minus-P3 gaps at both PD values are secondary/descriptive. Their
intervals are conservative nominal >=95% per contrast, not adjusted across
the secondary family. No causal superiority between arms follows from a
significant effect in one arm and a non-significant effect in another.

This is not the original five-value monotonicity, fitted-slope or gradient-retention
test. Two endpoints cannot establish continuous encoding, multi-parameter joint
behaviour, active-trait recoverability, or paraphrase equivalence. Report endpoint
rates and floor/ceiling concerns even when the primary interval is positive.
Failure of the original MoR control to show response here makes diagnosis less
clear; it does not retrospectively change the historical result.

No new no-profile calls are included: prior controls remain separate evidence
about the selected overlay at one condition, not pooled or treated as concurrent
controls for this new profile grid. Phase 0c's naked baseline is not transplanted.
Fresh confirmation remains necessary after selecting any candidate.

## Limits and follow-up

The researcher requested trying defensible approaches first and documenting a
limit if needed. A finite screen can identify a practical limitation of this
model/delivery/task combination. It cannot prove a fundamental hard cap on
encoding ethical concepts. Budget exhaustion or non-significance is not such
proof, and the equivalence margin or phase gate will not be loosened afterward.

Complete and review this fixed diagnostic before another paid allocation. A
promising result warrants a small intermediate-value/headroom check before any
full battery. A flat or ambiguous result warrants reassessing delivery and
measurement rather than automatically increasing N. No automatic expansion.

Preparation is authorised by the researcher's "go for it" instruction and the
standing $9 ceiling. Any exact payload approval required by automatic review
must be recorded separately; no separate human signature is inferred here.

```text
python -m pytest tests/test_validity_evidence_sensitivity.py -q
python code/run_validity_evidence_sensitivity.py --run-root experiments/phase1_5_encoding_validity/evidence_sensitivity_20260911 --prepare-only
python code/run_validity_evidence_sensitivity.py --run-root experiments/phase1_5_encoding_validity/evidence_sensitivity_20260911 --yes
```
