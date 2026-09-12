# Phase 2 exploratory pilot — prospective protocol

Prepared 2026-09-12 on `phase2-design-20260912`, following the researcher's
instruction: “first a small exploratory test, then we draw conclusions and run
the conclusive test.” This authorises the small pilot discussed in the session.
This document is frozen by a source-and-asset manifest before the first call.
That is a local prospective record, **not public preregistration**.

## Question and scope

Does the complete ten-parameter profile-injection package change individual
choices and group processes relative to contemporaneous context-only controls?
Are the orchestration, response format, variability and costs suitable for a
separate confirmatory study? All ten coordinates, original Beta marginals and
correlation matrix remain unchanged. This uses the existing LPM population
sampler and a prospective implementation of the specified Agents-of-Chaos-inspired
round protocol. Direct integration of either external project's library is not
claimed. No tools or real-world actions are available to simulated agents.

The pilot does not measure intrinsic understanding, human resemblance, or moral
goodness. It does not compare against an implemented postfilter. The encoded arm
supplies the profile before generation and preserves the model's output exactly.
The E/U contrast includes profile instructions and added prompt text; it cannot
isolate semantics, individual parameters, or provider-internal mechanisms.

## Fixed allocation and randomisation

- Population: 50 new Gaussian-copula profiles; root seed **2026091202**.
- Simple: S1, S2, S3; anchors **00100** and **11011**; E (encoded) and U
  (context only); 50 responses per cell: **600 calls**.
- Groups: five matched groups per problem. C1 has five agents and up to five
  rounds; C2 six agents and five rounds; C3 four agents and six rounds.
- Every group receives E and U in both anchors plus B, a no-profile neutral
  bridge. Same membership, CEO, private-evidence assignment and matched tie
  randomisation across the five conditions. Separate conversations throughout.
- Groups use nonoverlapping profiles within each problem, sampled without
  selecting profile values; profiles may recur across problems. Group blocks
  and condition order are deterministically shuffled. No outcome-based ordering.
- Maximum group calls: 5 × 5 × (25 + 30 + 24) = **1,975**.
- Total: **2,575 maximum calls**. C1 can stop at valid unanimous consensus.
- Independent per-call seeds are derived from the root and full slot identity.
  Population, schedule, analysis and tie seeds are separately derived. A seed is
  a reproducibility input, not a guarantee of deterministic provider output.

Only the two existing anchor definitions are used. The proposed ten-environment
repair remains separate; these anchors cannot identify five separate axis effects.
The existing configuration file has no authored practical descriptions, so the
pilot freezes the inherited engine's generic HIGH/LOW structural-description
fallback. Those abstract labels are a limitation of ecological interpretation;
the pilot does not validate concrete political institutions or silently author
new parameter-to-action mappings. Review richer descriptions before confirmation.
The future confirmatory population will use a different frozen root and no pilot
responses. No pilot profiles, wording variants or outcomes are selected for reuse.

## Prompts and state

Use the exact dilemma bodies loaded from `experiments/phase0b_calibration/questions`.
E uses the existing canonical system profile and context. U removes the profile
block and uses a task instruction referring only to the available situation and
context. Both request the same simple response format and length. B uses the
existing explicitly balanced neutral-context wording, never configuration 00000.
Roles and round instructions are equal across arms; profiles are reinjected on
every E round. Shared state contains previous rounds only.
The simple explanation instruction is symmetrically “2-3 sentences explaining
why” in both arms, so U is not asked to use a profile it did not receive. This is
a prospective wrapper change; the canonical file and locked dilemmas are intact.

C1 requires five valid votes for consensus or a final group outcome. C2 requires
five valid non-CEO binding votes; the CEO never votes in the tally. C3 requires
four valid binding votes; only an actual 2–2 tie receives a seeded random outcome.
Missing votes produce an incomplete outcome, never a rejection, consensus or tie.

C2 restores the specification's amendment mechanism: the locked question is the
original proposal; the final vote concerns that proposal plus CEO-adopted amendments.
Agents propose one textual amendment per round, identified by round and agent.
The CEO can adopt previously visible proposals in rounds 2–4. Proposals and active
amendments persist verbatim; adoption has no invented numerical consequence.
Incompatible or vague amendments are retained and flagged for review, not silently
resolved by the engine. This tests deliberation about a working plan, so it is not
an exact repetition of the single-call Phase 0 “as proposed” task.

C3 uses the 24 fictional scenario supplements in `evidence_schedule.json`:
eight favourable to each option, eight non-directional, distributed over rounds
1–5 with the existing item/round/polarity map. Counts do not establish equal
evidential weight. No concealed correct answer exists. No outside replication
result or resolved long-term efficacy is supplied. Polarity is analysis metadata
and never appears in agent prompts. Every item goes directly to 1–3 agents; the
frozen allocation is checked to ensure no agent directly receives all 24.
All privately received facts persist. Legitimately cited or explicitly shared
items become public only after the round barrier. Unknown citations are logged;
their purported evidence content is never injected as authentic evidence.
An item mentioned in a public transcript is distinguished from an authenticated
item whose content was legitimately disclosed. Semantic leaks without item IDs
require subsequent transcript review; the automated audit cannot detect all leaks.

The structured transcript preserves votes, actions, amendment text and evidence
IDs. Reasoning excerpts are limited to 360 characters per response; full raw
responses remain in the ledger. Excerpts are disclosed as truncated. Evidence and
amendments have separate persistent state and are not truncated with reasoning.
This is an explicit compression limitation for interpreting persuasion or memory.

