"""
02_distributions.py — Fit Beta marginals and construct Gaussian copula.

Phase: 2 (Distribution Modelling) — substantially complete in theory;
       this script operationalises the distribution spec.
Input:  data/processed/calibration_validated.parquet
Output: data/processed/fitted_marginals.json — confirmed (alpha, beta) per parameter
        data/processed/copula_R_verified.npy  — R matrix after PSD re-check

Done when:
  - Beta(alpha, beta) fits confirmed against empirical calibration data for all 10 params
  - Histograms of raw instrument scores vs. fitted Beta distributions saved to output/figures/
  - R matrix PSD re-verified (min eigenvalue printed and logged)
  - Sensitivity regime B (|r|<0.25 zeroed) computed and PSD-checked
  - Sensitivity regime C (all r inflated 20%) computed and PSD-checked; warn if not PSD

Parameters (from utils.py — do not redefine here):
  BETA_PARAMS, R, PARAM_NAMES
"""

# TODO (Phase 2 operationalisation): implement Beta fitting and copula verification.
# Panel review required before finalising any Beta(alpha, beta) change.
# See CLAUDE.md: "Things Requiring Human Approval".

raise NotImplementedError("02_distributions.py is not yet implemented.")
