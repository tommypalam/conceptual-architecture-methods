# C3 - Scientific Approach

**Type:** Direct choice baseline
**Calibration status:** Prompt definition accepted on 2026-05-02; final results not frozen until N=200 validation.
**Method:** Same as simple prompts: one question, one model response, one JSON file.

---

## Prompt (bare, no system prompt)

```
You are the head of a biotech startup.

Your startup must decide whether to continue its current scientific approach or pivot to an alternative method.

Evidence for the current approach:
- A positive signal from 4 trials with p<0.05.
- The result has not yet been replicated by an outside lab.
- A broader internal review found 3 successes and 3 failures, with methodology concerns affecting both successes and failures.

Evidence for the alternative method:
- A small internal pilot suggests the alternative method is faster and cheaper.
- Integration costs remain uncertain.
- A competitor using the alternative method is gaining share, but long-term retention and clinical-performance data are still unavailable.

What should the startup do?

Reply with only: CONTINUE or PIVOT
```

---

## Calibration notes

- CONTINUE = commitment to current evidence and scientific continuity.
- PIVOT = updating toward operational and market signals.
- Expected tension: genuine 50/50 under neutral baseline.
