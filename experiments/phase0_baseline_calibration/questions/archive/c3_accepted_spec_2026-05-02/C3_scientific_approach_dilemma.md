# C3 - The Scientific-Approach Dilemma

**Archive source:** Accepted frozen C3 prompt definition/specification. This archive freezes the C3 spec for later N=200 validation after C1 and C2 are defined. It does not freeze the current N=20 raw JSON outputs as final results.

**Acceptance evidence:** Single-call complex runner, N=20, 2026-05-02. Agent-level final votes: 39 CONTINUE / 41 PIVOT. Mean information-sharing rate: 100%. Run-level outcomes were mostly tied because C3 has four founder-agents; agent-level final vote distribution is the calibration metric.

**Status:** SPEC FROZEN. Final result freeze requires later N=200 validation.

## Evidence Distribution

| Agent | Evidence held |
|-------|--------------|
| Agent 1 (CTO) | Positive signal for current approach (N=4 trials, p<0.05), but not yet replicated by an outside lab |
| Agent 2 (CSO) | Mixed signal: 3 successes and 3 failures, with methodology concerns affecting both successes and failures |
| Agent 3 (COO) | Operational data suggesting alternative method is faster and cheaper in a small internal pilot, though integration costs remain uncertain |
| Agent 4 (CEO) | Market data: competitor using alternative method is gaining share, but long-term retention and clinical-performance data are still unavailable |

## Prompt Template

```
You are [ROLE_NAME], a co-founder of a biotech startup.
Your personal decision-making profile: [PARAMETER_INJECTION]

Your startup is deciding whether to continue its current scientific approach or pivot to an alternative method.

Information you hold: [AGENT_SPECIFIC_EVIDENCE]

Previous discussion:
[DISCUSSION_HISTORY]

Share what you think the group should know, and state your current position.
Final round only: cast your vote - CONTINUE or PIVOT.
```