## Execution and budget

Pinned model `gpt-5.4-mini-2026-03-17`; temperature 1; maximum completion tokens
600; reasoning effort `none`; standard service tier; OpenAI chat completions.
No model, prompt, settings or evidence substitution once live collection begins.
One attempt per slot, SDK retries disabled, bounded concurrency six. No automatic
repair prompts. A failed call is preserved. Transport failures stop execution
after the current batch; completed responses remain reusable. Unknown dispatches
block automatic continuation. Any linked recovery requires its own manifest.

Illustrative generation estimate is about $6; **$10 is the pilot operational
ceiling inside the researcher's $100 absolute new-package cap**. The estimate is
not a guarantee that every planned call fits. Before every call, reserve an upper
charge based on UTF-8 input bytes plus 512 framing tokens and all 600 output tokens,
at uncached rates $0.75/$4.50 per million with 10% price allowance. Completed calls
are charged conservatively at observed usage without cached-input discounts.
Unresolved calls retain their entire reservation. Each next dispatch must fit
within $10 including all in-flight reservations. If it cannot, stop and report
the incomplete allocation; never shrink, silently exclude or replace a cell.
Unused pilot allowance is not automatically spent. No other package run may
execute concurrently against this budget. Provider balance, taxes and unrelated
account spending are not verified by this local ledger.

The request, slot identity, seed and reservation are persisted before dispatch;
the full response and usage immediately after return. Records are write-once and
integrity checked on replay. A process lock prevents concurrent launch. Resume
reconstructs state from recorded responses and must produce identical requests.
Never erase an unresolved dispatch to force a retry. Raw data live in ignored
`data/raw/phase2_exploratory_20260912`; commit the protocol, source, population,
manifest, diagnostics, summaries and archive checksums.

Pricing verified against [the official model page](https://developers.openai.com/api/docs/models/gpt-5.4-mini)
on 2026-09-12. The 10% allowance is conservative local accounting, not a statement
that the provider will apply a regional surcharge to this account.

## Analysis fixed before observation

Report every planned cell, missing/invalid responses and terminal API failures.
Simple descriptive endpoint: probability of the first canonical label (A,
FORMAL_REPORT, ADOPT), Wilson 95% interval per cell. Paired E−U risk differences
and anchor differences use whole-profile bootstrap resampling, 10,000 draws,
with all four condition observations kept together. Paired contrasts use complete
pairs with counts disclosed, plus worst-case bounds assigning missing outcomes
both ways. No confirmatory p-values or declaration of ethical superiority.
Ceiling cells and degenerate bootstrap intervals are explicitly identified.

Group unit is the independent matched group, not each utterance. Report final
choice with Wilson intervals across the five groups per cell; exact paired
group differences are descriptive and five groups are too few for a reliable
effect-size or power estimate. Report missing groups, consensus rounds, C2
proposals/adoptions and C3 authenticated sharing/unknown citations. Do not pool
utterances or problems as independent replicates. Vote changes are descriptions,
not proof of bias or architectural noise. Report C3 pre-tie tallies separately.

Review a fixed outcome-independent simple subset (profile IDs 1, 6, ..., 46 in
every cell) and group 1 in all 15 group cells for task/state issues. This manual
inspection may identify hypotheses, but it cannot validate an ethical coding
scheme or be called blinded human coding.

Progression is based on engineering and design adequacy, not favourable effects:
verify request/provenance integrity, matching and accounting; describe parse,
truncation, saturation and missingness; inspect whether group mechanisms actually
operate. Then write an exploratory assessment and freeze a separate confirmatory
question, estimator, controls and sample-size calculation. If a pilot reveals a
material defect, preserve it and repair prospectively before confirmation.

## Relation to the original specification and review

The researcher explicitly chose this exploratory-first sequence after reviewing
the original roadmap. This prospective pilot is a bounded preliminary study,
not release of the original full Phase 2 or an original Phase 1.5 battery pass.
The original specification's moral-manual/preregistration-before-Phase-2 schedule
is deferred for this behavioural pilot under that instruction. No moral category
is operationalised or scored here. The coding manual and human sign-off remain
required before moral scoring; public preregistration and a justified analysis
plan remain prerequisites for the future confirmatory claims.

Five synthetic perspectives on this decision (not external expert approval):

- Linden: profile-sensitive decisions cannot establish understanding or goodness;
  keep those claims separate and do not equate obedience with ethical success.
- Osei: an exploratory sample diagnoses the task and harness; retain all six
  tasks and state that human comparison has not yet occurred.
- Tanaka: pair profiles and groups, preserve missingness, and resist powering the
  final study from the most favourable of noisy pilot effect estimates.
- Renna: fix upstream state delivery before interpreting social effects; freeze
  controls, generation settings and evidence before observing responses.
- Okafor: retain LPM sampling and explicit round barriers, and make every paid
  dispatch recoverable without duplicate requests or hidden retries.

Disagreement: collecting behavioural data before the originally scheduled moral
manual trades early empirical learning against completing all original gates.
Resolution: follow the researcher's exploratory-first instruction, disclose that
schedule amendment, withhold moral scoring and full-phase claims, and require a
separate confirmatory freeze after the pilot assessment. No theoretical mapping,
distribution, benchmark, locked question or full configuration subset is changed.
