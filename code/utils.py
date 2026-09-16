"""
utils.py — Shared helpers for the Concepts-as-Architecture (PARIA) pipeline.

Contains:
  - Gaussian copula correlation matrix R (canonical, human-owned)
  - Beta marginal parameters for the ten agent parameters
  - Societal configuration space (2^5 grid) and anchor configurations
  - PSD verification
  - Copula sampling (thesis v0.6 §3.4.2)
  - Logging helpers

Source of truth: Theory/concepts_as_architecture_thesis_v0_6.md (Table 1,
Appendix D) and Theory/implementation_specification_v0_1.md (Part 1).

Do not modify R or BETA_PARAMS without panel review and PSD re-verification.
Parameter order: [LL, CS, RT, MoR, RE, PD, TfA, ID, MS, AW]

Endpoint conventions (thesis v0.6 §3.1 — note LL runs 0=external, 1=internal):
  LL  Legitimacy Locus            0=external warrant      1=internal endorsement
  CS  Constraint Sensitivity      0=low                   1=high
  RT  Response Threshold          0=tolerant              1=hair-trigger
  MoR Mode of Response            0=internal/reflective   1=external/behavioural
  RE  Relational Embedding        0=atomised              1=relational
  PD  Procedural Dependence       0=outcome-dominant      1=process-dominant
  TfA Tolerance for Asymmetry     0=egalitarian           1=hierarchical
  ID  Internalisation Dependence  0=surface compliance    1=genuine endorsement
  MS  Moral Scope                 0=local/role-bound      1=universalised
  AW  Affective Weighting         0=cognitive             1=affective
"""

import itertools
import logging

import numpy as np
import scipy.stats as stats

# ---------------------------------------------------------------------------
# Canonical correlation matrix R
# Source: thesis v0.6 Appendix D, Table D.1 (verified PSD, min eigenvalue 0.311)
# HUMAN-OWNED: do not modify entries without panel review.
# ---------------------------------------------------------------------------

PARAM_NAMES = ["LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW"]

R = np.array([
    #  LL     CS     RT     MoR    RE     PD     TfA    ID     MS     AW
    [ 1.00,  0.30,  0.10, -0.10, -0.25,  0.15, -0.20,  0.45,  0.20,  0.05],  # LL
    [ 0.30,  1.00,  0.25,  0.30, -0.30,  0.05, -0.35,  0.20,  0.15,  0.25],  # CS
    [ 0.10,  0.25,  1.00,  0.20, -0.10,  0.15, -0.30,  0.15,  0.35,  0.25],  # RT
    [-0.10,  0.30,  0.20,  1.00, -0.15, -0.10, -0.10,  0.05,  0.10,  0.15],  # MoR
    [-0.25, -0.30, -0.10, -0.15,  1.00, -0.10,  0.25, -0.20, -0.15,  0.25],  # RE
    [ 0.15,  0.05,  0.15, -0.10, -0.10,  1.00, -0.10,  0.10,  0.20, -0.10],  # PD
    [-0.20, -0.35, -0.30, -0.10,  0.25, -0.10,  1.00, -0.25, -0.40, -0.15],  # TfA
    [ 0.45,  0.20,  0.15,  0.05, -0.20,  0.10, -0.25,  1.00,  0.25,  0.25],  # ID
    [ 0.20,  0.15,  0.35,  0.10, -0.15,  0.20, -0.40,  0.25,  1.00, -0.15],  # MS
    [ 0.05,  0.25,  0.25,  0.15,  0.25, -0.10, -0.15,  0.25, -0.15,  1.00],  # AW
])

# Beta marginal parameters: (alpha, beta) per parameter (thesis v0.6 Table 1)
BETA_PARAMS = {
    "LL":  (3.5, 2.5),   # mean 0.583, internal-leaning (GCOS)
    "CS":  (2.5, 2.0),   # mean 0.556, slight high (HPRS)
    "RT":  (2.5, 2.5),   # mean 0.500, symmetric (UG rejection)
    "MoR": (2.0, 2.5),   # mean 0.444, internal (STAXI/IRI/Thomas-Kilmann)
    "RE":  (2.0, 3.0),   # mean 0.400, atomised (Singelis SCS)
    "PD":  (2.5, 2.0),   # mean 0.556, outcome-leaning (Colquitt)
    "TfA": (2.0, 3.5),   # mean 0.364, egalitarian (SDO7)
    "ID":  (3.0, 2.0),   # mean 0.600, endorsement (SRQ)
    "MS":  (1.8, 1.5),   # mean 0.545, flat/universal (MES)
    "AW":  (2.2, 2.5),   # mean 0.468, slight cognitive (Davis IRI) — preliminary
}

# Population means per parameter (Beta mean = alpha / (alpha + beta)).
# Used by Phase 0b null condition B and Phase 1.5 sweeps/rotations.
POPULATION_MEANS = {
    name: round(a / (a + b), 3) for name, (a, b) in BETA_PARAMS.items()
}

# ---------------------------------------------------------------------------
# Societal configuration space: 2^5 grid over (Freedom, Justice, Authority,
# Care, Loyalty). Configuration codes are 5-character binary strings in that
# axis order, e.g. "00100" = the Milgram-analogue (Auth=1, all else low).
# The proof-of-concept tests a defensible subset of 8-12 configurations
# selected per thesis v0.6 §4.3 (per-axis coverage + anchors + max-entropy).
# ---------------------------------------------------------------------------

