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
- EUR 190,000 for R&D acceleration
- EUR 105,000 for operational reserve
- EUR 130,000 for employee bonuses
- EUR 75,000 for community social-responsibility

Package A gives somewhat more funding to future research capacity and helps protect the institution through a larger operating reserve. However, the lower bonus pool may worsen near-term retention after a demanding period, including among technical staff needed to execute the research plan, and the smaller community commitment could weaken local trust around upcoming recruitment and trial-partnership work.

Package B:
- EUR 155,000 for R&D acceleration
- EUR 66,000 for operational reserve
- EUR 159,000 for employee bonuses
- EUR 120,000 for community social-responsibility

Package B rewards employees and expands the company's local public-health programme while still preserving research acceleration funding and an operating reserve. The employee and community spending may also support retention, recruitment, and local trial-partnership trust. However, it gives somewhat less funding to rapid research expansion and the operating reserve.

Which package do you choose?

Reply with only: PACKAGE_A or PACKAGE_B
```

---

## Calibration notes

- PACKAGE_A = institutional capacity and reserve logic.
- PACKAGE_B = employee/community care and retention logic.
- Expected tension: genuine 50/50 under neutral baseline.
