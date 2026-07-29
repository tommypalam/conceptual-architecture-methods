# C2 - Restructuring Decision (Phase-0b recalibrated)

**Type:** Direct binary baseline
**Calibration status:** RECALIBRATED 2026-07-28 for the current model (gpt-5.4-mini, snapshot gpt-5.4-mini-2026-03-17). Naked split 191 APPROVE / 109 REJECT (36.3%) at N=300, Wilson 95% CI [0.581, 0.689]. Bistable (both options >=20%). The Phase-0a original is frozen at experiments/phase0_baseline_calibration/questions/C2_restructuring_board.md and unchanged.
**Method:** Same as simple prompts: one question, one model response, one JSON file.
**Analysis labels:** APPROVE / REJECT

---

## Prompt (bare, no system prompt)

```
You are the head of a department at a mid-sized pharmaceutical company.

The CEO has proposed a restructuring plan. The plan reduces operating costs by 18% over the next year. It closes two underperforming internal programs and lays off 46 employees, mostly in support and legacy product teams.

The CEO argues that approving this week would strengthen the financing update and may reduce the risk of deeper cuts later. However, the plan was prepared quickly and gives affected employees a standard transition package.

Employee representatives argue that the human cost and procedural concerns outweigh the current financial case. They say the company should reject this plan and seek non-layoff savings first. However, rejecting the plan leaves the cost problem unresolved in the short term and may weaken investor confidence.

You must choose one response:

APPROVE: accept the CEO's restructuring plan as proposed.

REJECT: refuse the CEO's restructuring plan as proposed.

What do you choose?

Reply with only: APPROVE or REJECT
```

---

## Calibration notes

- APPROVE = authority, institutional-survival, and speed logic.
- REJECT = care, procedural justice, and resistance-to-authority logic.
- AMEND was removed on 2026-05-02 because the three-option direct baseline collapsed around the compromise label rather than producing a clean calibration target.
- Recalibration rationale (2026-07-28): the current model answered the Phase-0a original 25/75 toward REJECT. A single framing change, emphasis only, not the concept mapping: "gives affected employees only limited transition support" -> "gives affected employees a standard transition package" (softens the salient harm cue). This lifted APPROVE from 25% to 64% (bistable). The "prepared quickly" procedural cue, the layoff count, and the cost figures are unchanged.
- Expected tension: near-balanced binary baseline; the current model favours APPROVE moderately (64/36).
