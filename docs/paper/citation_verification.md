# Citation verification record

**Current paper, 23 September 2026:** Related Work is section 2. The original
unchecked checklist below is historical; later entries record completed checks.
The publication revision rechecked the sources used in the current paper, with
the following primary-source record. This checks the narrow claims actually
cited, not an exhaustive novelty search.

| Current citation | Primary source | Check or correction |
|---|---|---|
| Lu et al. 2022 | [Author paper](https://arxiv.org/abs/2104.08786) | Example-order sensitivity; ACL year 2022 |
| Sclar et al. 2024 | [Author paper](https://arxiv.org/abs/2310.11324) | Meaning-preserving formatting sensitivity; ICLR 2024 |
| Razavi et al. 2025 | [Author paper](https://arxiv.org/abs/2502.06065) | Narrowed claim to reformulation and sensitivity prediction |
| Chatterjee et al. 2024 | [ACL](https://aclanthology.org/2024.findings-emnlp.852/) | Scale/instruction tuning do not necessarily reduce sensitivity |
| Webson and Pavlick 2022 | [ACL](https://aclanthology.org/2022.naacl-main.167/) | Irrelevant/misleading templates; authors and pages |
| Min et al. 2022 | [ACL](https://aclanthology.org/2022.emnlp-main.759/) | Random demonstration labels in the studied classification settings |
| Wei et al. 2023 | [Author paper](https://arxiv.org/abs/2303.03846) | Flipped and semantically unrelated labels |
| Liu 2026 | [Author paper](https://arxiv.org/abs/2605.08295) | Demonstrated label inventory; restored full title |
| Luz de Araujo and Roth 2025 | [Author paper](https://arxiv.org/abs/2407.02099) | 162 personas, seven models, empty and paraphrase controls |
| Zheng et al. 2024 | [ACL](https://aclanthology.org/2024.findings-emnlp.888/) | Objective-task persona effects and predictability |
| Geiger et al. 2025 | [JMLR](https://www.jmlr.org/papers/v26/23-0058.html) | Causal abstraction; added 26(83):1-64 |
| Zhang and Nanda 2024 | [Author paper](https://arxiv.org/abs/2309.16042) | Activation-patching methodological sensitivity |
| Vaidyanathan et al. 2026 | [Author paper](https://arxiv.org/abs/2606.27510) | Corrected first name to Sankaran, all authors and full title |
| Wang et al. 2023 | [Author paper](https://arxiv.org/abs/2305.14160) | Label-word information aggregation |
| Rao et al. 2023 | [Author paper](https://arxiv.org/abs/2310.07251) | In-context ethical-policy framing |
| Sachdeva and van Nuenen 2025 | [Author paper](https://arxiv.org/abs/2501.18081) | Self-consistency and inter-model disagreement |
| Barr et al. 2013 | [Author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/3881361/) | Random-effects structure and journal metadata |
| Gelman and Stern 2006 | [Author-hosted article](https://sites.stat.columbia.edu/gelman/surveys.course/GelmanStern2006.pdf) | Direct differences versus significance comparisons |
| Holm 1979 | [Original article scan](https://www.ime.usp.br/~abe/lista/pdf4R8xPVzCnX.pdf) | Sequential family-wise correction, volume and pages |

No new references were introduced in this publication revision. The current
paper makes no claim that field-level controls are absent from all prior work.

## Historical checklist and earlier verification passes

**Why this file exists.** The references in §9 were supplied by a literature
search run outside the drafting session. They were cited normally in the draft,
but **none has been checked against a database**, and several postdate the
drafting tools' knowledge entirely. This file is the checklist for the session
that does have database access.

**What to verify for each entry**, in order of how badly a mistake would hurt:

1. **Does the paper exist**, with these authors and this year?
2. **Does it make the claim attributed to it?** A real paper cited for the wrong
   finding is worse than a missing citation — it is the error a reviewer will
   catch and the one that damages the rest of the paper.
3. Venue and full reference details for the bibliography.

Mark each row. Anything that fails (1) or (2) must be removed or replaced, not
softened.

---

## Known issues to fix first

| Item | Issue |
|---|---|
| **von Oswald et al. 2022** | Supplied as "Oswald et al."; the usual citation is **von Oswald**. Flagged inline in §9.3. Correct the name, then verify. |
| **Liu (2026)** — label-slot / fixation | Cited as a single author in §9.2 while **Liu et al. (2021)** in §9.1 is a different work. Confirm these are distinct and that the 2026 one is single-author. |
| **Wei et al. 2021** and **Wei et al. 2023** | Two different Wei papers (instruction tuning; semantically unrelated labels). Confirm both, and disambiguate in the bibliography. |
| **Wang et al. 2023** and **Wang et al. 2026** | Same surname, different works (label-word anchoring; function-vector decomposition). Confirm and disambiguate. |
| **Holm (1979)** | Not in §9 but cited in `thesis.md` for the multiple-comparison correction, and **absent from the framework bibliography**. Volume and pages were written from memory. Verify or replace. |
| **Le Texier** | Already corrected from 2019 to **2018** to match the framework bibliography. Confirm 2018 is right. |

---

## §9.1 Prompt conditioning and sensitivity

| Citation | Claim attributed | Verified? |
|---|---|---|
| Radford et al. 2019 | zero-shot transfer via language-model conditioning | ☐ |
| Brown et al. 2020 | few-shot prompting as core capability | ☐ |
| Liu et al. 2021 | survey organising prompt-based learning | ☐ |
| Gao et al. 2021 | template and label-word choice made explicit | ☐ |
| Wei et al. 2021 | instruction tuning changes zero-shot prompt following | ☐ |
| Kojima et al. 2022 | large effect from minimal zero-shot prompt change | ☐ |
| **Lu et al. 2021** | example order moves performance near-random ↔ near-SOTA | ☐ |
| **Sclar et al. 2023** | formatting alone spans large accuracy ranges, meaning held | ☐ |
| **Razavi et al. 2025** | same for wording, structure, punctuation | ☐ |
| **Chatterjee et al. 2024** | scale/instruction tuning do not remove brittleness | ☐ |
| Yang et al. 2026 | shared lexical task heads explain prompt variance | ☐ |

The four in bold are load-bearing: they justify holding surface form constant to
the byte. If any fails, §9.1's motivating argument needs another source.

## §9.2 Label binding

| Citation | Claim attributed | Verified? |
|---|---|---|
| **Min et al. 2022** | randomising demonstration labels barely degrades performance | ☐ |
| Kim et al. 2022 | effect of correct mappings varies by configuration | ☐ |
| Fei et al. 2023 | domain-label bias as systematic failure mode | ☐ |
| Zhao et al. 2021 | contextual calibration reduces prompt-induced bias | ☐ |
| Jiang et al. 2023 | label shift explains instability under prompt variation | ☐ |
| Zhou et al. 2023 | calibration | ☐ |
| **Wei et al. 2023** | large models override semantic priors on unrelated labels | ☐ |
| **Liu 2026** | output bound to demonstrated token inventory; label-slot effect | ☐ |

The three in bold are the ones the draft uses *against itself* — they support the
disclaimer of semantic understanding. Verify these especially carefully, because
the draft now leans on them for its most important act of restraint.

## §9.3 Causal localisation

| Citation | Claim attributed | Verified? |
|---|---|---|
| Geiger et al. 2023 | causal abstraction unifies patching, mediation, tracing | ☐ |
| Zhang & Nanda 2023 | patching has many variants, disparate results | ☐ |
| Vaidyanathan et al. 2026 | patching can absorb hidden interaction effects | ☐ |
| Olsson et al. 2022 | induction heads account of ICL | ☐ |
| **von Oswald** et al. 2022 | gradient-descent interpretation of ICL | ☐ name! |
| Xie et al. 2021 | implicit Bayesian inference; distribution mismatch | ☐ |
| Todd et al. 2023 | function vectors | ☐ |
| Yin & Steinhardt 2025 | few-shot ICL depends on FV heads in larger models | ☐ |
| **Wang et al. 2023** | label words anchor: shallow gather, deep predict | ☐ |
| Nam et al. 2025 | causal head gating: facilitating/interfering/irrelevant | ☐ |
| Wang et al. 2026 | function vectors decompose additively by example | ☐ |

## §9.4 Persona conditioning

| Citation | Claim attributed | Verified? |
|---|---|---|
| **De Araujo & Roth 2024** | 162 personas, 7 models, empty- and control-persona baselines | ☐ |
| Han et al. 2025 | trait prompting yields recognisable personality-aligned behaviour | ☐ |
| Tang et al. 2026 | facet-level steering; persona signal dilutes under long context | ☐ |
| Du et al. 2025 | agent survey: prompt engineering as parameter-free optimisation | ☐ |
| Chowa et al. 2025 | agent survey | ☐ |

De Araujo & Roth carries the gap claim in §9.4 — that this literature compares
conditioned against unconditioned arms rather than isolating fields. Check that
the paper does what is attributed, including the control-persona baseline.

## §9.5 Moral evaluation

| Citation | Claim attributed | Verified? |
|---|---|---|
| Rao et al. 2023 | prompts as task + ethical policy + user input | ☐ |
| Benkler et al. 2023 | 1,128 prompts, 56,400 responses, demographic value patterns | ☐ |
| **Sachdeva 2025** | low inter-model agreement, moderate self-consistency | ☐ |

Sachdeva is used in §9.5 to reinterpret our cross-model shrinkage. If it does not
support that reading, delete the inference rather than keeping the citation.

---

## Two claims that are ours, not the literature's

These are marked in the draft and are **not** citation problems — they are claims
the search could not settle and that must stay hedged:

1. **That field-level identification under byte-held surface form is scarce for
   closed models** (§9.4). Stated as a gap the search indicated; not proven.
2. **That the replication gate is not represented elsewhere** (§9.6). The
   paper's strongest novelty claim. The search surfaced no counterexample, and the
   draft says explicitly that absence of evidence in a search is not evidence of
   absence. Keep that hedge unless a systematic check supports dropping it.

---

## After verification

Remove the citation-status banner at the top of §9 once every row is checked.
**Do not remove it while any row is unchecked** — it is the honest signal that the
section has not been confirmed, and it is what distinguishes cited-but-unverified
from verified.

---

# Verification results — 2026-09-16

Worked through with database access, in the order the checklist specifies.
**37 of 39 rows verified. Two citations do not exist and must be removed.**
Every row below was checked for existence, authorship, year, and that the paper
makes the claim attributed to it.

## FAILURES — remove, do not soften

| Citation | Where | Finding |
|---|---|---|
| **Han et al. 2025** | §9.4 | **No such paper found.** Four targeted searches returned only PersonaLLM (Jiang et al. 2024, Findings NAACL), TRAIT (Findings NAACL 2025), Serapio-García et al. (Nature Machine Intelligence 2025), and "Assessing Social Alignment" (arXiv 2412.16772). None is Han et al. 2025 and none carries the attributed claim as stated. The sentence it supports must be deleted. |
| **Chowa et al. 2025** | §9.4 | **No such paper found.** Agent-survey searches return Du et al. 2025, Luo et al. 2025, Guo et al. 2024, Wang et al. 2023 — no Chowa. Delete from the parenthetical; Du et al. 2025 stands alone and carries the claim. |

Per the rule at the top of this file, neither is replaced with a substitute:
CLAUDE.md prohibits adding citations the literature search did not supply.

## CORRECTIONS to verified entries

| Citation | Correction |
|---|---|
| **Sachdeva 2025** | Is **Sachdeva, P.S. and van Nuenen, T. (2025)** — TWO authors, cited as one. Also the paper reports "moderate **to high** self-consistency"; the draft says "moderate". Venue: ACM FAccT 2025, doi 10.1145/3715275.3732044 (arXiv 2501.18081). Claim otherwise verified: low inter-model agreement, and judgements diverge substantially from human AITA evaluations. |
| **Le Texier** | **2019 is correct; the "correction" to 2018 recorded above is wrong** and would have introduced an error. American Psychologist, 74(7), 823–839. `thesis.md` already has 2019 and should NOT be changed. It is the framework bibliography that needs fixing. |
| **von Oswald et al.** | Name fix confirmed correct — it is **von Oswald**. arXiv 2212.07677 (2022); published version is ICML 2023, PMLR 202. Pick one year convention and apply it. |
| **Benkler et al. 2023** | Paper verified (Benkler, N., Mosaphir, D., Friedman, S., Smart, A. and Schmer-Galunder, S., "Assessing LLMs for Moral Value Pluralism", arXiv 2312.10075). **The figures "1,128 prompts, 56,400 responses" could not be confirmed from the abstract** — check them against the full text or drop the numbers and keep the qualitative claim. |

## Disambiguations resolved

- **Liu et al. 2021** (Pengfei Liu, prompting survey, ACM CSUR) and **Liu 2026** (Ming Liu, sole author, Amazon, "In-Context Fixation", arXiv 2605.08295) are different works and different people. Confirmed distinct; the 2026 one is single-author as cited.
- **Wei et al. 2021** (FLAN, arXiv 2109.01652) and **Wei et al. 2023** (arXiv 2303.03846) confirmed distinct.
- **Wang et al. 2023** ("Label Words are Anchors", EMNLP 2023, arXiv 2305.14160) and **Wang et al. 2026** ("How Few-Shot Examples Add Up", arXiv 2605.16591, ICML 2026) confirmed distinct.
- **Holm (1979)** verified: Scandinavian Journal of Statistics, **6, 65–70**. Matches what `thesis.md` cites from memory. Add to the framework bibliography.

## Verified rows, with venue for the bibliography

§9.1 — Radford et al. 2019 ☑ · Brown et al. 2020 ☑ · Liu et al. 2021 ☑ (ACM
Computing Surveys, arXiv 2107.13586) · Gao et al. 2021 ☑ (ACL 2021) · Wei et al.
2021 ☑ · Kojima et al. 2022 ☑ (NeurIPS 2022) · **Lu et al. 2021** ☑ (arXiv
2104.08786; published ACL 2022) · **Sclar et al. 2023** ☑ (arXiv 2310.11324;
ICLR 2024) · **Razavi et al. 2025** ☑ (arXiv 2502.06065; Razavi, Soltangheis,
Arabzadeh, Salamat, Zihayat, Bagheri) · **Chatterjee et al. 2024** ☑ (POSIX,
Findings EMNLP 2024, 14550–14565; claim confirmed verbatim: "merely increasing
the parameter count or instruction tuning does not necessarily reduce prompt
sensitivity") · Yang et al. 2026 ☑ (arXiv 2604.22027)

§9.2 — **Min et al. 2022** ☑ (EMNLP 2022, arXiv 2202.12837) · Kim et al. 2022 ☑
(EMNLP 2022, arXiv 2205.12685) · Fei et al. 2023 ☑ (ACL 2023, arXiv 2305.19148;
domain-label bias confirmed) · Zhao et al. 2021 ☑ (ICML 2021, PMLR 139) · Jiang
et al. 2023 ☑ (Findings EMNLP 2023, arXiv 2310.10266) · Zhou et al. 2023 ☑
(Batch Calibration, arXiv 2309.17249) · **Wei et al. 2023** ☑ · **Liu 2026** ☑
(claim confirmed in detail: label-slot binding, set-level fixation, activation
patching recovering 98.4% of the accuracy gap)

§9.3 — Geiger et al. 2023 ☑ (arXiv 2301.04709; JMLR 26, 2025) · Zhang & Nanda
2023 ☑ (arXiv 2309.16042; ICLR 2024) · Vaidyanathan et al. 2026 ☑ ("The Curse of
Multiple Mediators", arXiv 2606.27510 — claim confirmed exactly) · Olsson et al.
2022 ☑ · von Oswald et al. 2022 ☑ · Xie et al. 2021 ☑ (arXiv 2111.02080) · Todd
et al. 2023 ☑ (arXiv 2310.15213; ICLR 2024) · Yin & Steinhardt 2025 ☑ (ICML
2025, arXiv 2502.14010) · **Wang et al. 2023** ☑ · Nam et al. 2025 ☑ (NeurIPS
2025, arXiv 2505.13737) · Wang et al. 2026 ☑

§9.4 — **De Araujo & Roth 2024** ☑ — claim confirmed in full: 162 personas, 7
models, 12 categories, control setting of 30 paraphrases of "a helpful
assistant" AND an empty-persona condition, "for all models and datasets,
personas show greater variability than the control setting". Full reference:
Luz de Araujo, P.H. and Roth, B. (2025). PLOS ONE, 20, e0325664 (arXiv
2407.02099, 2024) — decide which year to cite. · Du et al. 2025 ☑ (Du, Zhao,
Shi, Xie, Jiang, Bai and He; ACM Computing Surveys; "parameter-free strategies
that optimize agent behavior through prompt engineering" confirmed) · Tang et
al. 2026 ☑ (arXiv 2602.19157; dilution claim confirmed: "prompt- and RAG-based
signals ... can be diluted in long dialogues, leading to drifting and sometimes
inconsistent persona behavior") · ~~Han et al. 2025~~ ✗ · ~~Chowa et al. 2025~~ ✗

§9.5 — Rao et al. 2023 ☑ (Findings EMNLP 2023, arXiv 2310.07251) · Benkler et
al. 2023 ☑ with the figure caveat above · **Sachdeva 2025** ☑ with the
two-author correction above

## Banner

The citation-status banner at the top of §9 **may be removed once the two failed
citations are deleted and the four corrections are applied** — every remaining
row is checked. The two hedged claims that are ours rather than the
literature's (field-level identification is scarce for closed models; the
replication gate is not represented elsewhere) are unaffected and keep their
hedges.


---

# Application of the verification — 2026-09-22

The 2026-09-16 findings above were only partly applied to the draft. All are now
applied, and three load-bearing rows were independently re-checked against source
with live access:

| Fix | Status |
|---|---|
| `Han et al. 2025` removed from §9.4 | was already applied |
| `Chowa et al. 2025` removed; Du et al. 2025 stands alone | **applied 22 Sept** |
| `Sachdeva (2025)` → `Sachdeva and van Nuenen (2025)`; "moderate" → "moderate-to-high" self-consistency, plus the divergence-from-human finding | **applied 22 Sept** |
| `von Oswald` inline pending-verification note removed | **applied 22 Sept** |
| Benkler figures | the draft already cites qualitatively without the unconfirmed "1,128 prompts / 56,400 responses"; re-checked at arXiv 2312.10075 — authors and title confirmed, abstract carries no such figures. No change needed. |

**Re-checked at source, 22 September:**

- **Min et al. 2022** ☑ — EMNLP 2022, arXiv 2202.12837, Min, Lyu, Holtzman,
  Artetxe, Lewis, Hajishirzi, Zettlemoyer. Claim confirmed verbatim: "randomly
  replacing labels in the demonstrations barely hurts performance," across 12
  models. One of the three citations the draft uses *against itself*.
- **De Araujo & Roth 2024** ☑ — arXiv 2407.02099. 162 personas, 12 categories,
  7 models; both the 30-paraphrase "a helpful assistant" control and an
  empty-persona condition; "personas show greater variability than the control
  setting" confirmed. Carries the gap claim of §9.4.
- **Benkler et al. 2023** ☑ — arXiv 2312.10075, authors and title confirmed.

**The banner is removed.** Section 10 now states verified status, records that
two citations were deleted rather than substituted, and keeps the hedges on the
two claims that are ours rather than the literature's.


---

# Additions — 2026-09-23

Four references added in the paper revision, each checked at source:

| Citation | Checked | Claim used |
|---|---|---|
| Webson & Pavlick 2022, NAACL 2022, 2300–2344 | ACL Anthology 2022.naacl-main.167 ☑ | models learn as fast from irrelevant or misleading prompt templates |
| Zheng, Pei, Logeswaran, Lee & Jurgens 2024, Findings EMNLP 2024 | ACL Anthology 2024.findings-emnlp.888; arXiv 2311.10054 ☑ | personas in system prompts do not reliably improve performance; effects hard to predict |
| Wang et al. 2023, EMNLP 2023 ("Label Words are Anchors") | already ☑ in the 16 Sept verification (§9.3) | label words gather information in shallow layers |
| Barr, Levy, Scheepers & Tily 2013, JML 68(3):255–278 | standard reference, as cited in the thesis ☑ | maximal random-effects structure |

These depart from the 18 Sept rule "do not add citations the search did not
supply"; they are added because a reviewer would expect Webson & Pavlick and
Zheng et al. in a paper on whether models use prompt meaning, and each was
verified before use.
