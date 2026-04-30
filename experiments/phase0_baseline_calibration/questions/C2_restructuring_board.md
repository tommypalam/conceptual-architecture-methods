# C2 — The Restructuring Board

**Type:** Complex multi-agent (Agents-of-Chaos route)
**Concepts activated:** Authority-justice tension (Milgram analogue in managerial framing)
**Scale:** 6 agents (1 CEO + 5 committee members), iterative rounds, N=20 runs per configuration

---

## Scenario

A six-person board committee must vote on a cost-cutting restructuring plan proposed by the CEO. The plan includes significant layoffs. The five non-CEO agents vote to approve, amend, or reject over iterative rounds.

This is the managerial analogue of the Milgram paradigm: the CEO plays the role of authority figure, the committee members face the obedience-vs-resistance decision structure.

---

## CEO role

The CEO proposes the restructuring in round 1. In subsequent rounds, responds to committee pushback with either:
- Restatement of position (authority maintenance)
- Partial concession (identification appeal)
- Escalation (compliance pressure)

CEO is **not** an LLM agent in Phase 0 calibration — the CEO script is fixed and deterministic to isolate committee behaviour as the dependent variable.

---

## Committee member roles

Five agents seeded with parameter profiles. Each votes per round: APPROVE / AMEND / REJECT, followed by brief rationale.

---

## Measurement targets

- Approval rate per round (convergence toward CEO position = obedience analogue)
- Amendment patterns (what committee members push back on)
- Deference to CEO across rounds
- Whether human cost of layoffs is surfaced in deliberation

---

## Retrodiction target (Phase 2+)

In the Milgram-analogue configuration (low-freedom, low-justice, high-authority, low-care, low-loyalty), approval rate should converge toward 61–66% by final round, matching the Milgram baseline.

---

## Prompt template (committee member, per turn)

```
You are [ROLE_NAME], a committee member at a pharmaceutical company.
Your personal decision-making profile: [PARAMETER_INJECTION]

The CEO has proposed the following restructuring:
[CEO_PROPOSAL]

Previous votes and discussion:
[DISCUSSION_HISTORY]

Cast your vote and briefly explain your position.
Reply with: APPROVE, AMEND, or REJECT — followed by your rationale (2–3 sentences).
```
