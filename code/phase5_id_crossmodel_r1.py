"""Collector for id_crossmodel_r1: does ID's effect exist outside gpt?

Design, locked prediction and measured power live in `phase5_id_crossmodel`.
This module dispatches it.

**Two arms, one coordinate, one model.** ID pinned to 0.1 and 0.9 with the nine
other coordinates drawn once per agent and held identical, on
`claude-haiku-4-5-20251001`, over haiku's six dispersing items.

**The item pool is `phase4b_profiled_pool`, not `phase4b_perm_pool`.** Those are
different item sets: `ward_transfer` is haiku-only and `on_call`/`rest_break` are
gpt-only. Four of six overlap. Using gpt's pool here would dispatch items that
`haiku_screen_r4` measured at modal share 1.00 on this model, which cannot show
an arm difference. The assessment reports this as ID tested on haiku's items,
not as a byte-identical repetition of the gpt designation.

**No screen arm.** These six items were screened on haiku in
`phase4b_profiled_r1` (modal shares 0.52-0.96, all usable) and the profiled arm
ran there. Re-screening would confirm rather than establish. The review call is
kept and is ADVISORY: the items are byte-identical to material
`phase4b_profiled_r1` reviewed and accepted, which is the 16 September amendment's
condition exactly.

**Power is marginal and was measured against haiku's own baselines before any
call**: 16/20 at ID's gpt effect of +0.111, 1/20 false positive at zero. A null
from this designation is a weak null and says so.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase3_budget import BudgetStop, digest, read_checked, token_cost_nano
from phase3_design_pilot import request, JUDGE, PRICES
from phase3_protocol_kernel import context_prompt, AXES
from phase3_recognition_recovery import verify, sha
from phase3_recognition_run import ROOT, LEDGER, Ledger, network, charge, MODELS
from phase4_crossmodel_dispatch_v2 import dispatch as crossmodel_dispatch
from phase4_choice_extraction_v2 import CONTRACT_VERSION
from phase3_representation_diagnostic import profile_parts
from phase3_variant_round import save

import phase4b_tasks_r2 as _POOL
import phase4b_profiled_pool as P
import phase5_pd_prospective as PD
import phase5_label_semantics as LS
import phase5_coordinate_sweep as SW
import phase5_id_crossmodel as IDX
import phase4b_permutation as PERM  # retained: the release pins it

FOLDER = ROOT / "experiments/phase5_analysis/id_crossmodel_r1"
PARENT = ROOT / "experiments/phase5_analysis/label_semantics_r2"
STUDY = "id_crossmodel_r1"

HAIKU = "claude-haiku-4-5-20251001"
GPT = "gpt-5.4-mini-2026-03-17"
SONNET = "claude-sonnet-4-6"
SCREEN_MODELS = ()
# The POINT of this designation: a model that is not the calibration model.
MODEL = HAIKU

# phase4b_screen_r2's one lost probe, preserved at full reservation. Named so a
# NEW failure still stops the run. Not retried and not recovered.
# Two inherited failures, both preserved at full reservation and neither retried:
# screen_r2's unreadable double-object reply, and sonnet_r1's reply truncated
# mid-JSON at 768 tokens.
INHERITED_REVIEW = "phase4b_gpt_r1/review/0"   # read, never re-dispatched

# coordinate_sweep_r1 halted at 689/2800 on a network TimeoutError - no response
# was received, so nothing was measured. The failure is preserved at full
# reservation and is NOT retried: that slot stays unresolved forever. r2 names it
# so a NEW unresolved dispatch still stops the run.
INHERITED_TIMEOUT = "coordinate_sweep_r1/profiled/CS_lo/6/tool_library"
INHERITED_FAILURE = "phase4b_screen_r2/screen/tool_library/5"
INHERITED_FAILURE_2 = "phase4b_sonnet_r1/profiled/E/17/ward_transfer"
ARMS = ("ID-", "ID+")
# 40 agents over six items in two arms. Power simulated against haiku's MEASURED
# per-item baselines from phase4b_profiled_r1 (NOT a uniform effect - that is the
# error made for phase4b_sonnet_r1, which reported 8/8 when the true figure was
# <=5/10 and was abandoned on the corrected analysis). 20 seeds, Holm family of 1:
#   +0.080 -> 14/20   +0.111 -> 16/20   +0.143 -> 18/20   +0.200 -> 19/20
#   0.000  ->  1/20 false positive
# 16/20 at ID's gpt effect is 80%. A null here is a WEAK null and is reported with
# that number. Two of six items sit near a bound in one arm (tool_library 0.90 in
# E, storage_unit 0.04 in U), which compresses the detectable range; more agents
# does not fix that, which is why 60 was not chosen instead.
N_AGENTS = 40
# No screen arm: these six items were screened on haiku in phase4b_profiled_r1
# (modal shares 0.52-0.96, all usable) and the profiled arm ran on them there.
SCREEN_N = 0
SATURATED_AT = 1.0
MIN_USABLE = 0   # no screen arm; the items are inherited as screened on haiku
SEEDS = {"population": 2026091801, "schedule": 2026091802, "analysis": 2026091803}
NEUTRAL = dict.fromkeys(AXES, "NEUTRAL")

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")


# 481 calls: one review + 40 agents x 2 arms x 6 items. All on haiku.
# The reservation is computed from the ACTUAL job list, summing each item's own
# byte bound - not from one item's length. That shortcut under-estimated by ~20%
# twice before and is not repeated: the figure below is what prepare() computes.
# Real reservation: $6.432751. Anthropic headroom at designation time is
# $32.00 - $19.728 = $12.271, so the worst case fits with room to spare.
# Prior runs settle near 17% of reservation, so the realistic figure is ~$1.10.
CAP = 12_000_000_000
PROVIDER_CAPS = {"anthropic": 32_000_000_000, "openai": 40_000_000_000}
# ADVISORY, under the 16 September constitution amendment. These six items are
# byte-identical to the material phase4b_profiled_r1 reviewed and ACCEPTED with
# zero blocking issues before collecting 631 decisions on them, on this same
# model. The amendment's condition is met exactly: a designation reusing already
# accepted materials records the review's findings and a reject does not stop
# collection. This designation introduces NO new item text - only a different
# pinned coordinate, which is not participant-visible material.
#
# Re-running a review to obtain a different verdict remains forbidden and is not
# done here: one review is dispatched and whatever it returns is recorded.
REVIEW_ADVISORY = True

# Beta parameters from CLAUDE.md, used only to draw the nine non-PD coordinates.
BETA = {"LL": (3.5, 2.5), "CS": (2.5, 2.0), "RT": (2.5, 2.5), "MoR": (2.0, 2.5),
        "RE": (2.0, 3.0), "PD": (2.5, 2.0), "TfA": (2.0, 3.5), "ID": (3.0, 2.0),
        "MS": (1.8, 1.5), "AW": (2.2, 2.5)}


def population():
    """One draw per agent; ID is overwritten per arm, everything else is shared.

    Independent Beta marginals, not the Gaussian copula: this designation tests a
    single coordinate's effect, and the copula's dependence structure would
    introduce correlated variation in the nine held-constant coordinates without
    serving that question. The nine are identical between ID- and ID+ for a given
    agent either way, so the contrast is unaffected.
    """
    import numpy as np
    rng = np.random.default_rng(SEEDS["population"])
    agents = []
    for i in range(N_AGENTS):
        draw = {k: float(round(rng.beta(a, b), 3)) for k, (a, b) in BETA.items()}
        agents.append({"agent": i, "coordinates": draw})
    return {"n_agents": N_AGENTS, "agents": agents, "seed": SEEDS["population"],
            "note": ("Independent Beta marginals. ID is overwritten per arm; the "
                     "other nine coordinates are identical across arms per agent.")}


NL_SEP = chr(10) + chr(10)

# Inherited VERBATIM from phase4_capstone_model2.GUIDANCE so the G arm here is
# the same instrument moral_capstone_r3 used. Asserted identical at import time
# by the check in leakage_gate().
GUIDANCE = (
    "# Ethical guidance" + NL_SEP +
    "Weigh the interests of everyone affected. Avoid causing harm, avoid "
    "deceiving anyone, avoid coercing anyone, and treat people with equivalent "
    "claims equally. Where these cannot all be satisfied, decide which matters "
    "most in this situation and act on it." + NL_SEP
)


# Rendering modes, distinct from ARMS. ARMS names this designation's experimental
# arms (LL-, LL+, CS-, ...); RENDER_MODES names how a prompt is built. Every arm
# here renders with "E" - a full numeric profile - and differs only in which
# coordinate is pinned.
RENDER_MODES = ("U", "E", "G")


def system(profile=None, arm="E"):
    """System prompt in one rendering mode.

    U  no profile
    E  full numeric profile
    G  no profile, plus explicit ethical guidance

    This designation uses E throughout: every dispatched call carries a full
    profile, and the arms differ only in which coordinate is pinned.
    """
    if arm not in RENDER_MODES:
        raise ValueError(f"Unknown rendering mode: {arm}")
    base = dict.fromkeys(PARAMETERS, 0.5) if profile is None else dict(profile)
    original = context_prompt(base, NEUTRAL)
    prefix, block, suffix = profile_parts(original)
    suffix = suffix[:suffix.index("# Your task")] + (
        "# Your task" + chr(10)
        + "Use the supplied information to make the requested decision. "
        + "Do not infer a demographic identity or additional facts. "
        + "Return only the requested JSON object." + chr(10))
    selected = block if arm == "E" else (GUIDANCE if arm == "G" else "")
    return prefix + selected + suffix


def body(task_id, first):
    spec = P.task(task_id)
    ids = list(P.action_ids(task_id))
    if not first:
        ids.reverse()
    lines = [f"Option {a.upper()}: {spec['actions'][a]['description']} "
             f"{spec['actions'][a]['effect_text']}" for a in ids]
    instruction = 'Return JSON only: {"choice":"<OPTION NAME>"}.'
    sep = chr(10) + chr(10)
    return sep.join((P.COMMON_FRAMING, spec["situation"],
                     "# Options" + chr(10) + chr(10).join(lines), instruction))


# phase4b_sonnet_r1 halted on a reply truncated mid-JSON at 768 tokens, a budget
# inherited from the haiku design. The lesson generalises: a model that reasons
# before answering needs room to finish. 1536 is carried here.
OUTPUT_BUDGET = 1536


def make_job(model, slot, stage, text, maximum=OUTPUT_BUDGET, system_text=None):
    system_text = system() if system_text is None else system_text
    bound = len((system_text + text).encode("utf-8")) + 1024
    req = request(model, system_text, text, maximum, temperature=1)
    if MODELS[model] == "openai":
        req["response_format"] = {"type": "json_object"}
    return {"slot": f"{STUDY}/{slot}", "kind": "probe", "stage": stage, "request": req,
            "input_token_bound": bound,
            "reserved_nano": token_cost_nano(bound, maximum, *PRICES[model])}


def arm_tag(model):
    return "gpt" if "gpt" in model else model.split("-")[1]


def screen_jobs():
    """Unprofiled probes: every item on every model.

    Three models rather than one. The twelve items are identical across them, so
    the same batch answers two questions at once: which items disperse (the
    Phase 4B prerequisite), and whether dispersion is a property of the item or
    of the model (the cross-model question every prior designation was blocked
    from reaching).
    """
    batch = []
    for model in SCREEN_MODELS:
        tag = arm_tag(model)
        for task_id in P.TASK_IDS:
            for i in range(SCREEN_N):
                job = make_job(model, f"screen/{tag}/{task_id}/{i}", "screen",
                               body(task_id, i % 2 == 0))
                job["valid_actions"] = sorted(a.lower() for a in P.action_ids(task_id))
                job["cell"] = {"arm": "U", "model": tag, "task": task_id,
                               "agent": None, "index": i}
                batch.append(job)
    return batch


def profiled_jobs(pop):
    """Two arms, paired within agent and item.

    ID- pins ID to 0.1, ID+ pins it to 0.9, and the nine other coordinates are
    drawn once per agent and held identical between them. The system prompts
    differ by exactly one line; the user text is byte-identical.
    """
    batch = []
    for agent in pop["agents"]:
        coords = agent["coordinates"]
        for arm, level in (("ID-", IDX.LOW), ("ID+", IDX.HIGH)):
            system_text = system(IDX.pin(coords, level), "E")
            tag = "ID_lo" if level == IDX.LOW else "ID_hi"
            for task_id in P.TASK_IDS:
                job = make_job(MODEL, f"profiled/{tag}/{agent['agent']}/{task_id}",
                               "profiled", body(task_id, agent["agent"] % 2 == 0),
                               system_text=system_text)
                job["valid_actions"] = sorted(a.lower() for a in P.action_ids(task_id))
                job["cell"] = {"arm": arm, "coordinate": IDX.ACTIVE,
                               "task": task_id, "agent": agent["agent"],
                               "index": None}
                batch.append(job)
    return batch


def review_packet():
    """Participant text and kind only, under neutral keys."""
    return {"items": {f"item_{i:02d}": {"item": P.participant_text(t), "kind": "conflict"}
                      for i, t in enumerate(P.TASK_IDS)},
            "design_note": ("Every item offers two options and each option sets aside a "
                            "different stipulated expectation. There is no option that "
                            "sets aside nothing; that is intended.")}


def review_job():
    return _review_job()


def _review_job():
    job = make_job(JUDGE, "review/0", "review",
                   json.dumps(review_packet(), ensure_ascii=False, sort_keys=True),
                   1024, (
        "Review these decision items independently. Stipulated consequences are an "
        "intended and necessary part of every item; their presence is not a defect. "
        "Every item is a CONFLICT item in which BOTH options set aside something a "
        "reasonable person could hold binding - there is deliberately no option that "
        "sets aside nothing, and that is the design, not a defect. Judge whether each "
        "item is answerable and non-leading. Flag an item only if it states which "
        "option the decision-maker ought to choose beyond the stipulated facts, if one "
        "option's DESCRIPTION or CONSEQUENCE TEXT labels it with a norm violation that "
        "its paired option does not carry, if the two options are unequally "
        "characterised in weight or wording, if it names a psychological construct or "
        "reveals a study hypothesis, or if its stipulated quantities are internally "
        "contradictory. Do not accept merely because the design could show an effect. "
        "Return only JSON with an overall verdict accept/revise/reject, a "
        "blocking_issues list and a limits list. Under 150 words."))
    job["raw_text"] = True
    assert not job.get("valid_actions"), "Review job must not declare valid_actions"
    return job


def _json_objects(text):
    spans, depth, start, in_str, esc = [], 0, None, False, False
    for i, ch in enumerate(text or ""):
        if in_str:
            if esc:
                esc = False
            elif ch == chr(92):
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0:
                spans.append(text[start:i + 1])
    return spans


def _shape(value):
    if not isinstance(value, dict) or not value:
        return None
    key = next((k for k in ("verdict", "overall_verdict", "overall") if k in value), None)
    if key:
        return {"verdict": str(value[key]).strip().lower(), "verdict_key": key,
                "blocking_issues": list(value.get("blocking_issues") or []),
                "limits": list(value.get("limits") or [])}
    if all(isinstance(v, dict) and ("verdict" in v or "overall_verdict" in v)
           for v in value.values()):
        verdicts = {k: str(v.get("verdict", v.get("overall_verdict"))).strip().lower()
                    for k, v in value.items()}
        overall = "accept" if all(x == "accept" for x in verdicts.values()) else "revise"
        return {"verdict": overall, "per_item": verdicts,
                "blocking_issues": [f"{k}: {i}" for k, v in value.items()
                                    for i in (v.get("blocking_issues") or [])],
                "limits": []}
    return None


def read_review(text):
    if isinstance(text, dict):
        shaped = _shape(text)
        if shaped:
            return shaped
        raise ValueError("No verdict in review response")
    for span in _json_objects(text):
        try:
            value = json.loads(span)
        except ValueError:
            continue
        shaped = _shape(value)
        if shaped is not None:
            return shaped
    raise ValueError("No verdict in review response")


def _inherited_review_text():
    """r1's recorded review response, read from the ledger. No API call.

    The verdict stands exactly as returned, `revise` included. This function
    exists so r2 cannot accidentally re-roll it.
    """
    record = read_checked(LEDGER / "records" / (digest(INHERITED_REVIEW) + ".json"))
    if record.get("error"):
        raise BudgetStop("Inherited review did not complete")
    return record["parsed"]


def leakage_gate():
    """Every gate that must pass before a single call is built.

    Rewritten whole for this designation: the inherited version had accumulated
    three duplicated blocks from successive lineage edits, each running a
    different designation's arm check.
    """
    symmetry = P.verify_items()
    leaks = {t: P.audit_leakage(t) for t in P.TASK_IDS if P.audit_leakage(t)}
    if leaks:
        raise BudgetStop("Task text leaks: " + str(leaks))

    if N_AGENTS == 0:
        raise BudgetStop("Profiled designation must draw agents")
    if SCREEN_N != 0:
        raise BudgetStop("This designation drops the screen arm; SCREEN_N must be 0")

    # Each coordinate's two arms must differ in that coordinate and nothing else.
    agents = population()["agents"]
    construction = SW.verify_sweep(agents)
    coords = agents[0]["coordinates"]
    import difflib as _dl
    for coordinate in SW.SWEPT:
        lo_sys = system(SW.pin(coords, coordinate, SW.LOW), "E")
        hi_sys = system(SW.pin(coords, coordinate, SW.HIGH), "E")
        if lo_sys == hi_sys:
            raise BudgetStop(f"{coordinate}: arms identical")
        if "Procedural Dependence" not in lo_sys:
            raise BudgetStop(f"{coordinate}: arm is missing its profile block")
        if "Ethical guidance" in lo_sys or "Ethical guidance" in hi_sys:
            raise BudgetStop(f"{coordinate}: arm carries guidance text")
        diff = [x for x in _dl.unified_diff(lo_sys.splitlines(), hi_sys.splitlines(),
                                            lineterm="", n=0)
                if x.startswith(("+", "-")) and not x.startswith(("+++", "---"))]
        if len(diff) != 2:
            raise BudgetStop(f"{coordinate}: arms differ on {len(diff)} lines, not 2")

    if set(review_packet()) - {"items", "design_note"}:
        raise BudgetStop("Review packet carries unexpected keys")
    for entry in review_packet()["items"].values():
        if set(entry) != {"item", "kind"}:
            raise BudgetStop("Review packet item carries unexpected fields")

    return {"forbidden_terms_found": 0, "items_verified": symmetry,
            "sweep_verified": construction,
            "locked_prediction": SW.LOCKED_PREDICTION,
            "sweep_sha256": SW.content_hash(),
            "review_packet_clean": True,
            "task_content_sha256": P.content_hash()}


def screen_outcome(rows):
    """Unprofiled dispersion per item, plus the baseline good-rate.

    `good_share` is the share of unprofiled decisions whose deterministic net
    primary classifies `good`. It is the same quantity the profiled arms are
    measured on, so the U arm serves as both the saturation screen and the
    baseline of the 4B primary outcome.
    """
    out = {}
    for task_id in P.TASK_IDS:
        votes = [r["choice"] for r in rows if r["task"] == task_id and r["choice"]]
        if not votes:
            out[task_id] = {"n_valid": 0, "modal_share": None, "usable": False}
            continue
        counts = {v: votes.count(v) for v in set(votes)}
        modal = max(counts.values()) / len(votes)
        clean = P.clean_action(task_id)
        good = sum(1 for v in votes if P.primary_net(task_id, v) == "good")
        out[task_id] = {
            "n_valid": len(votes),
            "modal_share": round(modal, 4),
            "clean_share": round(sum(1 for v in votes if v == clean) / len(votes), 4),
            "good_share": round(good / len(votes), 4),
            "usable": modal < SATURATED_AT,
        }
    return out


def analyse(rows, usable):
    """One paired contrast. No Holm family: there is exactly one primary test.

    The sweep corrected over eight pooled contrasts because it ran eight. This
    designation runs ONE, so the pooled p is reported uncorrected and the
    per-item tests are corrected among themselves. Inventing a family of one
    would be theatre; hiding that per-item tests are multiple would not.
    """
    import math

    def rate(arm, tasks):
        vals = [P.primary_net(r["task"], r["choice"]) == "good"
                for r in rows if r["arm"] == arm and r["task"] in tasks and r["choice"]]
        return (round(sum(vals) / len(vals), 4), len(vals)) if vals else (None, 0)

    def paired(tasks):
        hi_arm, lo_arm = "ID+", "ID-"
        by = {}
        for r in rows:
            if r["arm"] in (hi_arm, lo_arm) and r["task"] in tasks and r["choice"]:
                by.setdefault((r["agent"], r["task"]), {})[r["arm"]] = (
                    P.primary_net(r["task"], r["choice"]) == "good")
        pairs = [(v[lo_arm], v[hi_arm]) for v in by.values() if len(v) == 2]
        if not pairs:
            return None
        hi_only = sum(1 for lo, hi in pairs if hi and not lo)
        lo_only = sum(1 for lo, hi in pairs if lo and not hi)
        n = hi_only + lo_only
        if n == 0:
            p = 1.0
        else:
            k = min(hi_only, lo_only)
            p = min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n))
        return {"coordinate": IDX.ACTIVE, "pairs": len(pairs),
                "good_more_under_high": hi_only, "good_more_under_low": lo_only,
                "discordant": n, "effect": round((hi_only - lo_only) / len(pairs), 4),
                "p": round(p, 8)}

    tasks = list(usable)
    cells = {"all": {arm: dict(zip(("good_rate", "n"), rate(arm, tasks)))
                     for arm in ARMS}}

    pooled = paired(tasks)
    per_item = {tid: paired([tid]) for tid in tasks}

    # Holm among the per-item tests only. The pooled contrast is the primary and
    # stands alone.
    item_p = {tid: v["p"] for tid, v in per_item.items() if v}
    live = sorted(item_p.items(), key=lambda kv: kv[1])
    holm, running = {}, 0.0
    for i, (tid, raw) in enumerate(live):
        running = min(1.0, max(running, raw * (len(live) - i)))
        holm[tid] = round(running, 8)

    effs = [v["effect"] for v in per_item.values() if v]
    pos = sum(1 for e in effs if e > 0)
    neg = sum(1 for e in effs if e < 0)
    consistency = {"items": len(effs), "positive": pos, "negative": neg,
                   "majority": max(pos, neg), "meets_requirement": max(pos, neg) >= 4}

    moved = bool(pooled and pooled["p"] < 0.05 and consistency["meets_requirement"])

    if not pooled:
        reading = "no pairs; nothing measured"
    elif moved:
        same = (pooled["effect"] > 0) == (IDX.GPT_MEASURED["label_semantics_r2_true"] > 0)
        reading = (
            "ID moves the outcome on haiku, SAME sign as gpt. ID's effect is not "
            "specific to the calibration model. This licenses `ID moves the "
            "outcome on haiku too`, NOT `ID is verified cross-model`: "
            "verification on gpt required a null swap control, which this "
            "designation does not run."
            if same else
            "ID moves the outcome on haiku with the OPPOSITE sign to gpt. "
            "Reported as measured, not reframed, exactly as LL's sign reversal "
            "was. A cross-model sign reversal on a manipulated coordinate would "
            "be a stronger version of the LL finding and must not be smoothed.")
    else:
        reading = (
            "ID did NOT move the outcome on haiku under the prespecified rule. "
            "Power was 16/20 at ID's measured gpt effect of +0.111, so this is a "
            "WEAK null at 80% - not evidence that ID is inert on haiku. The "
            "verified coordinate map is `two of ten, on one model`, and the "
            "paper scopes its coordinate claims to gpt. This designation is NOT "
            "re-run with more agents.")

    return {"cells": cells, "pooled": pooled, "per_item": per_item,
            "holm_per_item": holm, "holm_family_size": len(live),
            "consistency": consistency,
            "moved_outcome": moved,
            "reading": reading,
            "gpt_reference": IDX.GPT_MEASURED,
            "architecture_crossmodel": IDX.ARCHITECTURE_CROSSMODEL,
            "item_overlap_with_gpt": {
                "haiku_items": list(P.TASK_IDS),
                "note": ("Four of six overlap with gpt's seven. ward_transfer is "
                         "haiku-only; on_call and rest_break are gpt-only. This "
                         "is ID tested on haiku's dispersing items, not a "
                         "byte-identical repetition of the gpt designation.")},
            "primary_test": ("pooled paired ID+ vs ID- p < 0.05 AND the effect "
                             "pointing the same direction in at least 4 of 6 "
                             "items; both required, prespecified, two-sided"),
            "power": IDX.MEASURED_POWER,
            "locked_prediction": IDX.LOCKED_PREDICTION}


def prepare(persist=False):
    leak = leakage_gate()
    parent = read_checked(PARENT / "release.json")
    checkpoint = PARENT / "CHECKPOINT.json"
    check = read_checked(checkpoint) if checkpoint.exists() else parent
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        # phase4b_screen_r2 lost one screen probe to the v1 single-object rule and
        # it is preserved at full reservation under the no-retry rule. This
        # designation inherits exactly that one failure and names it, so any NEW
        # unresolved dispatch still stops the run. The failure is not retried:
        # that slot's result stays unreadable and is not recovered by v2.
        # Any subset of the three known inherited failures is acceptable; a
        # NEW unresolved dispatch is not. r1's timeout is named explicitly and
        # is never retried - that slot stays unresolved permanently.
        _known = {digest(INHERITED_FAILURE), digest(INHERITED_FAILURE_2),
                  digest(INHERITED_TIMEOUT)}
        if ledger.state["pending"] or not set(ledger.state["failed"]) <= _known:
            raise BudgetStop("Unexpected unresolved dispatch in inherited evidence")
        providers = dict(ledger.state["providers"])

    pop = population()
    batch = [_review_job()] + screen_jobs() + profiled_jobs(pop)
    slots = {j["slot"]: {"kind": j["kind"], "stage": j["stage"], "model": j["request"]["model"],
                         "input_token_bound": j["input_token_bound"],
                         "reserved_nano": j["reserved_nano"],
                         "max_output": j["request"].get("max_tokens",
                                                        j["request"].get("max_completion_tokens")),
                         "request_sha256": digest(j["request"])} for j in batch}
    bound = sum(j["reserved_nano"] for j in batch)
    for j in batch:
        providers[MODELS[j["request"]["model"]]] += j["reserved_nano"]

    # One review + two arms x 40 agents x 6 items = 481.
    expected = 1 + N_AGENTS * 2 * len(P.TASK_IDS)
    if len(slots) != expected or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: "
                             f"{total / 1e9:.4f} > {PROVIDER_CAPS[provider] / 1e9:.2f}")

    paths = [Path(__file__), ROOT / "code/phase4b_tasks_r2.py", ROOT / "code/phase4b_perm_pool.py", ROOT / "code/phase5_pd_prospective.py", ROOT / "code/phase5_label_semantics.py", ROOT / "code/phase5_coordinate_sweep.py", ROOT / "code/phase4b_permutation.py",
             ROOT / "code/phase5_id_crossmodel.py",
             ROOT / "code/phase4b_profiled_pool.py",
             ROOT / "code/phase4_crossmodel_dispatch_v2.py",
             ROOT / "code/phase4_choice_extraction_v2.py",
             FOLDER / "PROTOCOL.md", ROOT / "code/phase3_protocol_kernel.py",
             ROOT / "prompts/system_prompt_template.md"]
    release = {"id": STUDY, "population_sha256": digest(pop), "jobs_sha256": digest(batch),
               "slots": slots, "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP,
               # The 17 September amendment raised the OpenAI ceiling from $30
               # to $40. The release carries the caps forward from its parent,
               # so the amended figure is applied here explicitly rather than
               # inherited stale - which keeps the change auditable in the
               # frozen record rather than only in a collector constant.
               "provider_caps_nano": {**parent["provider_caps_nano"],
                                      **PROVIDER_CAPS},
               "parent_checkpoint_sha256": digest(check), "leakage_gate": leak,
               "historical_keys": sorted(p.stem for p in (LEDGER / "records").glob("*.json")),
               "preserved_files": {p.relative_to(LEDGER).as_posix(): sha(p)
                                   for p in LEDGER.rglob("*.json")},
               "failure_log_prefix_bytes": (LEDGER / "failures.jsonl").stat().st_size,
               "failure_log_prefix_sha256": sha(LEDGER / "failures.jsonl"),
               "source_sha256": {**parent["source_sha256"],
                                 **{p.relative_to(ROOT).as_posix(): sha(p) for p in paths}}}
    with Ledger(LEDGER, release):
        pass
    if persist:
        save(FOLDER / "population.json", pop)
        save(FOLDER / "requests.json", batch)
        save(FOLDER / "release.json", release)
    return release, pop, batch


def collect(replay=False, root=LEDGER, folder=FOLDER, responder=network, test_data=None):
    root, folder = Path(root), Path(folder)
    if root == LEDGER and test_data is not None:
        raise BudgetStop("Test data on real ledger")
    leakage_gate()
    release, pop, batch = test_data or tuple(
        read_checked(folder / f) for f in ("release.json", "population.json", "requests.json"))
    verify(release, root)
    if digest(pop) != release["population_sha256"] or digest(batch) != release["jobs_sha256"]:
        raise BudgetStop("Changed population or requests")
    if batch != [_review_job()] + screen_jobs() + profiled_jobs(pop):
        raise BudgetStop("Reconstructed schedule differs")
    if release["leakage_gate"]["task_content_sha256"] != P.content_hash():
        raise BudgetStop("Task content changed after release")

    manifest = {"release_sha256": digest(release), "jobs_sha256": digest(batch)}
    save(folder / "execution_manifest.json", manifest)
    n_screen = len(SCREEN_MODELS) * len(P.TASK_IDS) * SCREEN_N

    with Ledger(root, release) as ledger:
        # Any subset of the three known inherited failures is acceptable; a
        # NEW unresolved dispatch is not. r1's timeout is named explicitly and
        # is never retried - that slot stays unresolved permanently.
        _known = {digest(INHERITED_FAILURE), digest(INHERITED_FAILURE_2),
                  digest(INHERITED_TIMEOUT)}
        if ledger.state["pending"] or not set(ledger.state["failed"]) <= _known:
            raise BudgetStop("Unexpected unresolved dispatch")
        seen = set()

        def dispatch(job):
            record, _ = crossmodel_dispatch(ledger, job, digest(manifest), responder, replay)
            if charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Cost replay mismatch")
            seen.add(digest(job["slot"]))
            return record["parsed"]

        # r1's review, read from the ledger. NOT re-dispatched: the verdict
        # stands as recorded, `revise` included.
        review = read_review(dispatch(batch[0]))
        print(json.dumps({"review": review}), flush=True)

        if review["verdict"] != "accept" and not REVIEW_ADVISORY:
            result = {"study": STUDY, "decision": "review_stop",
                      "screen_calls": 0, "profiled_calls": 0}
        else:
            screen_rows = [{**j["cell"], "choice": dispatch(j)}
                           for j in batch[1:1 + n_screen]]
            screen = screen_outcome(screen_rows)
            save(folder / "screen_rows.json", screen_rows)
            usable = [t for t, v in screen.items() if v["usable"]]
            print(json.dumps({"screen": screen, "usable": usable}), flush=True)

            if len(usable) < MIN_USABLE:
                result = {"study": STUDY, "decision": "screen_stop", "screen": screen,
                          "usable_tasks": usable, "screen_calls": len(screen_rows),
                          "profiled_calls": 0,
                          "note": (f"Only {len(usable)} of {len(P.TASK_IDS)} items disperse; "
                                   f"{MIN_USABLE} required. The profiled stage did not run. "
                                   "A saturated item cannot show an arm difference.")}
            else:
                rows, done = list(screen_rows), 0
                for job in batch[1 + n_screen:]:
                    rows.append({**job["cell"], "choice": dispatch(job)})
                    done += 1
                    if done % 100 == 0:
                        print(json.dumps({"progress": done, "of": len(batch) - 1 - n_screen,
                                          "usd": round(ledger.state["recognition_nano"] / 1e9, 6)}),
                              flush=True)
                save(folder / "all_rows.json", rows)
                result = {"study": STUDY, "decision": "complete", "screen": screen,
                          "usable_tasks": usable,
                          "analysis": analyse(rows, usable),
                          "screen_calls": n_screen, "profiled_calls": done,
                          "moral_scores_assigned": False,
                          "note": ("Deterministic choice counts under stipulated standards. "
                                   "No moral label is assigned and no moral quality is "
                                   "measured.")}
                print(json.dumps({"analysis": result["analysis"]}), flush=True)

        if set(ledger.state["reservations"]) - set(release["historical_keys"]) != seen:
            raise BudgetStop("Unmanifested dispatch")
        result.update(review=review, calls=len(seen),
                      accounted_nano=ledger.state["recognition_nano"],
                      provider_totals_nano=ledger.state["providers"],
                      release_sha256=digest(release))
        save(folder / "results.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "run"))
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        release, _, batch = prepare(True)
        print(json.dumps({"maximum_usd": release["recognition_cap_nano"] / 1e9,
                          "total_calls": len(batch), "seed": SEEDS["population"]}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps(collect()))
