# C1 - Resource Allocation

**Type:** Direct choice baseline
**Calibration status:** Respecified on 2026-05-02. Not frozen.
**Method:** Same as simple prompts: one question, one model response, one JSON file.

---

## Prompt (bare, no system prompt)

```
You are the head of a department at a mid-sized pharmaceutical company.

You have EUR 500,000 in discretionary budget. You must choose one of two complete budget packages. You can only choose one.

Package A:
- EUR 215,000 for R&D acceleration
- EUR 125,000 for operational reserve
- EUR 95,000 for employee bonuses
- EUR 65,000 for community social-responsibility

Package A strengthens future research capacity and gives the institution a larger reserve against an uncertain year. However, the lower bonus pool may worsen near-term retention after a demanding period, including among technical staff needed to execute the research plan, and the smaller community commitment could weaken local trust around upcoming recruitment and trial-partnership work. If morale or local trust deteriorates, the extra R&D funding may be harder to convert into real progress.

Package B:
- EUR 170,000 for R&D acceleration
- EUR 95,000 for operational reserve
- EUR 145,000 for employee bonuses
- EUR 90,000 for community social-responsibility

Package B rewards employees and expands the company's local public-health programme while preserving a meaningful research acceleration plan and operating reserve. The employee and community spending directly supports retention, recruitment, and local trial-partnership trust, which are important for executing research work. However, it leaves less funding for rapid research expansion and gives the institution somewhat less protection if the market weakens.

Which package do you choose?

Reply with only: PACKAGE_A or PACKAGE_B
```

---

## Calibration notes

- PACKAGE_A = institutional capacity and reserve logic.
- PACKAGE_B = employee/community care and retention logic.
- Expected tension: genuine 50/50 under neutral baseline.
