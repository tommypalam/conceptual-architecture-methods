# Presentation-order dependence in the item pool

**Zero API calls. Offline re-analysis of frozen records from `semantics_r1` and
`probe_fields_r1`, 20 September 2026.** Prompted by
[defeasibility_screen_r1](defeasibility_screen_r1/ASSESSMENT.md), where two twins
that looked balanced (keep-share 0.52) turned out to be choosing whichever option
was printed first, 25/25 in both directions.

## Finding 1: two of the seven base items are strongly order-dependent

Keep-share by presentation order, `semantics_r1` CANON cells (profiled, 40 agents;
order is fixed per agent by `agent % 2`):

| Item | Keep shown first | Override shown first | Gap |
|---|---:|---:|---:|
| **meeting_room** | 0.75 | 0.00 | **0.75** |
| **desk_booking** | 0.80 | 0.07 | **0.73** |
| on_call | 0.25 | 0.55 | 0.30 |
| storage_unit | 0.82 | 0.68 | 0.15 |
| rest_break | 0.57 | 0.42 | 0.15 |
| tool_library | 0.57 | 0.70 | 0.12 |
| weekend_rota | 0.93 | 0.90 | 0.03 |

**This is a property of the published item pool, not of the Stage 3a twins.** The
same two families produced the twin artefacts. It has not been recorded before.
`pd_endpoint_r2` checked order on *different* items and found it irrelevant
(51.3% first-shown); that finding does not transfer and the check lapsed.

## Finding 2: no headline result is affected, and the reason is structural

Every effect in this project is a **paired within-agent contrast** — the same agent,
the same item, the same presentation order, differing only in the pinned value.
Presentation order is held fixed inside each pair, so an order-sensitive item
shifts both arms of the pair equally and the difference is unaffected.

Verified by splitting each headline contrast by order:

| Contrast | Keep shown first | Override shown first | Published |
|---|---:|---:|---:|
| PD (semantics_r1 CANON) | +0.357 | +0.321 | +0.3393 |
| Status-quo Preference | +0.421 | +0.379 | +0.4000 |
| Stated-Wish Deference | +0.293 | +0.321 | +0.3071 |
| Numbers Count | −0.293 | −0.200 | −0.2464 |
| Worst-off Priority | −0.179 | **+0.050** | −0.0643 |

Every effect keeps its sign and magnitude within each order, including Numbers
Count's reversal. **Worst-off Priority is the exception and splits across orders**,
which is further reason to claim nothing for it beyond the failed prediction
already recorded.

**No published figure changes and nothing is withdrawn.**

## Finding 3: unpaired screens are where this bites

A dispersion screen is *unpaired*: it counts votes across independent calls with
order alternating. A perfectly order-determined item then averages to a pooled
share near 0.50 and passes a band rule designed to detect exactly the opposite
condition. That is how `defeasibility_screen_r1` returned `screen_pass` on two
items that were making no choice at all.

## Standing rules adopted

1. **Every dispersion screen must report keep-share by presentation order** and
   treat an order gap above 0.20 as unusable, regardless of the pooled share.
1b. **Every forced choice put to a model must be presented in BOTH orders**,
   whether the model is acting as an agent or judging as a rater. Randomising
   order per trial makes a position-following responder *visible* but does not
   *neutralise* it; showing each item both ways makes a content-free responder
   score chance by construction. Learned the hard way in
   [inverse_inference_r1](inverse_inference_r1/ASSESSMENT.md), where the model
   answered "B" in 94 of 120 trials and scored 0/19 in one condition when the
   answer was A.
   Implemented in the next screen designation, not retro-fitted to frozen
   collectors.
1c. **Presentation order must be CROSSED with any covariate, not left to
   correlate with agent index.** In `precipitation_r2` the agent index set the
   order and also, through the frozen transcripts, the exemplar keep-count: 14 of
   16 keep-leaning agents fell in one order. The pre-registered dose-response then
   read order rather than exemplars, and was void by its own criterion - the arm
   whose text is identical for every agent showed the slope. **Third occurrence of
   this defect in one phase**: base items, then a judge prompt, now a covariate.
2. **Order-robustness is a property of an item**, established per item and never
   inherited from another item set.
3. Paired within-agent designs remain the right instrument: they are immune to
   this by construction, which is why the headline results survive a defect that
   destroyed a screen.

## What this does not establish

That the two order-dependent items are defective for paired use — they are not,
and they are retained. That any prior result is wrong — none is. That the pool is
otherwise sound: this check covers order only.
