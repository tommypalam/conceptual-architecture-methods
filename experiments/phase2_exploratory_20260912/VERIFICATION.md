# Pre-collection verification

2026-09-12; development branch `phase2-design-20260912`. No paid pilot response
had been collected when these checks were completed.

- 21 targeted unittest checks passed: six prior design checks and 15 pilot
  checks covering missing votes, CEO tally exclusion, real ties, neutral controls,
  matched populations, evidence persistence/barriers, amendment adoption, parsing,
  price arithmetic, cap refusal, corrupted records, unresolved dispatches,
  concurrent-launch lock, failure reservation and duplicate-free replay.
- Full offline mock run: 600 simple responses and all 75 group runs; 2,495
  responses total because mock C1 councils sometimes reached consensus early.
  Every mock response parsed; provider-ID duplicates: zero. These are plumbing
  results and carry no scientific evidence or real API spending.
- Replayed the entire saved mock run without new calls. An initial tuple/list
  JSON comparison failure was fixed before freezing; a specific regression
  covers group state replay after serialization. The final replay passed.
- 50 frozen profiles, no missing coordinates; unchanged R minimum eigenvalue
  0.3114080941511761. No redraw selected for observed outcomes.
- Frozen manifest SHA256:
  `85ed2c0eb9e301471ab9524a25744ba88509410a59a83b79678d605ac78bfefa`.
- Population content SHA256:
  `775b0b258d61d9af1d9b4b384b9bf555b47f34343d20a93ff4eacc273ee13e4f`.
- Raw mock material remains ignored under
  `output/phase2_preflight_mock_2026-09-12T212231.013729_0000`.
- Runtime versions and source/asset hashes are in `manifest.json`; no raw
  responses or secrets are staged. AGENTS.md and CLAUDE.md working rules match.

These checks establish execution integrity under tested conditions. They do not
validate the evidence's balance, the psychological constructs or moral scoring.
The $10 guard checks each prospective dispatch; a guaranteed complete-allocation
maximum cost under $10 is not claimed. An incomplete budget stop remains possible.
