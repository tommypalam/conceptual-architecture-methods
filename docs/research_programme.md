# The Cognitive Hexagon — Research Programme

> Wider-programme context supplied by the researcher. Maturity claims about
> other modules have not been independently verified in this repository.
> This project's authoritative current status is [NEXT_STEPS.md](../NEXT_STEPS.md).
> This document does not serve as the abstract of the Concepts as Architecture paper.

**Tommaso Piero Palamenga** · Bocconi University
*A research programme on synthetic minds, and the one vertex of it currently under empirical execution.*

> **What this document is.** A single readable map of a larger research programme (the Cognitive Hexagon) and a detailed status of its most-developed component, *Concepts as Architecture*, which is currently being executed and validated in code. It is written to be read in one sitting instead of opening a heavy repository. Nothing here is offered as a finished result; each part is labelled with its real maturity.

---

## 1. The one-paragraph version

The **Cognitive Hexagon** is an architecture for synthetic minds: six functional modules coupled in a closed loop (a *plane*), lifted by an axis of *interiority* (depth) and swept by an axis of *development* (time). Each module prices its operations in a single shared currency — **nats** (units of information) — so the modules are not a loose collection but an economy: what one spends, another must supply. Of the six modules, three are formally drafted and have "survived an adversary" (been stress-tested), two are early embryos, and one is proposed. **Concepts as Architecture** is the execution of one of the mature modules and is the only part of the programme with running code, real API experiments, and a locked empirical record. This document explains the whole shape, then reports exactly where that module stands.

---

## 2. The Hexagon at a glance

A mind is modelled as a **plane of six competences**, in two triads, wired so the output of one triad parameterises the input of the other:

| # | Module | Role | Status |
|---|--------|------|--------|
| 1 | **Cognitive Framework Index (CFI)** | *The engine* — relational, task-relative model of whole-agent intelligence (6 macros → 36 subdomains → facets; abilities as a coupling graph; capacity as a dynamical fixed point) | **BUILT** |
| 2 | **Concepts as Architecture** | *The behavioural governor* — 10-parameter probabilistic encoding of five political-ethical concepts (freedom, justice, authority, care, loyalty) that dictates how an agent reads the normative structure of its world | **Implemented; limited empirical support** |
| 3 | **Abductive Magnitude** | *The generative accelerator* — scores an abductive leap by the structural magnitude of the generative path (not by whether it turned out correct) | **BUILT** |
| 4 | **Reactive Grounding** | *The boundary organ* — concepts as decaying regions in feature space; learning as collision; revision only when the world pushes back | **EMBRYO** |
| 5 | **Cultural Evolution** | *The social field* — culture as the composition of minds; objectivity as intersubjective incompressibility | **EMBRYO** |
| 6 | **Cognitive Economics** | *The accountant* — prices the metabolic/computational cost of thought; abduction is the singularity of this cost law | **PROPOSED** |

Two further **axes** (not modules): **Depth** (interiority — is there something it is like to run the architecture?) and **Time** (development — the whole structure reorganising through experience).

**The closed loop.** CFI sets state-dependent constraints → shaping how Concepts reads the world → structural friction triggers an Abductive leap → the new language alters Grounding → acting on it drives Cultural Evolution → the shifted world changes the Economics of cognition → forcing CFI to self-correct, one tier up.

**The unifying bet.** Everything is priced in one currency (nats). Abduction *grows* the conceptual space; Grounding *carves within* it; Culture finds the *shared incompressible floor*; Economics prices the whole transaction. The couplings are not asserted — they are "paid for" in a shared unit. (Notably, the Grounding↔Economics coupling surfaced three separate times unprompted across drafts — treated as weak evidence it is real rather than imposed.)

---

## 3. The method (the part that travels)

Every module is written under one discipline, applied identically:

1. **State a formal object** — the precise mathematical thing being claimed.
2. **Make a falsifiable commitment** — name the single observation that would kill it.
3. **Flag the most elegant move as the most suspect** — clean settlements of hard problems are exactly what adversaries break; beauty is not evidence.
4. **Freeze the test cases before running** — so results cannot be rationalised after the fact.
5. **List forbidden shortcuts** — pre-commit to *not* rescuing a theory by tuning parameters after a disappointing run.

This is why each draft calls itself a "fetus," "embryo," or "survived its adversary": the maturity label is earned by how much adversarial pressure the module has withstood, not by how finished it looks.

