# Citation verification checklist — §9 of `paper_draft.md`

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
