# precipitation_r2 — protocol

**Status: prepared offline. A RE-DESIGNATION of
[precipitation_r1](../precipitation_r1/ASSESSMENT.md)**, which halted on a
transport `TimeoutError` at call 294 of 840. That designation is closed: its
failed slot stays unresolved and is never touched, and its 293 settled records
are excluded from every analysis here. Nothing is retried; this is the
designation that would have been built had r1 failed at call 1.

The distinction the no-retry rule protects is between *repairing* a halted run —
forbidden, because it is indistinguishable after the fact from retrying until the
numbers look clean — and *starting a new one*, which is always permitted. The
experiment is byte-identical at design hash `b75a407e…`; only the designation,
the release and the analysis seed are new.

**Status: prepared offline.** Programme: [../PROGRAMME.md](../PROGRAMME.md).
Exploratory; not part of the submitted thesis.

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
| Arms | INSTANCES / RULE / NEITHER x 40 agents x 7 twins = **840 calls** |
| Seeds | analysis 2026092211 |
| Cost | $3.162 reserved worst case; about $0.63 expected |

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
