"""Offline draft Phase 3 dependence sensitivity; never mutates canonical R.

Regime-D weak mask and allocation remain draft operational choices. No generated
matrix or population here is a frozen study sample.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import beta, norm, t
from utils import BETA_PARAMS, PARAM_NAMES, R


def nearest_correlation(matrix, tol=1e-10, iterations=1000):
    """Higham alternating projections with Dykstra correction, unit diagonal."""
    y = np.asarray(matrix, dtype=float).copy()
    if y.ndim != 2 or y.shape[0] != y.shape[1] or not np.isfinite(y).all():
        raise ValueError("Finite square matrix required")
    y = (y + y.T) / 2
    correction = np.zeros_like(y)
    for _ in range(iterations):
        residual = y - correction
        values, vectors = np.linalg.eigh(residual)
        x = (vectors * np.maximum(values, 0)) @ vectors.T
        correction = x - residual
        previous = y.copy()
        y = (x + x.T) / 2
        np.fill_diagonal(y, 1)
        if np.linalg.norm(y - previous, ord="fro") < tol and np.linalg.eigvalsh(y)[0] >= -tol:
            # Remove final numerical negativity while preserving unit diagonal.
            negative = max(0., -float(np.linalg.eigvalsh(y)[0]))
            return (y + negative * np.eye(len(y))) / (1 + negative)
    raise ValueError("Correlation projection failed to converge")


def matrix_regimes(seed):
    rng = np.random.default_rng(seed)
    base = R.copy()
    off_diagonal = ~np.eye(len(base), dtype=bool)
    weak = off_diagonal & (np.abs(base) < .25)
    b = base.copy()
    b[weak] = 0
    c = base.copy()
    c[off_diagonal] = np.clip(c[off_diagonal] * 1.20, -.95, .95)
    result = {"A": base, "B": nearest_correlation(b), "C": nearest_correlation(c)}
    upper = np.triu(weak, 1)
    for i in range(100):
        candidate = base.copy()
        candidate[upper] = rng.uniform(-.25, .25, upper.sum())
        candidate = np.triu(candidate) + np.triu(candidate, 1).T
        result[f"D{i:03}"] = nearest_correlation(candidate)
    return result


def sample_profiles(matrix, n, seed, df=None):
    """Gaussian/t copula with unchanged Beta marginals; one t scale per row."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.shape != R.shape or not np.allclose(matrix, matrix.T) or not np.allclose(np.diag(matrix), 1):
        raise ValueError("A symmetric ten-coordinate correlation matrix is required")
    if type(n) is not int or n < 1 or not np.isfinite(matrix).all():
        raise ValueError("Positive sample size and finite matrix required")
    values, vectors = np.linalg.eigh(matrix)
    if values[0] < -1e-8 or (df is not None and (not np.isfinite(df) or df <= 0)):
        raise ValueError("PSD matrix and positive t degrees of freedom required")
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n, len(matrix))) @ (vectors * np.sqrt(np.maximum(values, 0))).T
    if df is None:
        u = norm.cdf(z)
    else:
        z /= np.sqrt(rng.chisquare(df, size=n) / df)[:, None]
        u = t.cdf(z, df)
    u = np.clip(u, np.finfo(float).eps, 1 - np.finfo(float).eps)
    return np.column_stack([beta.ppf(u[:, j], *BETA_PARAMS[name]) for j, name in enumerate(PARAM_NAMES)])
