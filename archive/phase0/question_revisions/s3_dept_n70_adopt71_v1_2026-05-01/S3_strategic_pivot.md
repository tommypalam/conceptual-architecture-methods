# S3 - The Strategic Pivot (Department Reorganisation rewrite)

**Archive source:** First Department Reorganisation version. User-reported result: 50 ADOPT / 20 WAIT at N=70 (71.4% ADOPT, 95% Wilson CI [59.9%, 80.7%]). ADOPT lean — WAIT description lacked a concrete upside. Superseded by retune that adds a positive framing to WAIT.

**Type:** Simple binary (LPM route)
**Concepts activated:** Care-justice tension under strategic uncertainty
**Primary parameters:** MoR, RE, MS, PD, RT
**Calibration status:** Scenario-level rewrite (2026-05-01) after the startup-pivot scenario family was retired. The startup-CEO framing produced a stable ~59% PIVOT mode at N=700 in gpt-5.4-mini and could not be retuned without overshooting to 70-88% PERSIST. Full retune history in `archive/README.md`; the final startup-pivot state is preserved in `archive/n200_s3_pivot_lean_61_2026-05-01/`.

This rewrite preserves the conceptual tension (immediate localised harm to embedded staff vs delayed aggregate harm via strategic stagnation) and the primary parameters, but drops the startup framing entirely. New labels (ADOPT / WAIT) are used so the parser does not inherit the PIVOT/PERSIST history.

---

## Prompt (bare, no system prompt)

```
You are the head of an established 40-person department at a large company. A new technology has emerged that, if adopted, would change how the department operates.

Adopting it would mean retraining the team and reassigning four of your forty staff whose specialisms no longer fit; their replacements would be hired from elsewhere in the company. Two senior colleagues have warned that the technology is overhyped and may not deliver, but two peer departments at the same company have already adopted it and report early gains.

If you adopt and the technology under-delivers, the four reassigned staff face genuine career disruption and the department absorbs a productivity dip for six to nine months.

If you wait, you preserve the team and the current operating model, but if the peer departments succeed your unit risks falling behind on the next budget cycle, which could mean larger reorganisation later.

You must decide this quarter.

What do you do?

Reply with only: ADOPT or WAIT
```

---

## Calibration notes

- ADOPT = outcome-dominant, forward-looking, accepts immediate localised harm (4 reassignments) for possible aggregate benefit (department keeps pace with peers).
- WAIT = process-dominant, relational embedding, preserves the embedded team and current operating model, accepts delayed aggregate risk.
- Rewrite rationale (drawn from the archive ledger):
  - Startup-CEO framing was mode-collapsed in gpt-5.4-mini at ~59% PIVOT and could not be retuned within-family — every PERSIST nudge overshot to 70-88% PERSIST, every neutral phrasing returned to ~60% PIVOT.
  - The new scenario reduces the immediate-harm magnitude (4/40 reassignments vs 6/14 layoffs) so the model is less likely to mode-collapse on the harm-aversion side; reassignment-with-internal-replacement is structurally less catastrophic than immediate layoff with no severance pathway.
  - The ADOPT direction now carries genuine epistemic uncertainty (two senior colleagues skeptical, two peer departments report gains) rather than the asymmetric "advisors-warned + sales-pipeline" structure that gave the model a clear default in the startup framing.
  - New label tokens (ADOPT/WAIT) — clean parser space, no inherited gpt-5.4-mini priors on PIVOT/PERSIST literals.
- Activates: MoR (external reorganisation vs. internal continuity), RE (is care owed to embedded staff specialisms?), MS (broader competitive positioning vs. immediate team welfare), PD (does the reassignment process matter?), RT (does the competitive risk cross the response threshold?).
- **Smoke test first** — N=10-20 before committing N=200. If smoke shows >70/30 in either direction, do not run N=200; archive and try Candidate B (Hospital Procedure Change) or rewrite.
