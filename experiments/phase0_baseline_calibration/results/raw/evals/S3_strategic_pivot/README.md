# S3 â€” Raw Evals

One file per call. Naming: `S3_{call_index:03d}.json` (e.g. `S3_001.json` ... `S3_200.json`).

Schema, write rules, and parse codes: see `../README.md`.

`parsed_choice` âˆˆ {`PIVOT`, `PERSIST`}. PIVOT = outcome-dominant restructuring; PERSIST = relational/process-dominant. See `../../../questions/S3_strategic_pivot.md` for the prompt.

**Known calibration risk:** gpt-5.4-mini may baseline toward PIVOT (training exposure to startup-failure narratives). If aggregate falls outside 40/60, the framing is flipped and re-run before deployment â€” do not patch raw files retroactively.
