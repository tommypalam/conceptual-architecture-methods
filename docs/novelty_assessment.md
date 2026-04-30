# L1 Diagnosis: Novelty Assessment — PARIA

> Per the Research OS Template, Section 2. Completed before any code is written.
> Rule: any component scoring "No" gets piecewise execution with manual verification at every step. No exceptions.

---

## Plain English Summary

PARIA is novel in its **combination**, not in its individual parts. The statistics (Beta distributions, Gaussian copulas) are textbook. The ABM framework (Mesa) is standard. Python is Python. What is genuinely new — and where AI assistance is least reliable — is the *conceptual encoding layer*: the specific decisions about how a philosophical/psychological definition of "freedom", "justice", "authority", "care", or "loyalty" maps onto numerical parameters that then drive agent behaviour. That translation layer has no prior art the AI can reliably pattern-match against. Everything else is scaffolding around that hard core.

**Draft 0.5 update:** Scope expanded from 3 to 5 concepts. This increases the novelty surface — the care and loyalty parameter-to-behaviour mappings are as original as the freedom/justice/authority ones.

---

## Component-by-Component Assessment

### 1. Data Formats

| Component | AI familiar? | Implication |
|-----------|-------------|-------------|
| CSV / tabular calibration data from psych surveys | **Yes** | Fully delegatable |
| `.parquet` for agent draws | **Yes** | Fully delegatable |
| PyMC model objects | **Yes** | Fully delegatable |

---

### 2. Cleaning and Data Preparation

| Component | AI familiar? | Implication |
|-----------|-------------|-------------|
| Rescaling psychometric scores to [0, 1] | **Yes** | Delegatable |
| Handling missing values in survey data | **Yes** | Delegatable |
| Verifying Beta distribution fits against empirical score histograms | **Partially** | Mechanics are delegatable; judgment about conceptual fit adequacy requires human sign-off |

---

### 3. Merge Logic

| Component | AI familiar? | Implication |
|-----------|-------------|-------------|
| Merging instrument datasets by respondent ID | **Yes** | Standard join — delegatable |
| Copula sampling procedure (3-line NumPy/SciPy) | **Yes** | Documented in modus operandi — delegatable |

---

### 4. Statistical Methods

| Component | AI familiar? | Implication |
|-----------|-------------|-------------|
| Beta distribution parameterisation | **Yes** | Delegatable |
| Gaussian copula via Sklar's theorem | **Yes** | Delegatable — verify output |
| PSD verification of R via eigendecomposition | **Yes** | Delegatable |
| Higham (2002) nearest PSD algorithm | **Partially** | Uncommon — verify output carefully |
| Bayesian encoding with PyMC | **Yes** | Delegatable |
| Mesa ABM boilerplate | **Yes** | Delegatable; specific interaction *rules* are novel |
| t-copula robustness check | **Partially** | Less common — verify degrees-of-freedom parameterisation |

**Key constraint:** The specific correlation values in R are **human-owned constants**. AI must never modify R entries without explicit instruction and panel review.

---

### 5. Variable Construction — THE HIGH-RISK ZONE

| Component | AI familiar? | Implication |
|-----------|-------------|-------------|
| The 10 PARIA parameter definitions | **No** | Original to this project. Piecewise only. |
| Mapping Beta α/β to psychological constructs | **No** | Conceptual grounding is domain-specific. Human sign-off required. |
| Parameter-to-behaviour rules inside Mesa | **No** | AI will invent plausible-sounding rules that may be conceptually incoherent. Panel review before any rule enters code. |
| Performance metric ("morally good decisions") | **No** | Hardest open problem. AI must not attempt a definition without explicit human-led deliberation. |
| Concept silo encoding (freedom / justice / authority priors) | **No** | PARIA-original. No template exists. |
| Societal configuration definitions (000–111) | **No** | PARIA-original. Human-owned. |

---

### 6. Output Formats

| Component | AI familiar? | Implication |
|-----------|-------------|-------------|
| Plotly figures and comparison dashboards | **Yes** | Delegatable |
| Summary tables (obedience rate by config) | **Yes** | Delegatable |
| Milgram retrodiction comparison | **Partially** | Format is standard; whether 63% ≈ 65% counts as passing is a human judgment call |

---

## Risk Map

```
LOW RISK                           MEDIUM RISK                            HIGH RISK
(delegate freely)                  (delegate + verify output)             (piecewise, human-led, panel review)
─────────────────                  ──────────────────────────             ───────────────────────────────────
Data loading & reshaping           Gaussian copula mechanics              10-parameter definitions
Standard cleaning                  Beta fit adequacy judgment             Parameter-to-behaviour mapping
PSD verification                   t-copula robustness check              Performance metric definition
PyMC model syntax                  Milgram retrodiction interpretation     Concept encoding priors
Mesa boilerplate                   Factor analysis of 10 parameters        Societal config definitions
Plot generation                    R matrix modification (any)             Any cross-concept interaction rule
```

---

## Verdict

PARIA's novelty is **concentrated and locatable**: it lives in the conceptual encoding layer — translating philosophical/psychological definitions into parameter distributions, and those distributions into agent behaviour rules. Everything outside that layer is standard scientific computing.

**The primary failure mode to guard against:** AI produces syntactically correct, statistically plausible, conceptually incoherent parameter-to-behaviour rules that pass all automated tests and break only under expert conceptual scrutiny. The five-agent panel protocol in CLAUDE.md exists to catch exactly this.

---

*Assessment date: April 2026. Revisit at the start of each new phase.*
