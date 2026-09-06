# Remaining validity implementation

2026-09-06. Phase 1.5 remains open. These tools implement later tests; their
offline tests are not empirical evidence that the battery passed. The interrupted
Option-C experiment and its source files remain frozen; see [current status](../NEXT_STEPS.md).

## Entry points for code review

- `code/run_validity_followup.py`: numeric/verbal/hybrid rotations, optional
  multi-value gradients, and reviewed paraphrase comparisons. Mock by default.
- `code/run_validity_claude.py`: independent Claude generation, blind audit
  preparation, resumable coding, and audit scoring. Explicit model ID required.
- `code/engine/validity_variants.py`: transformations and paraphrase validation.
- `code/engine/validity_coherence.py`: deterministic selection and audit statistics.
- `code/engine/validity_equivalence.py`: constrained-score binomial TOST.
- `code/engine/validity_followup.py`: frozen designs, execution, and analysis.
- `tests/test_validity_followup.py`: offline integrity and inference tests.

## Decisions fixed before follow-up data collection

All behaviour experiments retain the source model snapshot, temperature, token
budget, neutral context, dilemmas, means, and full-harness response format.
Real dependent runs refuse an incomplete source sweep. Existing failures are
preserved; resuming over a terminal failure requires a reviewed new designation.
Frozen request content and source hashes prevent silent protocol changes.

The spec names six verbal levels while calling them quartiles. The verbal
prompt transformation uses six equal-width intervals on [0,1], with 1 included
in the final interval. The reasoning audit separately uses four actual quartiles.
Numeric-only prompts retain parameter names/values and omit endpoint definitions.
Verbal-only prompts retain endpoint definitions, but replace trait values with
words. These contrasts do not establish conceptual understanding on their own.

The .8 rotations are new observations, never substitutions of the .7 sweep.
Rotations cost 4,500 calls at N=50 (three representations). Three paraphrases
add 4,500, sharing the 1,500 canonical rotation calls. Thus these two tests use
9,000 calls together. A separate optional numeric/verbal five-value gradient
extension adds 15,000 calls, reusing only exact-protocol hybrid source sweeps.
The one-value rotations cannot estimate a within-parameter gradient. No automatic
launch of the optional extension or assertion of a 10,000-call total budget.

Each paraphrase must preserve structural placeholders, parameter identities, and
endpoint directions. Word-set Jaccard must be below .4 per parameter. A real
human must review semantic equivalence and record their name and approval against
the exact template hash. The generator's claimed identity is replaced by the
returned API model ID. Generated material is explicitly marked unapproved.
Lexical checks do not certify semantics.

Paraphrase equivalence uses all six pairs among four formulations at each of
30 parameter/problem cells: two one-sided constrained-binomial score tests,
10 percentage-point margin, alpha .05, Miettinen-Nurminen variance correction.
At least 24/30 cells must establish all-pair equivalence, with complete sampling
and at least 98% valid responses in every cell. At N=50, equal observed rates
near .5 alone are too imprecise to establish this equivalence margin. Failure
to establish equivalence does not establish a meaningful difference.
Implementation follows the [score TOST definition](https://www.statsmodels.org/dev/generated/statsmodels.stats.proportion.tost_proportions_2indep.html).

The 200-item audit samples only eligible full-harness reasoning, without selecting
by decisions or substantive content: 20 per parameter, four per sweep value,
balanced across problems within one observation, seed 20260604. Preparation waits
for the full source. The public pack contains opaque IDs, reasoning, and coding
definitions; the private key contains source links and true quartiles. Each Claude
request receives definitions and one reasoning text, with no true values or
swept-parameter identity. Decimal literals in reasoning are flagged and retained;
do not silently edit or exclude them after seeing scores.

Report literal spec thresholds plus class prevalence, majority baseline, confusion
matrices, and active-parameter balanced accuracy. A supplementary permutation test
shuffles true active-parameter quartiles within problems (1,999 resamples). This
addresses the confound from nine fixed means. The report requires scientific review
even if literal aggregate thresholds pass. Confidence is recorded, not used to
filter favourable estimates. Missing/abstained quartiles count as incorrect.

Gradient comparisons report absolute fitted logit-slope ratios and prespecified
direction agreement only where the original sweep criterion is supported.
The >=.5 ratio is a point-estimate diagnostic, not a confidence-bound guarantee.
Pinned/separated fits and absent directional hypotheses remain unassessable.

## Commands (from repository root)

Offline smoke test, no credentials or paid calls:

```powershell
python -B -m pytest tests/test_validity_followup.py -q -p no:cacheprovider
python -B code/run_validity_followup.py --source-root experiments/phase1_5_encoding_validity/option_c_20260906_r2 --run-root output/validity_followup_mock --experiment rotations --n 1
```

Independent generation request is also exported in
`docs/validity_paraphrase_request.json`. Claude uses the existing Anthropic
transport in `llm_client.py`; install the optional `anthropic` package in the
project environment before real calls. No dependency change is needed for offline
tests. API credentials are read from `ANTHROPIC_API_KEY`, never from project files.
Use a verified explicit snapshot model ID for `$claudeModel`; no default silently
chooses or replaces one. [Claude Messages API](https://platform.claude.com/docs/en/api/messages/create)
provides the returned model ID recorded with each response.

```powershell
$env:ANTHROPIC_API_KEY = [Environment]::GetEnvironmentVariable('ANTHROPIC_API_KEY','User')
python -B code/run_validity_claude.py run --task paraphrases --model $claudeModel --run-root experiments/phase1_5_encoding_validity/claude_paraphrases_v1 --yes
```

After the full source sweep finishes:

```powershell
python -B code/run_validity_claude.py prepare-audit --source-root experiments/phase1_5_encoding_validity/option_c_20260906_r2 --out output/validity_audit_pack
python -B code/run_validity_claude.py run --task audit --model $claudeModel --blind-pack output/validity_audit_pack/blind_pack.json --run-root experiments/phase1_5_encoding_validity/claude_audit_v1 --limit 1 --yes
python -B code/run_validity_claude.py score-audit --answer-key output/validity_audit_pack/private_answer_key.json --run-root experiments/phase1_5_encoding_validity/claude_audit_v1
```

Omit `--limit 1` to resume the full audit after operational verification. Do not
change prompts/model after observing coding accuracy. For behaviour comparisons,
use `--provider openai --yes` only after source completion, and `--prepare-only`
to freeze without calls. Paraphrases require `--paraphrases PATH` to the reviewed
bundle; score with `--baseline-root PATH` pointing to the matching rotations run.
All raw call records remain local artifacts; commit manifests and summaries only.

Remaining empirical work: complete the source sweep; configure/verify the Claude
credential and exact model; generate and review the three paraphrases; run the
independent audit and robustness comparisons; assess gradients if pursued; then
review the combined evidence. There is no automatic Phase 1.5 pass shortcut.
