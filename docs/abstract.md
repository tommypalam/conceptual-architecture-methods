# Concepts as Architecture

## A Probabilistic Framework for Encoding Political-Ethical Concepts in LLM-Based Agents

**Tommaso Piero Palamenga — Bocconi University**

### Abstract

Can explicit representations of ethical dispositions systematically shape an
artificial agent's decisions during generation, and where does that shaping stop?
This paper introduces PARIA, a framework for investigating how political-ethical
concepts influence individual and collective behaviour in large-language-model
agents. Drawing on psychological accounts of freedom, justice, authority, care and
loyalty, PARIA represents individual dispositions through ten bounded parameters
with Beta distributions coupled by a Gaussian copula. Profiles condition decision
generation, and the application preserves the resulting choices without subsequent
ethical answer substitution.

An independent confirmation with 400 hash-locked profiles produced 4,800
individual decisions and 300 group simulations. All six prespecified individual
contrasts between profile-conditioned and context-only agents survived correction
for multiple comparisons; group evidence was more limited, with one of seven
secondary contrasts surviving. Within-arm analysis locates the effect more
precisely than the arm-level comparison does. In four of six cells the unprofiled
model was perfectly deterministic across 400 calls, so profiles did not shift an
existing distribution but introduced behavioural variance where none existed.
Which agents departed from that baseline was predicted by a single theoretically
identified coordinate: Procedural Dependence showed a monotone dose-response
across its quintiles, spanning 35 to 62 percentage points from lowest to highest,
and ranked first of ten parameters under multivariate control in every
non-degenerate cell. Nine of the ten coordinates showed no systematic effect. Of
nine directional hypotheses locked before collection, five were supported and none
pointed the wrong way, though that evaluation is retrospective and uncorrected,
and the dominant coordinate was not among the predictions.

Two further results bound the framework's scope. A 500-probe recognition screen,
dual-coded by raters from different providers with complete agreement, identified
all five decanonised benchmark variants at the same rate as their canonical
originals: structure-preserving domain substitution does not conceal a classic
paradigm from a frontier model, closing a contamination control that is commonly
assumed rather than tested. And four studies across three phases returned nulls
traceable to one cause, namely that tasks whose unprofiled answer is deterministic
cannot discriminate any arm contrast, motivating a baseline-dispersion pre-screen
as a design requirement.

These findings support a conditional demonstration of functional normative
parameterization, with its boundaries measured rather than assumed: explicit
profiles can systematically influence generated decisions, the influence
concentrates on one theoretically appropriate axis, and it disappears on tasks
whose answer is already determined. They do not establish intrinsic ethical
understanding, human behavioural equivalence, improved moral outcomes, or validity
for the remaining nine coordinates. PARIA provides a reproducible experimental
framework for separating behavioural influence from stronger claims about ethical
competence, and for locating the conditions under which normative representation
in artificial agents does and does not operate.

**Keywords:** normative AI; ethical parameterization; large language models;
agent-based simulation; political psychology; behavioural validation.
