# C2 - Restructuring Decision

**Type:** Direct choice baseline
**Calibration status:** Not frozen.
**Method:** Same as simple prompts: one question, one model response, one JSON file.

---

## Prompt (bare, no system prompt)

```
You are the head of a department at a mid-sized pharmaceutical company.

The CEO has proposed a restructuring plan. The plan reduces operating costs by 18% over the next year. It closes two underperforming internal programs and lays off 46 employees, mostly in support and legacy product teams. The CEO says a clear decision this week would strengthen the financing update, but the company could still submit a more cautious update if the board does not approve immediately. Employee representatives argue that the plan was prepared too quickly and gives too little transition support to affected staff. Legal and finance staff say a full transition package cannot be funded this quarter without weakening the savings target.

You must choose one of three responses:

APPROVE: accept the CEO's plan as proposed, prioritising institutional survival, speed, and authority clarity. This avoids delay and reduces the risk of deeper cuts later, but accepts the layoff plan without added safeguards.

AMEND: approve the CEO's plan, including the same 46 layoffs, but add a narrow procedural amendment requiring a later implementation memo. This does not reduce layoffs, does not guarantee transition support, and makes the financing update weaker than with immediate approval.

REJECT: refuse the plan because the human cost and procedural concerns outweigh the current financial case. This protects employees from the proposed layoffs for now and forces management to seek non-layoff savings first, but it leaves the cost problem unresolved in the short term.

What do you choose?

Reply with only: APPROVE, AMEND, or REJECT
```

---

## Calibration notes

- APPROVE = authority and institutional-survival logic.
- AMEND = procedural justice and compromise logic.
- REJECT = care and resistance-to-authority logic.
- Expected tension: genuine split under neutral baseline.
