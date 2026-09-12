# Phase 2 fresh-sample behavioural confirmation

Prospective local protocol, 2026-09-13. Researcher instruction: "lets go ahead and complete phase 2 run it".
This implements the exploratory-first follow-up discussed in the pilot's CONFIRMATION_NEXT.md.
It completes the amended two-anchor behavioural Phase 2, not the original ten-environment battery.
The protocol, population, schedule, source and runtime are hash-frozen and committed before paid collection.
There is no public preregistration; a local prospective freeze must not be described as one.

## Questions and inference

Primary: does the full encoded ten-parameter profile change individual choices relative to context alone?
E receives canonical profile plus context; U receives context with no profile. Both receive the exact same
locked dilemma and output instructions. This estimates a whole prompt/profile intervention, including its
extra information and length. It does not identify each coordinate, internal ethical understanding,
superiority to postfilters, or moral goodness. No postfilter comparator is collected.

All ten LPM parameters, their Beta marginals, Gaussian copula R, canonical definitions and locked six
dilemmas are unchanged. The existing anchors 00100 and 11011 change all five societal bits together:
their differences identify context packages, not separate political-ethical axes. The original broader
configuration proposal remains unperformed. This narrower follow-up follows the reviewed small-study sequence.
The custom group engine preserves Agents-of-Chaos-inspired interactions; direct external framework
integration is not claimed. Human resemblance is Phase 3; human-validated dual moral coding is Phase 4.
The earlier requirement for a moral manual before behavioural collection is deferred by the researcher's
exploratory-first sequence; human approval is still required before assigning moral scores.

## Fixed sample and collection

- Root seed 2026091302; 400 fresh copula profiles, no filtering/redrawing. Verify no exact duplicate
  vectors with the 50-profile pilot. Same agents across S1/S2/S3, both contexts and both arms: 4,800 calls.
- Twenty matched groups per task: C1 five agents, C2 six including one fixed CEO, C3 four.
  Membership is nonoverlapping within each task; agents may recur across tasks and individual tests.
  Membership, CEO, evidence delivery and tie seed are fixed across each group's five conditions:
  E/U in both anchors plus B (profile-free balanced neutral context). Total 300 group runs.
- C1 maximum five rounds with early unanimous termination; C2 five rounds with five non-CEO final
  votes; C3 six rounds with random tie-break only for complete 2-2 final votes. Maximum 7,900 group calls,
  12,700 overall. Incomplete final voting produces a missing outcome, not a majority of survivors.
- Independent conversations, profile reinjected every group round; matched condition orders and block
  schedule randomized deterministically. Within-round requests see the same preceding state; changes
  become visible only next round. Reasoning excerpts retain 360 characters; full responses remain raw.
- Same pinned model as pilot: gpt-5.4-mini-2026-03-17, temperature 1, reasoning none, maximum 600 output
  tokens, default tier, explicit api.openai.com endpoint, per-slot seed. API seed is not a guarantee of
  deterministic provider outputs. SDK automatic retries disabled, six maximum concurrent calls.
- No optional stopping for effect sizes or significance. Full fixed allocation, unless budget,
  transport, integrity or external interruption prevents completion. Preserve every attempted request.

## Prospective group repairs informed by the pilot

1. A unique terminal canonical VOTE label may be inline. Duplicate/ambiguous labels, refusals and
   truncated responses remain invalid. No spelling or invisible-Unicode repairs; no inferred decisions.
2. Parse reasoning/share/action/adoption independently. A malformed vote cannot erase an otherwise
   valid disclosure. C3 authenticates only directly held or already public IDs and applies a round
   barrier. Unavailable citations remain flagged and never become authenticated facts automatically.
3. C2 repeats an authoritative adopted-amendment record after the output instructions. Discussion is
   explicitly distinguished from adoption. Only well-formed ADOPT IDs from the CEO in rounds 2-4,
   referring to earlier-round proposals, bind. Bare references in AMENDMENT are flagged, not new text.
   Valid actions may survive a malformed vote; refusal/truncation clears all fields.
4. Model claims about unadopted amendments remain verbatim. No automatic vote or reasoning correction.
   These clarifications change the group harness; pilot and confirmation trajectories are not pooled.
   Simple prompts are unchanged, permitting a cleaner independent replication of the six contrasts.

## Prespecified analysis

The first labels are S1 A, S2 FORMAL_REPORT, S3 ADOPT; code reads exact labels from the locked
engine definitions (the label names, not this prose, are authoritative). No first label is coded good.
Six primary individual contrasts are E minus U first-label probability, one for each task and anchor.
Use paired agent IDs, two-sided exact conditional McNemar/binomial tests, Holm adjustment across six
at family alpha .05. No per-parameter hypothesis tests are primary.

