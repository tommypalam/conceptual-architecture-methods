# Fixed-specification tool delivery: candidate screen

Prepared 2026-09-11 on `phase1-5-tool-delivery-screen`. No empirical result is
implied by the protocol or offline tests. Original Phase 1.5 remains unmet.

The researcher requested a concrete repair, retaining the theory and locked
prompts. Thesis v0.6 sections 4.1 and 8.2 explicitly provide a tool-injection
alternative. This is an isolated delivery prototype for that route, not the
complete distribution-sampling tool or a change to the simulation engine.
Controlled sweeps assign a fixed profile; a tool read must never redraw it.

## Manipulation and exact review scope

The control sends the original two messages. In the candidate, a short new
system bridge requests `read_agent_specification`, a real function with no
arguments. The function returns the **entire existing system specification
verbatim**, including all ten parameter values and descriptions, neutral
context, and task instructions. The locked user message stays byte-identical.
The actual model tool call is returned in the transcript with its actual ID;
the next API call produces the decision. No model-generated specification is
substituted. No answer, trait weight, behavioural mapping, normalization,
feedback, correction, profile selection or new parameter is supplied by the tool.

The exact bridge and function schema are in [HUMAN_REVIEW.md](HUMAN_REVIEW.md).
All rendered source messages are in [request_preview.json](request_preview.json).
This preserves source wording, **but changes the active harness**: delivery
role, position, extra system instruction and turn count change together.
Previous human approval of endpoint meanings does not mean this new bridge was
previously reviewed. The optional evidence-card tool remains unrelated/inactive.

## Allocation and budget

- Neutral configuration; GPT-5.4 mini snapshot `gpt-5.4-mini-2026-03-17`.
- MoR/S3 and PD/S3, each at .1 and .9; the other nine retain original means.
- Canonical plus all three human-approved r5 wordings; system versus tool delivery.
- 32 conditions, 10 fresh decisions each: **320 decisions, at most 480 API calls**.
- Temperature 1, final maximum 600 tokens; retrieval maximum 128 tokens.
- Root seed 20260924; ten shuffled complete blocks, concurrency 3. Every API
  request has a distinct derived requested seed. No deterministic-output claim.
- Cap **$3.50**; conservative full-dispatch reserve **$3.28692**. Prior conservative
  charge $3.89954775, including the earlier unknown timeout reservation; cap plus
  prior charge stays below the latest $9 allowance. Provider balance unverified.
- Known prices retained from the September 11 ledger: input $0.75/M tokens,
  output $4.50/M. No cached-token discount assumed in estimates/reservations.

MoR/S3 was selected for previously observed parameter sensitivity; PD/S3 for
previously observed wording differences. Both are **development cases**, not
held-out validation. This is not another joint PD/MoR-corner experiment: one
parameter varies while the other remains at its original mean. Previous runs
are not pooled into this screen. The paused 900-call confirmation stays paused.

## Fixed primary and decision rule

For each delivery, average the squared differences between every pair of four
wording-specific ADOPT probabilities, equally across the four parameter/value
contexts and all six pairs. Estimate each squared difference without binomial
sampling bias:

`k_a(k_a-1)/(n(n-1)) + k_b(k_b-1)/(n(n-1)) - 2(k_a/n)(k_b/n)`.

Do not clip negative estimates. Primary: **tool minus system** average squared
wording difference; negative favours the candidate. Use 10,000 stratified
binomial bootstrap replications, percentile 95% interval, seed 20260925.
This small-N bootstrap is an exploratory screen, not an exact significance test
or equivalence interval. Boundary cells can understate bootstrap uncertainty.

The candidate merits broader confirmation only when all apply:

1. All 320 decisions and 480 expected API records are valid, with verified provenance.
2. The primary bootstrap interval lies wholly below zero.
3. Canonical tool MoR endpoint difference is at least +.20 and retains at least
   half a **positive** concurrent canonical system difference.
4. Mean tool MoR endpoint difference across all four wordings is at least +.20.

The sensitivity safeguards are screening point-estimate requirements, not
validated effect bounds. Report all cells and intervals, regardless of outcome.
Failure to meet this rule means **no scale-up support**, not proof that tools
cannot work. Meeting it warrants a separate broader confirmation design only.
No automatic full sweep, changed threshold, partial-pass or Phase 2 launch.
No PD behavioural direction is newly hypothesised. With only two endpoints,
monotonicity is not assessed at all.

## Provenance and stop rules

The runner stores exact serialized JSON request bodies before dispatch, then
the full provider response, API/request IDs, usage, timestamps, model, seed,
and immutable decision links. Credentials and request headers are not stored.
Local tests compare canonical payload objects to the existing OpenAI SDK.
The runner uses direct HTTP with no automatic retries; this transport difference
is disclosed and shared across both concurrently collected arms.

One attempt per API slot. A model, API, usage, wire, tool-shape or parsing failure
stops the current batch and invalidates this screen. A retrieval failure does
not trigger a decision call. The assistant tool-call envelope must fit 1024 UTF-8
bytes; a larger envelope is preserved and rejected before further spending.
No retries, replacements or automatic partial-run recovery. Unknown usage keeps
its reserved charge. Data and failures are saved locally with a verified ZIP;
that is a same-computer backup, not off-device protection.

## What would still be required

The earlier 23/30 versus 8/30 canonical repeat discrepancy remains unexplained.
Existing audits found no local source/record/parse mismatch. Exact wire logging
improves the new experiment's auditability; it does not diagnose that old change.

This screen cannot clear 24/30 paraphrase equivalence cells, establish graded
response curves, representation retention, active-trait recoverability, ethical
understanding, or invariance to the new harness. A promising candidate still
requires null-harness checks, wider prospectively fixed tests and the existing
validity battery. Constant output is not successful encoding. Source theory,
Phase 0 prompts, distributions, correlations and gates remain unchanged.

API mechanics were checked against [official OpenAI function-calling documentation](https://developers.openai.com/api/docs/guides/function-calling)
on September 11; this supports the call/return implementation, not an expectation
of better ethical encoding.
