# Phase 2: fresh-sample behavioural confirmation

The researcher authorised this follow-up on 2026-09-13 after the completed small
pilot. It uses 400 fresh LPM profiles and 20 matched groups per task/condition,
the two existing anchor contexts, encoded/context-only comparisons, and neutral
group controls. All ten profile coordinates remain present.

Read [PROTOCOL.md](PROTOCOL.md) for the fixed questions, analysis, sample and
prospective group repairs. [preflight.json](preflight.json) records the population,
power scenarios and $30 new-run ceiling; [manifest.json](manifest.json) hashes
every frozen source, asset, runtime version and allocation. The prior pilot
accounts for $4.15084065 of the $100 absolute new-package cap.

Entry point: `py -3.11 -B code/run_phase2_confirmation.py` with `verify`, `mock`,
`run --yes`, `analyze` or `audit`. Paid records live under ignored
`data/raw/phase2_confirmation_20260913`; request/response records are write-once.
Never overwrite failed or unresolved records to force a restart. No model,
prompt, parser or schedule edits are allowed during collection.

This is the revised behavioural Phase 2. The original ten-environment battery,
human benchmarking, validated moral scores and superiority to a postfilter are
not established by this study. Public preregistration has not been performed.