Report counts, complete pairs, discordance counts n10/n01 and paired risk differences. Confidence
intervals use two Clopper-Pearson marginal intervals for discordance probabilities with Bonferroni
coverage, subtracting [L10-U01, U10-L01]. Pointwise 95% divides alpha over two marginals; family 95%
divides over twelve marginals. These conservative intervals remain nondegenerate at ceilings.
Validate with outcome-free enumeration before collection. Family intervals and Holm decisions need
not agree because the former are more conservative. Cell intervals use exact binomial limits.

If either outcome of a pair is invalid, retain the pair as missing. Report complete-pair estimates
and worst-case full-sample bounds assigning each missing difference anywhere in [-1,1]. A contrast
with any missing pairs receives primary p=1 and cannot support its confirmatory claim; complete-pair
p is separately descriptive. Do not shrink the six-test family or replace invalid answers.

Secondary group family: six paired E-U contrasts in final first-label outcomes (three tasks x two
anchors), plus C1 consensus-by-round-five E-U in 00100. Apply the same exact methods with N=20 and
Holm across these seven secondary tests. This pilot-informed consensus endpoint is fixed before the
fresh sample. Separate individual and group families do not imply one global .05 error guarantee.
Group-level clustering is respected: votes/rounds are not independent sample units. Missing policy
and conservative family intervals follow the individual method with family size seven.

Other summaries are descriptive: neutral group bridges, rounds, proposals/adoptions, authenticated
evidence count /24, invalid fields, and six individual context contrasts (11011 minus 00100 within
each task/arm). No new discovery claim from unadjusted secondary inspection. No pooling with pilot.
A fixed qualitative review takes simple IDs 1,41,...361 in all cells and group 1 in all conditions,
plus every parser failure. This assistant review is unblinded and not a human gold set or moral score.

## Size justification and budget

Exact design power from code/phase2_confirmation_power.py: N=400 has about .834 power for a ten-point
paired shift with discordance .30 at conservative alpha .05/6. This is a planning assumption, not a
guarantee or a fitted pilot effect. Ceiling tasks cannot be rescued by larger N alone. N=20 groups
is a constrained secondary replication and is not advertised as powered for modest differences.
Preflight records exact group power scenarios at alpha .05/7 to make that limitation concrete.

Projected additional accounting is approximately $19, based on the completed pilot's token usage
scaled by allocation; group prompt clarification adds some input cost. Enforce a $30 new-run ceiling.
The previous pilot conservatively accounts for $4.15084065, so the planned maximum combined charge
is $34.15084065, below the absolute $100 new-package cap. The historical Phase 1.5 budget is separate.
Costing reserves before dispatch using UTF-8 byte bounds plus framing and max output; unknown charges
retain the full reservation and halt. Rates use full uncached input $.75/M and output $4.50/M plus 10%
allowance, ignoring caching discounts. Pricing checked 2026-09-13 against
https://developers.openai.com/api/docs/models/gpt-5.4-mini . Account invoices are not automatically verified.

## Structured synthetic review and resolution

Decision: execute a fresh two-anchor behavioural follow-up with independent field validation and
explicit C2 state, preserving the pilot and deferring human/moral validity to their later phases.

- Vera Linden: supports a whole-profile functional question, rejects equating profile influence with
  understanding or labelling dissent bad. Normative interpretation awaits the dual coding protocol.
- Marcus Osei: fresh agents and unchanged simple prompts permit replication; repaired group prompts
  change the intervention. Human resemblance needs independent benchmarks and contamination controls.
- Yuki Tanaka: supports fixed paired units, exact tests, multiplicity control and nondegenerate bounds;
  N=20 groups is weak for moderate effects and overlapping tasks cannot inflate effective N.
- Sofia Renna: preserving field provenance matters downstream; neither evidence IDs nor coherent prose
  establishes truthfulness. Keep model hallucinations visible for later validated coding.
- James Okafor: supports smallest prospective fixes for demonstrated parser/state defects, strict
  write-once transport and a full no-network replay before interpreting outcomes.

Disagreement: whether a small group replication deserves the word conclusive. Resolution: individual
contrasts are primary confirmation; group tests are bounded secondary evidence. Close only the
amended behavioural collection/analysis task, with broader architecture, human and moral claims open.
These are synthetic review perspectives, not external experts or human approval. No parameter mapping,
distribution, theory meaning, locked dilemma or historical outcome is changed.
