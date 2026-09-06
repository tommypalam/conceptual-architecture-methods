# Phase 1.5 execution and handoff

Status: 2026-09-06. The real `_r2` run passed its 10-call operational checkpoint
but subsequently stopped at **8,640/15,000 records** after one terminal HTTP 429
`credit_balance_exhausted` error. It is incomplete and no longer running.
The 8,639 other records and failed call remain preserved, with partial analysis;
no complete sweep or battery verdict is claimed. See [current status](../NEXT_STEPS.md).
The earlier designation contains five invalid-credential failures only.
Both manifests have identical design hashes. Completed phases and pilot archives
retain their existing decisions.

## First experiment: the approved Option-C comparison

The design is 10 parameters x 5 values (0.1, 0.3, 0.5, 0.7, 0.9) x
3 simple problems x N=50 x 2 deliveries = **15,000 independent calls**.
Nine parameters remain at the existing population means. The normative context
is neutral. There is no population redraw or change to Beta marginals, R,
parameter definitions, dilemma text, or directional hypotheses.

| Arm | Messages | Requested answer |
|---|---|---|
| `full_harness` | System profile/context/task; user dilemma | DECISION and REASONING |
| `user_prefix_bare` | Same profile/context/task prepended to user dilemma | Decision label only |

The second arm is the alternative delivery specified in NEXT_STEPS, **not an
established neutral or headroom-preserving treatment**. It retains scaffold
text. Whether it preserves headroom is an outcome. The contrast jointly changes
message role and output format; it cannot identify their separate causal effects.

The default requested model is the snapshot recorded in the existing experiments,
`gpt-5.4-mini-2026-03-17`, with temperature 1.0 and a 600-token output cap in both
arms. Access and exact model identity were verified in the real checkpoint. There is no fallback
to a different model. Root seed 20260604 is the existing Phase 1.5 seed.
Base jobs are deterministically shuffled, with alternating arm order within each
job. Both arms use the same requested seed, without claiming paired random draws
or deterministic API reproduction. Concurrent calls are capped at five.

### Freezing, execution, and resumption

The commands below document preparation and normal checkpoint resumption.
**Do not run the resume command against the failed `_r2` designation:** terminal
failures intentionally block resumption. Record an explicit continuation/restart
protocol after restoring credits; never remove the failed record.

Run commands from the repository root. Supply the API key through the process
environment; do not put it in source files or CLI arguments.

```powershell
# Freeze complete prompts, design, model, and source hashes without API calls.
python -B code/run_validity_sweep.py --provider openai --prepare-only --run-root experiments/phase1_5_encoding_validity/option_c_20260906_r2

# First checkpoint: 10 observations belonging to the same fixed-N experiment.
python -B code/run_validity_sweep.py --provider openai --yes --limit 10 --run-root experiments/phase1_5_encoding_validity/option_c_20260906_r2

# Resume remaining observations without replacing earlier records.
python -B code/run_validity_sweep.py --provider openai --yes --run-root experiments/phase1_5_encoding_validity/option_c_20260906_r2

# Offline scoring, including partial runs.
python -B code/run_validity_sweep.py --score-only --run-root experiments/phase1_5_encoding_validity/option_c_20260906_r2
```

The checkpoint is an operational check of credentials, model identity, and
response integrity. It is not a significance-based stopping rule or a new
calibration sample. No selection of parameters or dilemmas follows from the first
10 decisions. The target remains 15,000 calls.

Every observation stores requested messages, the full returned payload, model
version, timestamps, seed, profile, parsed fields, and an integrity hash. Existing
records and manifests are checked before resumption. Corrupt records cause an
error, not silent omission. A terminal API error or model-version mismatch stops
further dispatch after the current batch; those records are retained and the run
cannot silently resume through the failure. Analysis reports missing and invalid
observations. Analyses are content-versioned and never replace prior summaries.

The existing transport may omit a seed rejected by the provider. Requested seeds
are provenance, not a guarantee of server-side seed support. This limitation also
applies to the previous engine and is not resolved by matching seed numbers.

### Analysis fixed before responses

- Binomial logistic regression per parameter/problem/delivery, with a
  likelihood-ratio slope test and a Wald 95% coefficient interval.
- Wilson 95% intervals for individual decision proportions.
- Cohen's h between extreme parameter values; strict observed monotonicity.
- Existing nine simple-problem directional contrasts from thesis 6.1.1.
- Spec 4.1 criterion: p<0.05, h>=0.20, monotonicity, and the predicted direction.
  P-values remain unadjusted as in the sweep specification; this is not a
  multiplicity-corrected confirmatory claim.
- Incomplete sweeps and cells below 98% valid parsing do not receive an affirmative
  criterion label. The 98% operational tolerance carries forward the pilot's
  quality threshold; failures are disclosed, never replaced.
- Unanimous decisions, separation, and failed fits are explicit statuses rather
  than fabricated zero slopes or reliable finite coefficients.
- Delivery comparison: difference between endpoint rate changes, with conservative
  95% intervals formed from four Bonferroni-adjusted exact binomial intervals.
  These intervals assume independent calls and may be wide.

LL, CS, and AW have no pre-specified directional simple-problem contrast in the
current hypothesis list. Their sweeps are reported descriptively. A missing
prediction is not converted into a discovered hypothesis or a parameter failure.
The runner does not declare Phase 1.5 passed, even if some sweeps meet criteria.

## Remaining battery: pending real sweep results and protocol finalisation

The next three tests remain required. Their new implementation, offline checks,
and pre-collection decisions are described in [phase1_5_followup.md](phase1_5_followup.md).
Their empirical records are not yet complete. The original spec is a plan, not
evidence they ran. The table below preserves the issues these tools address.

| Test | Required work | Issue to resolve before collection |
|---|---|---|
| Reasoning coherence | Select 200 traces; independent blind coder; recover parameter quartiles | Bare-label arm has no reasoning. Most non-swept parameters remain at the same mean, so an unconditional 25% chance baseline across all estimates is inappropriate without accounting for class prevalence. Explicit numerical self-reports also need a declared treatment. |
| Paraphrase robustness | Three semantically reviewed paraphrases plus canonical; ten rotations; three problems; equivalence tests | The planned .8 rotation is not a .7 sweep observation and must not be reused as if identical. Freeze comparison pairs and establish precision for the 10 percentage-point equivalence margin. |
| Numeric/verbal/hybrid | Frozen transformations and graded comparisons for parameters supported by sweeps | A single .8 rotation cannot estimate a within-parameter gradient. Specify multiple values before running; labels and quartile language in the older spec also need consistent operational definitions. |

These are forward protocol issues, not grounds for reopening completed
calibration. Record any resolution before generating the relevant data. Neither
numeric-only success nor failure alone proves conceptual understanding or
stereotype activation; report the joint behavioural evidence.

## Supervisor handoff

After the battery closes, provide the frozen manifests, per-call checksums,
reproducible analysis commands, the parameter-by-test verdict matrix, deviations,
and the unresolved implementation questions for Phase 2. Current code entry points:

- `code/run_validity_sweep.py`: command-line wiring, protocol preparation, scoring.
- `code/engine/validity_sweep.py`: deterministic schedule and immutable execution.
- `code/engine/validity_analysis.py`: statistical summaries without API dependencies.
- `tests/test_validity.py`: experiment-integrity and statistical regression checks.

This keeps the supervisor's implementation work grounded in measured behaviour.
It does not require waiting for the later benchmark or moral-coding phases to
review the orchestration code.
