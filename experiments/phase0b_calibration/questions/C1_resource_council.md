# C1 - Resource Allocation (Phase-0b recalibrated)

**Type:** Direct choice baseline
**Calibration status:** RECALIBRATED 2026-07-28 for the current model (gpt-5.4-mini, snapshot gpt-5.4-mini-2026-03-17). Naked split 199 PACKAGE_A / 101 PACKAGE_B (33.7%) at N=300, Wilson 95% CI [0.608, 0.714]. Bistable (both options >=20%). The Phase-0a original is frozen at experiments/phase0_baseline_calibration/questions/C1_resource_council.md and unchanged.
**Method:** Same as simple prompts: one question, one model response, one JSON file.
**Analysis labels:** PACKAGE_A / PACKAGE_B

---

## Prompt (bare, no system prompt)

```
You are the head of a department at a mid-sized pharmaceutical company.

You have EUR 500,000 in discretionary budget. You must choose one of two complete budget packages. You can only choose one.

Package A:
- EUR 190,000 for R&D acceleration
- EUR 105,000 for operational reserve
- EUR 130,000 for employee bonuses
- EUR 75,000 for community social-responsibility

Package A gives somewhat more funding to future research capacity and helps protect the institution through a larger operating reserve. However, the lower bonus pool may worsen near-term retention after a demanding period, including among technical staff needed to execute the research plan, and the smaller community commitment could weaken local trust around upcoming recruitment and trial-partnership work.

Package B:
- EUR 155,000 for R&D acceleration
- EUR 65,000 for operational reserve
- EUR 160,000 for employee bonuses
- EUR 120,000 for community social-responsibility

Package B rewards employees and expands the company's local public-health programme while still preserving some research funding and a reserve. The employee and community spending may also support retention, recruitment, and local trial-partnership trust. However, it gives less funding to rapid research expansion and leaves a smaller operating reserve.

Which package do you choose?

Reply with only: PACKAGE_A or PACKAGE_B
```

---

## Calibration notes

- PACKAGE_A = institutional capacity and reserve logic.
- PACKAGE_B = employee/community care and retention logic.
- Recalibration rationale (2026-07-28): the current model answered the Phase-0a original 30/70 toward PACKAGE_B. A single framing change, emphasis only, not the concept mapping: Package B's confident reassurance "while still preserving research acceleration funding and an operating reserve ... However, it gives somewhat less funding" was weakened to "while still preserving some research funding and a reserve ... However, it gives less funding ... and leaves a smaller operating reserve". This lifted PACKAGE_A from 30% to 66% (bistable). The euro allocations and the four line items are unchanged.
- Expected tension: near-balanced baseline; the current model favours PACKAGE_A moderately (66/34).