CONFIG_AXES = ["Freedom", "Justice", "Authority", "Care", "Loyalty"]

ALL_CONFIGS = ["".join(bits) for bits in
               ("".join(map(str, c)) for c in itertools.product((0, 1), repeat=5))]

MILGRAM_ANALOGUE = "00100"          # F=0, J=0, A=1, C=0, L=0 — anchor config
MILGRAM_INVERSE = "11011"           # full inverse — second anchor config


def config_to_axes(code: str) -> dict:
    """Translate a 5-bit configuration code into a {axis: 0|1} mapping."""
    if len(code) != 5 or any(ch not in "01" for ch in code):
        raise ValueError(f"Configuration code must be 5 binary digits, got {code!r}")
    return dict(zip(CONFIG_AXES, (int(ch) for ch in code)))


# ---------------------------------------------------------------------------
# PSD verification
# ---------------------------------------------------------------------------

def verify_psd(matrix: np.ndarray, label: str = "R") -> float:
    """
    Verify that a matrix is positive semi-definite.
    Returns the minimum eigenvalue. Raises AssertionError if not PSD.
    Call this after any modification to R (CLAUDE.md non-negotiable rule).
    """
    eigenvalues = np.linalg.eigvalsh(matrix)
    min_eig = float(np.min(eigenvalues))
    assert min_eig > 0, (
        f"Matrix {label} is NOT positive semi-definite. "
        f"Min eigenvalue = {min_eig:.4f}. "
        "Do not proceed. Restore R or apply Higham (2002) nearest-PSD algorithm."
    )
    return min_eig


# Run PSD check at import time — fail loudly if R has been corrupted.
_MIN_EIG = verify_psd(R, label="R")


# ---------------------------------------------------------------------------
# Gaussian copula sampling (thesis v0.6 §3.4.2)
# ---------------------------------------------------------------------------

def sample_agents(n: int, seed: int | None = None,
                  corr: np.ndarray | None = None) -> np.ndarray:
    """
    Sample n agents from the Gaussian copula over the ten Beta marginals.

    Step 1:  z ~ MVN(0, R)
    Step 2:  u = Phi(z)            (standard normal CDF)
    Step 3:  x = BetaInvCDF(u)     (per-parameter marginal transform)

    Returns an (n, 10) array, columns in PARAM_NAMES order, all values in
    [0, 1]. Marginals are preserved exactly; R supplies the dependency
    structure.

    Parameters
    ----------
    n : int
        Number of agents to sample.
    seed : int or None
        Random seed. Always provide in production runs (config/seeds.json
        maps phase-name -> root seed per the Implementation Specification).
    corr : ndarray or None
        Correlation matrix override for sensitivity regimes B/C/D and the
        t-copula comparison harness. Defaults to the canonical R. Any
        override is PSD-verified before use.
    """
    matrix = R if corr is None else corr
    if corr is not None:
        verify_psd(matrix, label="R (override)")

    rng = np.random.default_rng(seed)
    z = rng.multivariate_normal(mean=np.zeros(len(PARAM_NAMES)),
                                cov=matrix, size=n)
    u = stats.norm.cdf(z)
    x = np.column_stack([
        stats.beta.ppf(u[:, i], *BETA_PARAMS[name])
        for i, name in enumerate(PARAM_NAMES)
    ])
    return x


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

def setup_logger(name: str, log_path: str | None = None) -> logging.Logger:
    """Configure a logger that writes to console and (optionally) a file."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s  %(name)s  %(levelname)s  %(message)s")
    if not logger.handlers:
        console = logging.StreamHandler()
        console.setFormatter(fmt)
        logger.addHandler(console)
        if log_path:
            fh = logging.FileHandler(log_path, encoding="utf-8")
            fh.setFormatter(fmt)
            logger.addHandler(fh)
    return logger


def log_dataframe_summary(df, label: str, logger: logging.Logger) -> None:
    """
    Print row count, column names, dtypes, and missing-value counts.
    Call after every data transformation (CLAUDE.md non-negotiable rule).
    """
    logger.info("[%s] rows=%d  cols=%s", label, len(df), list(df.columns))
    logger.info("[%s] dtypes:\n%s", label, df.dtypes.to_string())
    missing = df.isna().sum()
    missing = missing[missing > 0]
    if missing.empty:
        logger.info("[%s] no missing values", label)
    else:
        logger.warning("[%s] missing values:\n%s", label, missing.to_string())


def log_agent_summary(agents: np.ndarray, config_code: str,
                      logger: logging.Logger) -> None:
    """
    Print per-parameter summary statistics for a sampled agent population.
    Call after sample_agents() (CLAUDE.md non-negotiable rule).
    """
    logger.info("Agent population for config %s: N=%d", config_code, len(agents))
    for i, name in enumerate(PARAM_NAMES):
        col = agents[:, i]
        expected = POPULATION_MEANS[name]
        logger.info(
            "  %-4s mean=%.3f (expected %.3f)  sd=%.3f  min=%.3f  max=%.3f",
            name, col.mean(), expected, col.std(ddof=1), col.min(), col.max(),
        )
    out_of_range = ((agents < 0) | (agents > 1)).sum()
    if out_of_range:
        logger.error("%d values outside [0, 1] — sampling bug", out_of_range)
