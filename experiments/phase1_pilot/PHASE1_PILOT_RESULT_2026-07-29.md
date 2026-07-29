# Phase 1 — Pilot Result (2026-07-29)

Operational pilot (spec Part 3). Verifies the pipeline end-to-end; does NOT test
encoding validity (that is Phase 1.5).

## Configuration
- Problems: **S3** (PRIMARY tier — clean pipeline check) and **S2** (spec §3.1's
  choice — to document harness behaviour). Findings-aware deviation from §3.1
  (which picks S2 alone); rationale in PHASE0_CLOSURE_2026-07-29.md.
- Config: `10011` (Freedom=1, Justice=0, Authority=0, Care=1, Loyalty=1) — the
  closest binary encoding of §3.1's "authority-low, justice-low, otherwise
  neutral" (binary codes cannot express per-axis neutral; documented choice).
- N = 50 agents/problem, free-drawn from the Gaussian copula. Full Phase-2
  harness (parameters + normative context + DECISION/REASONING). Recalibrated
  locked question set. Temperature 1.0. 100 calls.

## Five diagnostics (spec §3.2)

| # | diagnostic | S3 | S2 |
|---|-----------|----|----|
| 1 | parse integrity (>=98%) | 50/50 = 100% PASS | 50/50 = 100% PASS |
| 2 | decision distribution (not 100/0) | ADOPT 35 / WAIT 15 (0.70) PASS | REPORT 4 / LOCAL 46 (0.08) skewed but not unanimous |
| 3 | reasoning recovery (>=3/10 params) | PASS — traces cite care, loyalty, freedom, process-dependence, legitimacy, justice | PASS — traces cite process-dependence, response-threshold, moral-scope |
| 4 | logical consistency (<10% mismatch) | PASS — decisions match reasoning | PASS — decisions match reasoning |
| 5 | implementation health | PASS | PASS |

## Verdict: PILOT PASS

All operational gates pass. The pipeline runs end-to-end without intervention;
outputs are well-formed; storage/immutability hold. Parse integrity is perfect.

S2's skew (0.08 toward LOCAL) is the EXPECTED harness effect (Phase 0b: S2 is
the most harness-fragile problem; 0c naked baseline 0.19). It is not a pipeline
failure — parse, reasoning recovery, and logical consistency all pass on S2. It
confirms the harness collapse carries into the full Phase-2 config, as predicted.

## Encouraging early signal (not a formal test — that is Phase 1.5)

The S3 REASONING traces show agents responding to the INJECTED CONFIG and
PARAMETERS in the predicted directions:
- ADOPT agents invoke the high axes: "high-freedom, high-care, high-loyalty
  environment", "peer legitimacy", "high process sensitivity".
- WAIT agents invoke the low axis: "low-justice … avoid imposing a disruptive
  change", "process obligations matter more than the possible upside … with low
  justice and authority".

Reasoning is decision-consistent and parameter-referencing — the earliest
indication that the encoded architecture is doing work. Phase 1.5 will test this
formally (single-parameter sweeps, paraphrase robustness, verbal/numeric
ablation).

## Logical-consistency audit (diagnostic 4, manual)

Sampled traces show reasoning that entails the stated decision in every case
inspected (no post-hoc mismatch): S3 ADOPT<->pro-change axes, S3 WAIT<->low-justice
caution, S2 LOCAL<->"contestable, minor, correctable, lowest responsible level".
Mismatch rate well under the 10% threshold on the sample.

## Outcome
Pilot PASS. Cleared to proceed to Phase 1.5 (encoding-validity battery, spec
Part 4) — the framework's primary hard gate. Note Phase 1.5 runs on the SIMPLE
problems (S1-S3) under NEUTRAL configuration; the harness non-neutrality finding
and the tiered baselines (PHASE0_CLOSURE) carry forward as context.
