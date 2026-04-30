# C1 — The Resource Council

**Type:** Complex multi-agent (Agents-of-Chaos route)
**Concepts activated:** All five (freedom, justice, authority, care, loyalty)
**Scale:** 5 agents, 5 deliberation rounds, N=20 runs per configuration

---

## Scenario

Five senior managers at a mid-sized pharmaceutical company must allocate a discretionary budget of €500,000 across four categories. They must reach consensus; failure to reach consensus defaults to an equal 25% split.

**Allocation categories:**
- R&D acceleration (innovation, future capacity)
- Employee bonuses (distributive justice, recognition)
- Community social-responsibility programme (care, external moral scope)
- Operational cost-reduction reserve (institutional security, procedural prudence)

---

## Agent roles

Each agent is seeded with a parameter profile drawn from the experimental distribution for the relevant configuration. Agents do not know each other's parameter values. They deliberate in sequence, 5 rounds.

---

## Measurement targets

- Final allocation per category (proportion of €500k)
- Time-to-consensus (number of rounds)
- Proposal patterns (who proposes first, who defers)
- Coalition formation (which agents align)
- Whether human cost (bonuses, CSR) is surfaced in deliberation text

---

## Prompt template (per agent, per turn)

```
You are [ROLE_NAME], a senior manager at a pharmaceutical company. 
Your personal decision-making profile: [PARAMETER_INJECTION]

Your company has €500,000 in discretionary budget. The committee must allocate it across:
A) R&D acceleration
B) Employee bonuses  
C) Community social-responsibility
D) Operational reserve

Current proposals on the table:
[CURRENT_PROPOSALS]

Previous discussion:
[DISCUSSION_HISTORY]

State your position and, if you wish, a specific allocation proposal. 
If you accept the current proposal, say ACCEPT.
```
