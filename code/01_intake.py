"""
01_intake.py — Load and validate raw calibration data.

Phase: 2 (Distribution Modelling)
Input:  data/raw/ — empirical calibration data from psychometric instruments
Output: data/processed/calibration_validated.parquet — validated, typed, documented

Done when:
  - All raw files loaded without error
  - Row counts, column types, and key distributions printed
  - No unexpected nulls in identifier columns
  - Value ranges match expected instrument scales
  - Output written to data/processed/

Instruments expected in data/raw/:
  SDO (Pratto et al., 1994)        → TfA proxy
  GCOS (Deci & Ryan, 1985)         → PLB proxy
  HPRS (Hong & Faedda, 1996)       → CS proxy
  MFQ-2 (Atari et al., 2023)       → SMG proxy
  SCS (Singelis, 1994)             → RE proxy
  STAXI (Spielberger, 1988)        → MoR proxy
  SRQ (Ryan & Connell, 1989)       → ID proxy
  CFC (Strathman et al., 1994)     → TO proxy
  Colquitt (2001) Justice Scale    → PD proxy
  Ultimatum Game rejection data    → CAT proxy
"""

# TODO (Phase 2 / Phase 3): implement data intake and validation.
# See CLAUDE.md Non-Negotiable Rule 3 — print row count, columns, missing values
# after every load. See Verification Checklist §9 in research-os-template.md.

raise NotImplementedError("01_intake.py is not yet implemented.")
