"""Swap controls for TfA and MoR: are their effects bound to their fields?

`parameter_followup_r2` established that both move the outcome at 80 agents:
TfA -0.1107 [-0.1536, -0.0661] and MoR -0.0732 [-0.1161, -0.0304], where the
sweep at 25 agents had left both just outside Holm correction. They are
load-bearing *coordinates*, not demonstrated *field* effects. They sit exactly
where PD sat after `coordinate_sweep_r2` and before `label_semantics_r1`.

**The construction**, taken unchanged from `phase5_label_semantics_multi`. For an
active coordinate A, the partner field AW, and a level L in {0.1, 0.9}:

    TRUE(L)   L on A's entry,              the drawn AW value on AW's entry
    SWAP(L)   the drawn AW value on A,     L on AW's entry

Both arms carry the multiset {L, drawn-AW} across those two entries, so the
blocks are **numeral-identical**: same length, same line count, same ten numbers,
same field order. Only which entry holds L differs.

**AW is a better-evidenced partner than it was.** When the earlier swap controls
ran, AW's inertness rested on a post-hoc correlation and a by-product measurement
of -0.036. `parameter_followup_r1` has since pinned AW in its own right at 80
agents: **+0.016 [-0.027, +0.057], 90% equivalence bound 0.050** - the tightest
bound in the project. And `probe_fields_r1` showed AW's slot is not a dead slot:
an invented field placed there reached +0.400. The slot can carry an effect; AW's
own gloss does not produce one, which is the right shape for a partner.

**Predictions, locked before collection.**

  - **TRUE gates each coordinate separately.** It must reproduce
    `parameter_followup_r2`: TfA near -0.111, MoR near -0.073, both NEGATIVE.
    If a TRUE arm fails, that coordinate's SWAP contrast is uninterpretable and
    nothing is claimed for it - the LL lesson, where a null SWAP beside an
    unreplicated TRUE would have read as "the field carries it".
  - **SWAP is the test and is NOT predicted directionally.**
  - **The primary quantity is the within-unit difference TRUE - SWAP** with a
    95% unit-bootstrap interval, not one arm clearing a threshold while the other
    does not. That inference was made once about ID and withdrawn (Gelman and
    Stern); the direct difference of differences is what settled PD at +0.375
    [+0.286, +0.464] and left ID at +0.064 [-0.014, +0.146].

**A power caution recorded in advance, not after the result.** PD's effect was
+0.339 when its swap control ran. TfA (-0.111) and MoR (-0.073) are 3x and 4.6x
smaller. Simulated at the measured per-item baselines, Holm family 4, 80 agents:
0.111 is detected 18/20, 0.100 17/20, but **0.075 only 8/20 and 0.050 7/20**.
TfA is adequately powered. **MoR is NOT**: at its measured size this design finds
it in fewer than half of simulated runs, so a MoR TRUE arm that fails its gate is
as likely to be a power failure as a real non-replication, and nothing will be
concluded from it either way. MoR is carried because dropping it after r2 would
be selection, not because this design can settle it.

**Item consistency differs between them and is carried forward.**
`parameter_followup_r2` found MoR uniform (6 of 7 items negative, range -0.125 to
0.000) and TfA item-dependent (+0.175 on `desk_booking` against -0.312 on
`on_call`), so TfA's pooled figure is a partial cancellation. Per-item effects
are reported for both arms of both coordinates.

**Both coordinates run in one designation** so the Holm family covers all four
contrasts together rather than treating each coordinate as its own lucky draw.
"""
from __future__ import annotations

import hashlib
import json

import phase7_block_variants as BV

PARAMETERS = BV.PARAMETERS
ACTIVE = ("TfA", "MoR")
PARTNER = "AW"
LOW, HIGH = 0.1, 0.9
ARMS = tuple(f"{a}:{arm}{s}" for a in ACTIVE for arm in ("TRUE", "SWAP")
             for s in ("+", "-"))

PRIOR = {
    "TfA": {"effect": -0.1107, "ci95": [-0.1536, -0.0661],
            "items": "2+/4-", "source": "parameter_followup_r2",
            "note": "item-dependent: +0.175 on desk_booking against -0.312 on on_call"},
    "MoR": {"effect": -0.0732, "ci95": [-0.1161, -0.0304],
            "items": "0+/6-", "source": "parameter_followup_r2",
            "note": "uniform across items, range -0.125 to 0.000"},
}
PARTNER_EVIDENCE = {
    "pinned_directly": {"effect": +0.0161, "ci95": [-0.0268, +0.0572],
                        "equivalence_bound_90": 0.050, "agents": 80,
                        "source": "parameter_followup_r1"},
    "slot_can_carry_an_effect": {"effect": +0.4000, "field": "Status-quo Preference",
                                 "source": "probe_fields_r1"},
}


def true_profile(coordinates, active, level):
    """Level on the active coordinate; the partner keeps its drawn value."""
    if active not in ACTIVE:
        raise ValueError(f"Not an active coordinate: {active}")
    if set(coordinates) != set(PARAMETERS):
        raise ValueError("Require exactly the ten parameter codes")
    out = dict(coordinates)
    out[active] = level
    return out


