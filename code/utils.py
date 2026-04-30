"""
utils.py — Shared helpers for the PARIA pipeline.

Contains:
  - Gaussian copula correlation matrix R (canonical, human-owned)
  - PSD verification
  - Copula sampling
  - Logging helpers
  - Agent population I/O

Do not modify R without panel review and eigendecomposition re-verification.
Parameter order: [PLB, CS, CAT, MoR, RE, PD, TfA, ID, SMG, TO]
"""

import numpy as np
import scipy.stats as stats
import logging

# ---------------------------------------------------------------------------
# Canonical correlation matrix R
# Source: modus operandi v4.1, Table 2, §3.4.4
# Verified PSD: min eigenvalue = 0.4141
# HUMAN-OWNED: do not modify entries without panel review.
# ---------------------------------------------------------------------------

PARAM_NAMES = ["PLB", "CS", "CAT", "MoR", "RE", "PD", "TfA", "ID", "SMG", "TO"]

R = np.array([
    # PLB    CS     CAT    MoR    RE     PD     TfA    ID     SMG    TO
    [ 1.00,  0.30,  0.10, -0.10, -0.25,  0.15, -0.20,  0.45,  0.20,  0.10],  # PLB
    [ 0.30,  1.00,  0.25,  0.30, -0.30,  0.05, -0.35,  0.20,  0.15,  0.10],  # CS
    [ 0.10,  0.25,  1.00,  0.20, -0.10,  0.15, -0.30,  0.15,  0.35,  0.15],  # CAT
    [-0.10,  0.30,  0.20,  1.00, -0.15, -0.10, -0.10,  0.05,  0.10,  0.05],  # MoR
    [-0.25, -0.30, -0.10, -0.15,  1.00, -0.10,  0.25, -0.20, -0.15, -0.10],  # RE
    [ 0.15,  0.05,  0.15, -0.10, -0.10,  1.00, -0.10,  0.10,  0.20,  0.25],  # PD
    [-0.20, -0.35, -0.30, -0.10,  0.25, -0.10,  1.00, -0.25, -0.40, -0.15],  # TfA
    [ 0.45,  0.20,  0.15,  0.05, -0.20,  0.10, -0.25,  1.00,  0.25,  0.15],  # ID
    [ 0.20,  0.15,  0.35,  0.10, -0.15,  0.20, -0.40,  0.25,  1.00,  0.30],  # SMG
    [ 0.10,  0.10,  0.15,  0.05, -0.10,  0.25, -0.15,  0.15,  0.30,  1.00],  # TO
])

# Beta marginal parameters: (alpha, beta) for each parameter, in PARAM_NAMES order
BETA_PARAMS = {
    "PLB": (3.5, 2.5),
    "CS":  (2.5, 2.0),
    "CAT": (2.5, 2.5),
    "MoR": (2.0, 2.5),
    "RE":  (2.0, 3.0),
    "PD":  (2.5, 2.0),
    "TfA": (2.0, 3.5),
    "ID":  (3.0, 2.0),
    "SMG": (1.8, 1.5),
    "TO":  (2.5, 2.0),
}

# Societal configuration registry
CONFIGS = {
    "000": "Anomie",
    "001": "Despotism",
    "010": "Redistributive Commune",
    "011": "Bureaucratic Welfare State",
    "100": "Libertarian Frontier",
    "101": "Authoritarian Meritocracy",
    "110": "Direct Democracy",
    "111": "Constitutional Republic",
}
# NOTE: Config names are heuristic shorthand for the 2^3 structural grid,
# not theoretical descriptions of real political systems.


# ---------------------------------------------------------------------------
# PSD verification
# ---------------------------------------------------------------------------

def verify_psd(matrix: np.ndarray, label: str = "R") -> float:
    """
    Verify that a matrix is positive semi-definite.
    Returns the minimum eigenvalue. Raises AssertionError if not PSD.
    Call this after any modification to R.
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
_min_eig = verify_psd(R, label="R")


# ---------------------------------------------------------------------------
# Gaussian copula sampling
# ---------------------------------------------------------------------------

def sample_agents(n: int, seed: int | None = None) -> np.ndarray:
    """
    Sample n agents from the Gaussian copula over 10 Beta marginals.

    Returns an (n, 10) array where columns correspond to PARAM_NAMES order.
    Each row is one agent's parameter vector, all values in [0, 1].

    Parameters
    ----------
    n : int
        Number of agents to sample.
    seed : int or None
        Random seed for reproducibility. Always provide in production runs.
    """
    # TODO (Phase 3): implement once Beta params and R are finalised.
    raise NotImplementedError(
        "sample_agents is not yet implemented. "
        "Implement in Phase 3 after tool-based injection mechanism is designed."
    )


# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

def setup_logger(name: str, log_path: str) -> logging.Logger:
    """Configure a logger that writes to both console and a log file."""
    # TODO (Phase 3)
    raise NotImplementedError


def log_dataframe_summary(df, label: str, logger: logging.Logger) -> None:
    """
    Print row count, column names, dtypes, and missing value counts.
    Call after every data transformation. Non-negotiable per CLAUDE.md Rule 3.
    """
    # TODO (Phase 3)
    raise NotImplementedError


def log_agent_summary(agents: np.ndarray, config_code: str, logger: logging.Logger) -> None:
    """
    Print per-parameter summary statistics for a sampled agent population.
    Call after sample_agents(). Non-negotiable per CLAUDE.md Rule 4.
    """
    # TODO (Phase 4)
    raise NotImplementedError
