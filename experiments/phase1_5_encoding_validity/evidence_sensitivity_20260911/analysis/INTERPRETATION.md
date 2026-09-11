# Local response survives; wording robustness remains unresolved

Completed 540/540 valid responses, with no terminal API/model/usage failures.
Model `gpt-5.4-mini-2026-03-17`, neutral context, root seed 20260916, temperature
1, 600-token cap; 30 single-decision calls per cell. All other nine parameter
values are held at their original source means within each probe.

Recorded full-rate token estimate: **$0.650970** for this diagnostic,
**$1.1531925 cumulatively** across the two newly funded screens. Approximately
**$7.8468075 remains of the $9 allowance**, not a checked provider-account
balance. No automatic expansion is scheduled.

## Primary: grounding still supports a local MoR response

| Arm | MoR=.1 ADOPT | MoR=.9 ADOPT | Difference | Conservative >=95% interval |
|---|---:|---:|---:|---|
| Original | 8/30 (26.7%) | 26/30 (86.7%) | +.600 | [.183, .861] |
| Repetition alone | 1/30 (3.3%) | 3/30 (10.0%) | +.067 | [-.178, .290] |
| Repetition + grounding | 3/30 (10.0%) | 23/30 (76.7%) | +.667 | [.261, .897] |

The grounding result follows MoR/S3's existing positive direction and its
interval excludes zero. The prespecified status is
**POSITIVE_RESPONSE_DETECTED_NOT_VALIDATED**. This answers one concrete concern:
grounding does not make every tested profile produce the same decision. At
these canonical MoR endpoints, a large behavioural contrast remains observable.

It does not establish preserved continuous gradients, retained slope magnitude,
or superiority over repetition. Significance in one arm and non-significance
in another is not a test of their difference. The original control also shows
a positive endpoint contrast. Repetition's observed rates and interval warrant
caution about using repetition alone as a repair, without proving zero response.

These MoR cells use PD's population mean, not PD=.8. Their response cannot be
transported to every joint profile or to all ten parameters.

## PD: the gap is not uniformly small across tested values

| Arm | P2 at PD=.1 | P3 at PD=.1 | P2 at PD=.9 | P3 at PD=.9 |
|---|---:|---:|---:|---:|
| Original | 23/30 | 29/30 | 27/30 | 6/30 |
| Repetition alone | 4/30 | 7/30 | 7/30 | 1/30 |
| Repetition + grounding | 27/30 | 14/30 | 7/30 | 9/30 |

With grounding, the low-PD P2-minus-P3 gap is **+.433**, conservative nominal
>=95% interval **[.030, .722]**. At high PD it is **-.067**, interval
**[-.433, .317]**. These are secondary, non-family-adjusted contrasts. The low
endpoint has a large observed discrepancy; the high endpoint is imprecise.
Neither establishes +/- .10 equivalence. The previous zero observed gap at
PD=.8 was a separate screen, not proof of a uniformly robust response curve.

Grounding P2 changes by -.667 between PD endpoints, interval [-.897, -.261];
P3 changes by -.167, interval [-.548, .258]. PD/S3 has no prespecified direction:
these observations are descriptive and do not validate a normative action
mapping. P3's interval does not prove absence of sensitivity.

## Consequences for the next step and thesis claims

This is a mixed but informative result: local parameter response is possible
under the candidate, while wording robustness remains unresolved. It is not
evidence of a fundamental limit on ethical encoding, and the data do not yet
justify calling the observed residual a hard cap. No gate or margin changes.

The next useful small diagnostic is the missing intermediate values (.3, .5,
.7), keeping the same existing meanings and explicit controls, to distinguish
a gradual response from threshold behaviour and to locate wording dependence.
Do not mix the previously collected endpoints into a new confirmatory sample;
any combined curve is exploratory and must disclose the stages and candidate
selection. Confirmation would freeze a complete selected condition and use
fresh data. It also needs appropriate headroom and parameter-responsiveness
criteria, not just agreement caused by near-fixed decisions.

If the eventually tested routes still fail, report the practical limitation of
this model, delivery, wording set and task coverage, with uncertainty and the
unsolved gate intact. That can be a defensible thesis finding without claiming
the theory is impossible or retrospectively redefining success.

Original prompts, source records and theory remain unchanged. The optional
tool is inactive. Phase 1.5 remains open; Phase 2 remains on hold.