---

## 4. Concepts as Architecture — the vertex under execution (detailed status)

**Concepts as Architecture** is Hexagon Vertex 2. It is the behavioural governor and the only module with running code and a locked empirical record. It is a Bocconi thesis in its own right.

### 4.1 The research question
> Can canonical psychological definitions of five political-ethical concepts — **freedom, justice, authority, care, loyalty** — be encoded as uncertainty-aware parameter profiles that generate *distinguishable and interpretable* social dynamics in an LLM-agent simulation?

The longer-term question is whether an agent understands an ethical concept. The present experiments test behavioural consequences and sensitivity to expression; they do not uniquely distinguish internal understanding from learned instruction-following.

### 4.2 The encoding
Each concept is represented through a canonical definition and mapped across **ten parameters** (e.g. Legitimacy Locus, Response Threshold, Relational Embedding, Moral Scope…) as **Beta distributions**, combined into a **10-dimensional joint distribution** via a **Gaussian copula** with a verified positive-semi-definite correlation matrix. Agents are sampled from this joint and placed in societal **configurations** (binary high/low on each of the five concepts). Six experimental dilemmas (three simple, three complex) exercise the framework, with locked, measured baselines. The tested full harness was non-neutral; deviation from 50/50 alone cannot be attributed to encoded parameters.

### 4.3 Evidence and current work

Phase 0 calibration, harness diagnostics, and the locked holdout are closed.
The tested full harness materially altered several dilemma baselines. The
Phase 1 operational pilot passed, establishing pipeline functionality rather
than formal encoding validity. The July sweep pilot supplied preliminary
parameter-response evidence, including a direction reversal requiring review.

Phase 1.5 is closed for the researcher-accepted limited objective. Independent
PD confirmation and later canonical/verbal effects support initial functional
normative parameterization under specified conditions. The original full battery
remains unmet; all ten outcomes and robustness limitations remain reported.
The accepted conclusion does not establish ethical understanding or validate
the full architecture. No new paid run is queued. See the
[accepted closure](../experiments/phase1_5_encoding_validity/ACCEPTED_CLOSURE_2026-09-12.md)
and [results](phase1_5_results.md). The original Phase 2 design is not released.

### 4.4 Interpretation limits

Parameter-referential reasoning is not by itself evidence of recovered latent
traits or conceptual understanding. Numeric-only success or failure does not
uniquely distinguish understanding from label association. The battery combines
behavioural gradients, blinding, robustness, and baseline-aware interpretation;
its conclusions remain contingent on completed experiments and review.

---

## 5. How the pieces fit

This project is not a standalone demo — it is **Vertex 2 supplying a dependency the rest of the Hexagon waits on.** Cultural Evolution (Vertex 5) explicitly lists "Concepts as Architecture" as a *built input channel* it composes over. So the rigour this project is being held to — frozen prompts, honest baselines, refusing to fake a pass — is not thesis bureaucracy; it is laying one verified girder in a larger structure, so that what leans on it later leans on something real.

---

## 6. Maturity ledger (so nothing is oversold)

| Component | Maturity | One-line honest status |
|-----------|----------|------------------------|
| CFI (1) | Built (drafted, adversary-tested) | Formal spec exists; not yet instantiated as a running graph |
| Concepts as Architecture (2) | **Implemented; limited empirical support** | Locked Phase 0, operational pilot, accepted scoped Phase 1.5 closure; broad validity unmet |
| Abductive Magnitude (3) | Built (drafted, adversary-tested) | Executable metric on code traces; lateral term partly placeholder |
| Reactive Grounding (4) | Embryo | Formal object + falsifier stated; toy world specified, not yet run |
| Cultural Evolution (5) | Embryo | Composition operator specified; inputs not yet real |
| Cognitive Economics (6) | Proposed | Cost law stated with one asserted pole of unknown location |
| Depth axis | Open | Needs a measurable proxy or it stays decoration (acknowledged) |
| Time axis | Partially mechanised | Generalising "reactive recompilation" from one module to the plane |

---

## 7. In one line

> **Six competences in a plane, lifted by depth, swept by time — priced in one currency, each part labelled with exactly how far it has earned its place. One vertex is running in code and returning real results; the rest are honest bets with their own kill-conditions named.**

*Author: Tommaso Piero Palamenga, Bocconi University. Status: research in progress — not for citation. Every framework here names the observation that would refute it; that is the point.*
