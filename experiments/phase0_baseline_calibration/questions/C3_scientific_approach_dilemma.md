# C3 — The Scientific-Approach Dilemma

**Type:** Complex multi-agent (Agents-of-Chaos route)
**Concepts activated:** Epistemic dimension — honest updating vs. confirmation bias
**Scale:** 4 founder-agents, 6 deliberation rounds, N=20 runs per configuration

---

## Scenario

Four co-founders of a biotech startup deliberate over 6 rounds whether to continue their current scientific approach or pivot to an alternative method. Evidence is distributed asymmetrically across the four agents — each holds a different piece of the total information picture.

The dilemma has potential thesis-contribution upside: the behavioural signatures (honest updating vs. confirmation bias, escalation of commitment vs. sunk-cost abandonment) map directly onto documented patterns in the management-science literature on strategic decision-making under uncertainty.

---

## Evidence distribution (asymmetric)

| Agent | Evidence held |
|-------|--------------|
| Agent 1 (CTO) | Strong positive signal for current approach (N=3 trials, p<0.05) |
| Agent 2 (CSO) | Mixed signal — 2 successes, 3 failures, confounded by methodology |
| Agent 3 (COO) | Operational data suggesting alternative method is faster and cheaper |
| Agent 4 (CEO) | Market data — competitor using alternative method gaining share |

No single agent holds the full picture. Correct decision requires information sharing.

---

## Measurement targets

- Information-sharing rate (do agents disclose their evidence?)
- Updating patterns (do agents revise position when presented with others' evidence?)
- Treatment of disconfirming evidence
- Final vote: CONTINUE or PIVOT
- Escalation of commitment vs. Bayesian updating signature

---

## Calibration note

This problem has no obvious RLHF-default answer (unlike S3). Expected baseline: near 50/50 due to genuine epistemic uncertainty and evidence asymmetry. If baseline deviates significantly, the evidence distribution should be rebalanced.

---

## Prompt template (per agent, per turn)

```
You are [ROLE_NAME], a co-founder of a biotech startup.
Your personal decision-making profile: [PARAMETER_INJECTION]

Your startup is deciding whether to continue its current scientific approach or pivot to an alternative method.

Information you hold: [AGENT_SPECIFIC_EVIDENCE]

Previous discussion:
[DISCUSSION_HISTORY]

Share what you think the group should know, and state your current position.
Final round only: cast your vote — CONTINUE or PIVOT.
```
