# Small Claude screen with unchanged approved prompts

Purpose: cheaply test whether the previously observed large PD/S3 wording
dependence is also visible with the existing Claude Haiku snapshot. This is a
development diagnostic, not a full sweep, independent audit or equivalence test.

The researcher explicitly authorised using remaining Claude API usage on
September 11 while preserving original prompts. OpenAI spending remains zero.
Pending any more specific total Claude budget, this study uses a conservative
assistant-set $0.75 local dispatch cap. That is not a claim that the researcher
approved a new total budget. No automatic follow-up spending is authorised.

## Unchanged materials

Copy the exact four baseline message lists from the approved
`axis_instruction_20260910` manifest: canonical and the three previously reviewed
Claude paraphrases. Do not include the unsuccessful added axis instruction.
All system/user strings, roles, definitions, endpoint meanings, profile values,
dilemma wording and response requirements stay unchanged. Original source files
are read-only inputs. Verify source hashes, approval hash and exact message/profile
equality before dispatch and scoring. No new paraphrases are generated.

Claude transport places the same system content in Anthropic's system field;
the user content is unchanged. This is a model-plus-provider diagnostic, not an
isolated causal comparison of model weights. Historical OpenAI observations are
not pooled or used as concurrent controls. Haiku generated the prior paraphrases;
it is now the behavioural subject, not an independent judge of their quality.

## Fixed allocation and cost

- Model: `claude-haiku-4-5-20251001`; accessible in the read-only model lookup.
- Configuration: neutral; one fixed ten-parameter profile, PD=.8; problem S3.
- Four formulations, 20 calls each: 80 calls total; no parameter sweep.
- Twenty blocks each contain all four formulations, shuffled with seed 20260914.
  This seed controls schedule order only; Anthropic receives no sampling seed.
- Temperature 1, maximum 600 output tokens; the original 2–3-sentence response
  instruction is preserved. No added brevity instruction changes the prompt.
- Concurrency 2, one transport attempt, SDK retries disabled, 90-second timeout.
  Stop after the active batch on terminal API/model error. Preserve failures;
  no in-place retry, replacement or automatic continuation.
- Expected token cost roughly $0.15–$0.25; $0.75 dispatch guard. Before every
  batch, reserve UTF-8 input bytes plus overhead and the full output allowance.
  Provider billing and unreported failed-request usage remain authoritative.
  Pricing checked September 11: $1/million input, $5/million output, from
  [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing).

## Analysis fixed before outcomes

Report every cell's recorded/valid/invalid/missing counts, ADOPT proportion and
pointwise Wilson 95% interval. The sole primary contrast is P2 minus P3, selected
from the prior development evidence. Construct two exact 97.5% binomial intervals;
subtract their opposing endpoints for a conservative interval with at least
95% coverage for the difference. Include all possible binary completions of
unknown decisions by taking their interval envelope at planned N=20.

A complete, sufficiently valid screen detects a gross wording failure only if
that primary interval lies wholly above +.10 or below -.10. Require the original
98% per-cell validity floor; at N=20 that requires all 20 valid. Other formulations
are descriptive controls, not additional primary tests. Report all-formulation
<=5% or >=95% observed saturation separately as uninformative for discrimination.

No detected failure means only that this small screen did not detect a gross
failure. It does not establish equivalence, continuous ethical encoding, model
superiority or a Phase 1.5 pass. There is no outcome-dependent sample increase,
full battery, hypothesis revision or new prompt following this diagnostic.

## Verification and review

Two offline behavioural tests passed: complete 80-call mocked execution with
unchanged messages, blocked zero-budget dispatch, no-call resume, exact interval
quantiles and unknown-decision envelope, preserved failures and failed-resume
refusal. Mock outcomes are not empirical evidence. Original messages, model IDs,
record hashes, counts and ZIP payload bytes will be checked after collection.
Raw responses remain local; inventories and reports are committed separately.

The theory, original validity gate and researcher consultation requirements
remain unchanged. This small provider screen does not replace the spec 4.5
review before substantial lexical re-engineering or full revalidation.
