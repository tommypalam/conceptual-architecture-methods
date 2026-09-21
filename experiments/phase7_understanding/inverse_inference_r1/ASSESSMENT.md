# inverse_inference_r1 — assessment

**Complete but UNINFORMATIVE. The instrument failed, not the hypothesis.**
120 calls, 120/120 valid, zero failures, $0.084606. `gpt-5.4-mini-2026-03-17`,
21 September 2026. Protocol: [PROTOCOL.md](PROTOCOL.md). Design hash
`01dbadd6…538abe6e`.

The recorded decision is `no_inference`. **That reading should not be used.** The
analysis measured accuracy, and accuracy here is dominated by a positional bias
the design did not control.

## What was recorded

| Condition | Correct | Accuracy | 95% CI | vs chance |
|---|---:|---:|---|---|
| GLOSSED | 18/40 | 0.450 | [0.30, 0.60] | not above |
| NAMED | 16/40 | 0.400 | [0.25, 0.55] | not above |
| **BLIND** | **11/40** | **0.275** | [0.15, 0.43] | **below**, p = 0.0032 |

GLOSSED − BLIND = +0.175 [0.000, +0.350], not excluding zero.

A below-chance result on a two-alternative forced choice is the first sign that
something is wrong with the instrument rather than with the model.

## The diagnosis: the model answered "B" almost regardless

| Condition | Chose A | Chose B |
|---|---:|---:|
| BLIND | 12 | **28** |
| NAMED | 5 | **35** |
| GLOSSED | 9 | **31** |

Split by what the correct answer was:

| Condition | Correct when answer = A | Correct when answer = B |
|---|---:|---:|
| BLIND | **1/19 = 0.053** | 10/21 = 0.476 |
| NAMED | **0/19 = 0.000** | 16/21 = 0.762 |
| GLOSSED | **3/19 = 0.158** | 15/21 = 0.714 |

**In NAMED the model was right 0 times out of 19 when the answer was A.** No
account on which the model is reading the transcripts produces that. It is
answering by position. Accuracy then tracks only how the answer key happened to
fall — the key was 19 A / 21 B, so a pure "always B" responder scores 21/40 =
0.525, and the three conditions scatter around that according to how completely
the bias took hold. BLIND's 0.275 is that bias plus noise, not inverted knowledge.

**Every quantity in the results file inherits this.** The condition comparison,
the paired differences and the `no_inference` decision are all functions of
accuracy, and accuracy is not measuring inference. Nothing about bidirectionality
is established in either direction.

## Why the design let this through, stated plainly

The project has an explicit rule about presentation order, adopted in this phase:
[ORDER_DEPENDENCE.md](../ORDER_DEPENDENCE.md) requires screens to report results
by presentation order because two items in the pool turned out to be
order-determined, and an earlier screen passed two candidates that were doing
nothing but following position.

**I applied that rule to the participant items and not to this judge design.** The
A/B order was randomised per trial — which is why the bias is visible at all — but
randomising the order does not detect a responder that ignores content. Detecting
that needs each trial presented in **both** orders, so that a content-free
responder scores 0.50 by construction and a content-sensitive one does not. That
is a 240-call design, not 120, and it is the design this should have been.

The gate checked many things: that BLIND names nothing, that NAMED is name-only,
that no prompt leaks "PD" or the pinned values, that the key is not degenerate.
**It did not check the one failure mode the phase had already documented.**

## What this costs, and what it does not

**The marker is untested.** Bidirectionality is neither demonstrated nor refuted.
The hypothesis is untouched: nothing here bears on whether the model can recover a
field from behaviour, because nothing here measured that.

**The materials are undamaged.** The `pd_prospective_r1` transcripts are frozen
and unaltered; they cost nothing to reuse. A corrected design — each pair shown in
both orders, 240 calls, about $0.18 — remains available and would be a new
designation with its own release.

**No other result is affected.** This designation touched no other study, and its
120 records are preserved as collected.

**The rule now generalises.** Presentation-order control applies to *any* forced
choice this project puts to a model, whether the model is acting as an agent or
judging as a rater. It is not a property of the participant item pool. That is the
lesson, and it cost $0.08 to learn twice.

## What no reading of this establishes

That the model cannot recover a field from behaviour. That it can. That
transcript statistics suffice. Anything about PD, understanding, or any marker of
the programme.

## Accounting

OpenAI $21.277892 → **$21.344140**/$40 (the reservation was $0.487; settlement
$0.0846, the remainder released). Anthropic unchanged $22.268707/$32.
Package ≈ $43.613/$100. Usage estimates, not verified provider balances.
