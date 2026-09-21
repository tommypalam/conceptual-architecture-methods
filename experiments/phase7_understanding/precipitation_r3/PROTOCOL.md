# precipitation_r3 — protocol

**Status: prepared offline.** Follows
[precipitation_r2](../precipitation_r2/ASSESSMENT.md), whose three primary
contrasts were significant and order-robust but whose **discriminating secondary
was void**: the dose-response slope appeared in the RULE arm, whose text is
identical for every agent and cannot respond to exemplar keep-count. Keep-count
was confounded with agent parity, parity set presentation order, and order moves
the bare item from 0.179 to 0.436 — so the slope read order, not exemplars.

**This designation crosses order with the covariate.** Every agent-item is shown
**both ways**, so order is balanced within every agent, arm and keep-count by
construction (verified before release: 63/63, 84/84, 357/357, 336/336 by
keep-count; 21/21 per agent). A covariate cannot proxy order when order does not
vary between agents. 1,680 calls.

r2 is **not superseded** and its records are not reused; its primary contrasts
stand as measured. What this adds is a readable secondary. The experiment is
otherwise identical, at the same design hash.

## Question

Reactive Grounding (vertex 4) holds a concept in two registers — a cloud of
remembered instances and a boundary fitted to them — and its **Conjecture 1** is
that the boundary *stiffens* as the cloud evaporates. That is the claimed
difference between holding a concept and following a rule you are currently being
told.

Phase 7 so far measured lens-stacking inside a fixed dimensionality: supply a
gloss, behaviour narrows; reverse the gloss, it reverses
([semantics_r1](../semantics_r1/ASSESSMENT.md)). Real — and a supplied gloss is a
rule being read. **This asks whether a boundary forms from INSTANCES and
generalises to a dimension the instances are silent about.**

## Three circularity traps, and the control for each

| Trap | Control |
|---|---|
| **Instruction persistence** — "withdrawal" that leaves the text earlier in context is trivial | The harness sends one user turn and holds no state. Every cell is an independent call; withdrawn material is **absent**, not earlier |
| **Measuring the outcome that defines the treatment** — the triviality trap of Cognitive Economics Claim 1 | Read out on a dimension the exemplars are **silent on**: exemplars are base-item decisions where keep and procedure coincide; the test items are the **twins**, where they come apart |
| **Idealised exemplars** — constructing clean transcripts writes the rule being tested for | Exemplars are **actual frozen decisions**, noise included. No agent chose keep on all seven; the max is six |

A fourth was considered and rejected: holding out *items* is impossible, because
four of the five unused pool items saturated on gpt and one was excluded on
review. Generalisation is therefore tested across the **keep/procedure direction**.

## Run statement (rule 4)

| | |
|---|---|
| Model | `gpt-5.4-mini-2026-03-17`, temperature 1, reasoning disabled |
| Materials | frozen `pd_prospective_r1` exemplars; `defeasibility_screen_r1` twins. **No new participant data, no new items** |
| Arms | INSTANCES / RULE / NEITHER x 40 agents x 7 twins x 2 orders = **1,680 calls** |
| Seeds | analysis 2026092221 |
| Cost | $6.325 reserved worst case; about $1.25 expected |

Design content hash `b75a407e4c0aa0575fe30aa00a158eee55c85a8921cdad8aa76bbacbf6146e11`.

| Arm | The user turn carries |
|---|---|
| **INSTANCES** | five of the agent's own prior decisions, as a transcript. No rule, no field, no gloss |
| **RULE** | the procedural principle stated as an instruction. No exemplars |
| **NEITHER** | the bare item |

The item body is byte-identical across arms; only the prefix differs. **No profile
block is rendered in any arm** — the model acts as an agent, and the manipulation
is entirely the prefix. Verified before release: no arm leaks a pinned value, only
RULE mentions procedure, and NEITHER is the bare item.

## Analysis, fixed before collection

1. **Primary: INSTANCES − NEITHER**, a within-item contrast with a 95% bootstrap
   interval, with RULE − NEITHER and INSTANCES − RULE alongside. Never one arm
   clearing a threshold while another does not.
2. **Secondary, dose-response.** The five shown exemplars vary in how many are
   keeps (**1 to 4 of 5**, verified). If a boundary is *fitted* to instances, the
   shift should track that count. **The RULE arm cannot produce this** — its text
   is identical for every agent — so a slope there would void the secondary.
3. Decision rule exercised offline on planted data for all four readings; the
   dose slope was flat in the three nulls and +0.158 with the interval excluding
   zero only under a planted exemplar-fitted boundary.

## What no outcome establishes

Understanding, or that the model holds a concept. **Survival under decay**: there
is no γ across independent calls, so this addresses only the *first half* of
Conjecture 1 — whether a boundary forms and generalises, not whether it survives
the loss of the instances over time. And a null is **not a verdict on the model
alone**: Reactive Grounding's own honest flag concedes the max-entropy
identification is its most suspect move, and this harness cannot separate "no
boundary in the model" from "the vertex-4 bet is wrong here".