def swap_profile(coordinates, active, level):
    """The same two numerals, exchanged between the active field and the partner."""
    out = true_profile(coordinates, active, level)
    out[active] = coordinates[PARTNER]
    out[PARTNER] = level
    return out


def block_equivalence(render_block, coordinates, active, level):
    """TRUE and SWAP must be numeral-identical and differ on exactly two lines."""
    import re
    t = render_block(true_profile(coordinates, active, level))
    s = render_block(swap_profile(coordinates, active, level))
    a, b = t.split("\n"), s.split("\n")
    diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    numerals = lambda text: sorted(re.findall(r"\d+\.\d+", text))
    return {"matched": (len(a) == len(b) and len(t) == len(s)
                        and numerals(t) == numerals(s) and len(diff) == 2),
            "lines_differing": len(diff), "same_length": len(t) == len(s),
            "same_numeral_multiset": numerals(t) == numerals(s)}


def verify_construction(render_block, agents):
    """Every property the design rests on, for every agent, against the renderer."""
    problems = []
    for agent in agents:
        c = agent["coordinates"]
        for active in ACTIVE:
            for level in (LOW, HIGH):
                eq = block_equivalence(render_block, c, active, level)
                if not eq["matched"]:
                    problems.append(f"agent {agent['agent']} {active} L={level}: {eq}")
            # Degeneracy at RENDERED precision: if the drawn partner value prints as
            # a level, TRUE and SWAP collapse and the contrast is silently diluted.
            if f"{c[PARTNER]:.2f}" in (f"{LOW:.2f}", f"{HIGH:.2f}"):
                problems.append(f"agent {agent['agent']}: drawn {PARTNER} renders as a level")
            if f"{c[active]:.2f}" in (f"{LOW:.2f}", f"{HIGH:.2f}"):
                problems.append(f"agent {agent['agent']}: drawn {active} renders as a level")
            blocks = {arm: render_block(fn(c, active, lv))
                      for arm, fn in (("TRUE", true_profile), ("SWAP", swap_profile))
                      for lv in (LOW, HIGH)}
            if len(set(blocks.values())) != len(blocks):
                problems.append(f"agent {agent['agent']} {active}: arms are not distinct")
    if problems:
        raise ValueError("Construction verification failed: " + "; ".join(problems[:6]))
    return {"verified": True, "agents": len(agents), "arms": list(ARMS),
            "note": ("For every agent and level, TRUE and SWAP are numeral-identical, "
                     "equal in length and differ on exactly two lines. No drawn value "
                     "collides with a level at rendered precision.")}


LOCKED_PREDICTION = {
    "question": ("Are the TfA and MoR effects bound to their own fields, or does the "
                 "model respond to an extreme numeral wherever it sits?"),
    "active": list(ACTIVE), "partner": PARTNER, "levels": [LOW, HIGH],
    "prior": PRIOR, "partner_evidence": PARTNER_EVIDENCE,
    "effect_definition": ("paired difference in the share classifying `good`, printed "
                          "0.90 minus printed 0.10, by agent and item"),
    "gate": ("Each coordinate's TRUE arm must reproduce parameter_followup_r2 in SIGN "
             "and clear Holm over the four contrasts. A coordinate whose TRUE arm fails "
             "has an uninterpretable SWAP contrast and nothing is claimed for it."),
    "swap_not_predicted": ("SWAP carries no directional prediction. Near zero suggests "
                           "the field carries the effect; comparable to TRUE suggests "
                           "numeric extremity anywhere in the block."),
    "primary": ("the within-unit difference TRUE - SWAP per coordinate, with a 95% "
                "unit-bootstrap interval. NOT significance-versus-non-significance, "
                "the inference withdrawn over ID."),
    "power": {"agents": 80, "family": 4,
              "detected_at_0.111": "18/20", "detected_at_0.100": "17/20",
              "detected_at_0.075": "8/20", "detected_at_0.050": "7/20",
              "false_positives": "1/20",
              "caution": ("MoR (-0.073) is UNDERPOWERED here - 8/20 at its measured "
                          "size. Nothing is concluded from a MoR gate failure. TfA "
                          "(-0.111) is adequately powered at 18/20.")},
    "not_established_by_any_outcome": [
        "understanding, or that either coordinate is understood as a concept",
        "that the field's STATED MEANING carries it - that needs the gloss-reversal "
        "design of semantics_r1, which this designation does not run",
        "anything beyond gpt-5.4-mini and these seven items",
        "that the ten parameters are privileged: probe_fields_r1 found an invented "
        "field moving these items more than either coordinate here",
    ],
    "no_reroll": "No arm is re-run with more agents after the results are seen.",
}


def content_hash():
    payload = json.dumps({"active": ACTIVE, "partner": PARTNER, "levels": [LOW, HIGH],
                          "prediction": LOCKED_PREDICTION},
                         sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
