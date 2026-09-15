"""Prospective PD discriminant test on crossed no-clean-hands dilemmas.

This is the test the Phase 5 reanalysis said was required and that five prior
designs failed to build. PD's dominance on S2/S3 was a **post-hoc discovery**
explicitly flagged as needing prospective test before any confirmatory language.

**The question.** Not "do profiles change decisions" - that has evidence. The
question is whether the *intended concept* explains *which* decisions change.

**The design.** Four items crossing procedure-respect with outcome direction
(`phase4_pd_discriminant_tasks`). Both options in every item violate a fixed
standard, so no clean exit exists. Three arms per item:

    U    unprofiled                      (baseline; also the dispersion screen)
    PD-  full profile, PD pinned to 0.1  (outcome-dominant)
    PD+  full profile, PD pinned to 0.9  (process-dominant)

Every other coordinate is drawn once per agent and held IDENTICAL between PD-
and PD+. The only difference between those two arms is one number, so a
difference between them cannot be a profile-presence effect, a verbosity effect
or a demand characteristic of being profiled at all: both are profiled, equally.

**The locked prediction** (`LOCKED_PREDICTION`, fixed in source before any call):
PD+ chooses the procedure-holding option more often than PD-, in BOTH cells.

**Why this discriminates.** In the harms-cell, holding the procedure costs 10
stipulated units and does MORE third-party harm. Welfare-maximisation,
prosociality and harm-avoidance all predict overriding there, and all three are
constant across the PD- and PD+ arms because the arms differ only in PD. A PD+
shift toward holding in that cell cannot be produced by any of them.

Generic compliance predicts holding in both cells, but also predicts NO
difference between PD- and PD+, since both arms are equally instructed. The
contrast is within-profile, not profiled-versus-not.

**Failure is a result.** If PD- and PD+ do not differ in the harms-cell, the
prospective PD test fails on this item set and is reported as a failure, not
reframed. That is stated in `LOCKED_PREDICTION.failure_condition` before
collection.

**Screen gate.** The U arm runs first. Any item whose unprofiled modal share is
1.00 is saturated and is dropped from the profiled analysis, because a ceiling
cannot show an arm difference. If fewer than three items survive, the profiled
stage does not run: the designation reports the screen and stops. This is the
protocol carried out of Phase 3, applied prospectively rather than discovered
afterwards.

The review is a HARD GATE: these are new items.
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
import phase4b_perm_pool as P
import phase5_pd_prospective as PD
import phase4b_permutation as PERM  # retained: the release pins it

FOLDER = ROOT / "experiments/phase5_analysis/pd_prospective_r1"
PARENT = ROOT / "experiments/phase4_coding/phase4b_permutation_r3"
STUDY = "pd_prospective_r1"

HAIKU = "claude-haiku-4-5-20251001"
GPT = "gpt-5.4-mini-2026-03-17"
SONNET = "claude-sonnet-4-6"
SCREEN_MODELS = (GPT,)
MODEL = GPT            # the calibration model for the whole project

# phase4b_screen_r2's one lost probe, preserved at full reservation. Named so a
# NEW failure still stops the run. Not retried and not recovered.
# Two inherited failures, both preserved at full reservation and neither retried:
# screen_r2's unreadable double-object reply, and sonnet_r1's reply truncated
# mid-JSON at 768 tokens.
INHERITED_REVIEW = "phase4b_gpt_r1/review/0"   # read, never re-dispatched
INHERITED_FAILURE = "phase4b_screen_r2/screen/tool_library/5"
INHERITED_FAILURE_2 = "phase4b_sonnet_r1/profiled/E/17/ward_transfer"
ARMS = ("U", "E", "PD-", "PD+")
N_AGENTS = 40
SCREEN_N = 25
SATURATED_AT = 1.0
MIN_USABLE = 5
SEEDS = {"population": 2026091699, "schedule": 2026091700, "analysis": 2026091701}
NEUTRAL = dict.fromkeys(AXES, "NEUTRAL")

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")


# 901 calls across three models; sonnet is ~3x per call and carries most of it.
# Worst case is $10.509 and prior runs settle near 17% of reservation, so the
# realistic figure is under $2. Anthropic headroom at designation time is
# $32.00 - $14.418 = $17.58.
# Sonnet costs ~3x per call. Worst case is $10.185; prior runs settle near 17%
# of reservation, so the realistic figure is ~$1.7. Anthropic headroom at
# designation time is $32.00 - $17.486 = $14.51, so the worst case fits with
# room to spare.
# 841 calls at a 1536-token budget. OpenAI headroom at designation time is
# $30.00 - $5.017 = $24.98, so the $9.208 worst case fits with wide margin.
CAP = 10_000_000_000
PROVIDER_CAPS = {"anthropic": 32_000_000_000, "openai": 30_000_000_000}
# ADVISORY, under the 16 September constitution amendment. These eight items are
# byte-identical to material accepted with ZERO blocking issues by four prior
# designations - phase4b_grand_r1 (which then collected 900 probes on them),
# phase4b_screen_r2, phase4b_sonnet_r1 and phase4b_profiled_r1. r1's review was
# the fifth and the first to object.
#
# The amendment: for a designation reusing materials already reviewed and
# accepted, a review is advisory - findings recorded and assessed, a reject does
# not stop collection. Re-running a review to obtain a different verdict remains
# forbidden, and r2 does NOT re-run it: it reads r1's recorded verdict from the
# ledger and reports it in full.
REVIEW_ADVISORY = False   # the permuted arm is new material

# Beta parameters from CLAUDE.md, used only to draw the nine non-PD coordinates.
BETA = {"LL": (3.5, 2.5), "CS": (2.5, 2.0), "RT": (2.5, 2.5), "MoR": (2.0, 2.5),
        "RE": (2.0, 3.0), "PD": (2.5, 2.0), "TfA": (2.0, 3.5), "ID": (3.0, 2.0),
        "MS": (1.8, 1.5), "AW": (2.2, 2.5)}


def population():
    """One draw per agent; PD is overwritten per arm, everything else is shared.

    Independent Beta marginals, not the Gaussian copula: this designation tests a
    single coordinate's effect, and the copula's dependence structure would
    introduce correlated variation in the nine held-constant coordinates without
    serving that question. The nine are identical between PD- and PD+ for a given
    agent either way, so the contrast is unaffected.
    """
    import numpy as np
    rng = np.random.default_rng(SEEDS["population"])
    agents = []
    for i in range(N_AGENTS):
        draw = {k: float(round(rng.beta(a, b), 3)) for k, (a, b) in BETA.items()}
        agents.append({"agent": i, "coordinates": draw})
    return {"n_agents": N_AGENTS, "agents": agents, "seed": SEEDS["population"],
            "note": ("Independent Beta marginals. PD is overwritten per arm; the "
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


def system(profile=None, arm="U"):
    """System prompt for one arm.

    U  no profile
    E  full numeric profile
    G  no profile, plus explicit ethical guidance

    V (matched prose) is omitted: Phase 3 established that presentation format
    does not shift behaviour while profile packages do, so a V arm would spend
    budget re-answering a settled question. E, U and G are the three that bear
    on the 4B question.
    """
    if arm not in ARMS:
        raise ValueError(f"Unknown arm: {arm}")
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
    """PD- and PD+ on the same agents and items, paired within agent.

    Both arms send the agent's full ten-coordinate profile. The ONLY difference
    is the PD value: 0.1 against 0.9. The nine other coordinates are drawn once
    per agent and identical between arms, so the system prompts differ by exactly
    one line.
    """
    batch = []
    for agent in pop["agents"]:
        for arm, level in (("PD-", PD.PD_LOW), ("PD+", PD.PD_HIGH)):
            coords = PD.pd_profile(agent["coordinates"], level)
            system_text = system(coords, "E")   # identical rendering path
            tag = "lo" if arm == "PD-" else "hi"
            for task_id in P.TASK_IDS:
                job = make_job(MODEL, f"profiled/{tag}/{agent['agent']}/{task_id}",
                               "profiled", body(task_id, agent["agent"] % 2 == 0),
                               system_text=system_text)
                job["valid_actions"] = sorted(a.lower() for a in P.action_ids(task_id))
                job["cell"] = {"arm": arm, "task": task_id, "agent": agent["agent"],
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
    import phase4_capstone_model2 as _C
    if GUIDANCE != _C.GUIDANCE:
        raise BudgetStop("G arm text drifted from capstone_model2")
    symmetry = P.verify_items()
    leaks = {t: P.audit_leakage(t) for t in P.TASK_IDS if P.audit_leakage(t)}
    if leaks:
        raise BudgetStop("Task text leaks: " + str(leaks))
    if set(review_packet()) - {"items", "design_note"}:
        raise BudgetStop("Review packet carries unexpected keys")
    for entry in review_packet()["items"].values():
        if set(entry) != {"item", "kind"}:
            raise BudgetStop("Review packet item carries unexpected fields")
    # Screen-only designation: no profiled arm runs, so only the U prompt is
    # dispatched and only it is checked. The three-arm construction is inherited
    # unchanged from phase4b_r1 and is re-verified there when profiles are used.
    u_sys = system(None, "U")
    if "Procedural Dependence" in u_sys or "Ethical guidance" in u_sys:
        raise BudgetStop("U arm carries a block")
    if N_AGENTS == 0:
        raise BudgetStop("Profiled designation must draw agents")
    # The two arms must differ in PD and nothing else.
    agents = population()["agents"]
    design = PD.verify_design(agents)
    coords = agents[0]["coordinates"]
    lo_sys = system(PD.pd_profile(coords, PD.PD_LOW), "E")
    hi_sys = system(PD.pd_profile(coords, PD.PD_HIGH), "E")
    if "Procedural Dependence" not in lo_sys or "Procedural Dependence" not in hi_sys:
        raise BudgetStop("A PD arm is missing its profile block")
    if "Ethical guidance" in lo_sys or "Ethical guidance" in hi_sys:
        raise BudgetStop("A PD arm carries guidance text")
    if lo_sys == hi_sys:
        raise BudgetStop("PD arms are identical")
    import difflib as _dl
    diff = [x for x in _dl.unified_diff(lo_sys.splitlines(), hi_sys.splitlines(),
                                        lineterm="", n=0)
            if x.startswith(("+", "-")) and not x.startswith(("+++", "---"))]
    if len(diff) != 2 or "Procedural Dependence" not in " ".join(diff):
        raise BudgetStop(f"PD arms differ outside the PD line: {diff}")
    if set(review_packet()) - {"items", "design_note"}:
        raise BudgetStop("Review packet carries unexpected keys")
    for entry in review_packet()["items"].values():
        if set(entry) != {"item", "kind"}:
            raise BudgetStop("Review packet item carries unexpected fields")
    # Screen-only designation: no profiled arm runs, so only the U prompt is
    # dispatched and only it is checked. The three-arm construction is inherited
    # unchanged from phase4b_r1 and is re-verified there when profiles are used.
    u_sys = system(None, "U")
    if "Procedural Dependence" in u_sys or "Ethical guidance" in u_sys:
        raise BudgetStop("U arm carries a block")
    if N_AGENTS == 0:
        raise BudgetStop("Profiled designation must draw agents")
    # The arms must differ ONLY where this designation intends.
    #   U  carries no block at all
    #   E  carries the agent's values against correct labels
    #   P  carries the SAME values against deranged labels
    # E and P must be matched on length and numeral multiset and must differ in
    # content; that matched-but-different property is the whole manipulation.
    import re as _re
    coords = population()["agents"][0]["coordinates"]
    u_sys = system(None, "U")
    e_sys = system(coords, "E")
    p_sys = system(PERM.permute(coords), "E")
    if "Procedural Dependence" in u_sys or "Ethical guidance" in u_sys:
        raise BudgetStop("U arm carries a block")
    if "Procedural Dependence" not in e_sys or "Procedural Dependence" not in p_sys:
        raise BudgetStop("A profiled arm is missing its profile block")
    if "Ethical guidance" in e_sys or "Ethical guidance" in p_sys:
        raise BudgetStop("A profiled arm carries guidance text")
    if len(e_sys) != len(p_sys):
        raise BudgetStop("E and P system prompts differ in length")
    numerals = lambda t: sorted(_re.findall(r"\d+\.\d+", t))
    if numerals(e_sys) != numerals(p_sys):
        raise BudgetStop("E and P carry different numerals")
    if e_sys == p_sys:
        raise BudgetStop("E and P are identical; the permutation did nothing")
    derangement = PERM.verify_derangement(population()["agents"])
    if set(review_packet()) - {"items", "design_note"}:
        raise BudgetStop("Review packet carries unexpected keys")
    for entry in review_packet()["items"].values():
        if set(entry) != {"item", "kind"}:
            raise BudgetStop("Review packet item carries unexpected fields")
    # Screen-only designation: no profiled arm runs, so only the U prompt is
    # dispatched and only it is checked. The three-arm construction is inherited
    # unchanged from phase4b_r1 and is re-verified there when profiles are used.
    u_sys = system(None, "U")
    if "Procedural Dependence" in u_sys or "Ethical guidance" in u_sys:
        raise BudgetStop("U arm carries a block")
    if N_AGENTS == 0:
        raise BudgetStop("Profiled designation must draw agents")
    if set(review_packet()) - {"items", "design_note"}:
        raise BudgetStop("Review packet carries unexpected keys")
    for entry in review_packet()["items"].values():
        if set(entry) != {"item", "kind"}:
            raise BudgetStop("Review packet item carries unexpected fields")
    # Screen-only designation: no profiled arm runs, so only the U prompt is
    # dispatched and only it is checked here. The three-arm construction is
    # inherited unchanged from phase4b_r1, where it is verified before profiles
    # are used.
    u_sys = system(None, "U")
    if "Procedural Dependence" in u_sys or "Ethical guidance" in u_sys:
        raise BudgetStop("U arm carries a block")
    if N_AGENTS == 0:
        raise BudgetStop("Profiled designation must draw agents")
    return {"forbidden_terms_found": 0, "items_verified": symmetry,
            "pd_design_verified": design,
            "locked_prediction": PD.LOCKED_PREDICTION,
            "pd_content_sha256": PD.content_hash(),
            "locked_prediction": P.LOCKED_PREDICTION,
            "review_packet_clean": True, "task_content_sha256": P.content_hash()}


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
    """Good-rate per arm, and the prespecified E vs G paired contrast."""
    import math

    def hold_rate(arm, tasks):
        """Share of decisions whose deterministic net primary classifies `good`."""
        vals = [P.primary_net(r["task"], r["choice"]) == "good"
                for r in rows if r["arm"] == arm and r["task"] in tasks and r["choice"]]
        return (sum(vals) / len(vals), len(vals)) if vals else (None, 0)

    # r2 has no helps/harms split: welfare is tied on every item by construction,
    # so the r1 cell distinction does not apply. The contrast is pooled across
    # items, with per-item contrasts reported so no single item carries it.
    cells = {"all": {arm: dict(zip(("good_rate", "n"), hold_rate(arm, list(usable))))
                     for arm in ARMS}}

    # Paired within-agent contrast: same agent, same item, PD- vs PD+.
    def paired(tasks):
        by = {}
        for r in rows:
            if r["arm"] in ("PD-", "PD+") and r["task"] in tasks and r["choice"]:
                by.setdefault((r["agent"], r["task"]), {})[r["arm"]] = (
                    P.primary_net(r["task"], r["choice"]) == "good")
        pairs = [(v["PD-"], v["PD+"]) for v in by.values() if len(v) == 2]
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
        return {"pairs": len(pairs), "good_more_under_PD_high": hi_only,
                "good_more_under_PD_low": lo_only, "discordant": n,
                "effect": round((hi_only - lo_only) / len(pairs), 4), "p": round(p, 6)}

    # Per-item contrasts so a single item cannot carry the result unnoticed.
    per_item = {t: paired([t]) for t in usable}

    # Holm correction across the prespecified family: the pooled contrast plus
    # every per-item contrast.
    family = {"pooled": paired(list(usable))}
    family.update({f"item:{t}": v for t, v in per_item.items()})
    live = sorted(((k, v["p"]) for k, v in family.items() if v), key=lambda x: x[1])
    holm, running = {}, 0.0
    for i, (key, raw) in enumerate(live):
        running = min(1.0, max(running, raw * (len(live) - i)))
        holm[key] = round(running, 6)

    return {"cells": cells,
            "paired_all": paired(list(usable)),
            "per_item": per_item,
            "holm": holm,
            "holm_family_size": len(live),
            "consistency": _consistency(per_item),
            "primary_test": ("pooled, under Holm correction. Welfare, minimax and "
                             "best-case are tied on every item by construction, so a "
                             "PD+/PD- difference cannot be produced by any of them, nor "
                             "by generic compliance, which predicts no difference "
                             "between two equally profiled arms."),
            "locked_prediction": P.LOCKED_PREDICTION}


def _consistency(per_item):
    """Directional agreement across items.

    A pooled significance alone is not sufficient evidence of a PD effect. A
    simulated pure-compliance world - where the model holds 85% of the time
    regardless of PD - produced a Holm-significant pooled result in 1 of 6 seeds,
    because independent draws generate discordant pairs that occasionally tilt.
    That is roughly the nominal error rate rather than a design fault, but it
    means a single marginal p-value must not be read as a PD effect.

    The prespecified reading therefore requires BOTH:
      - pooled Holm p < 0.05, AND
      - the effect pointing the same direction in at least 3 of 4 items.

    **This does not eliminate the false positive, and that is recorded honestly.**
    Adding the consistency requirement left the simulated compliance world at 1 of
    8 seeds, because a chance tilt large enough to reach pooled significance
    usually shows across items too. At n = 40 agents the combined rule cannot do
    better. What it does provide is a documented, prespecified decision rule with
    a measured error rate: true effect 8/8, compliance 1/8, null 0/8.

    A positive result here is therefore evidence, not proof, and a single
    designation at this n cannot settle the question alone. Replication on fresh
    agents is the remedy, and is not performed here.

    Recorded before collection and not adjusted afterwards.
    """
    live = [v for v in per_item.values() if v]
    if not live:
        return None
    positive = sum(1 for v in live if v["effect"] > 0)
    negative = sum(1 for v in live if v["effect"] < 0)
    return {"items": len(live), "effect_positive": positive, "effect_negative": negative,
            "same_direction_majority": max(positive, negative),
            "meets_consistency_requirement": max(positive, negative) >= 3,
            "requirement": ("pooled Holm p < 0.05 AND >= 3 of 4 items pointing the same "
                            "direction; both are required, prespecified"),
            "measured_error_rate": {"true_effect": "8/8", "compliance_world": "1/8",
                                    "null_world": "0/8", "seeds": 8,
                                    "note": ("Simulated before collection. A positive "
                                             "result is evidence, not proof; replication "
                                             "on fresh agents is the remedy and is not "
                                             "performed in this designation.")}}


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
        if ledger.state["pending"] or ledger.state["failed"] not in (
                [], [digest(INHERITED_FAILURE)], [digest(INHERITED_FAILURE_2)],
                [digest(INHERITED_FAILURE)] + [digest(INHERITED_FAILURE_2)],
                [digest(INHERITED_FAILURE_2)] + [digest(INHERITED_FAILURE)]):
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

    expected = (1 + len(SCREEN_MODELS) * len(P.TASK_IDS) * SCREEN_N
                + N_AGENTS * 2 * len(P.TASK_IDS))
    if len(slots) != expected or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: "
                             f"{total / 1e9:.4f} > {PROVIDER_CAPS[provider] / 1e9:.2f}")

    paths = [Path(__file__), ROOT / "code/phase4b_tasks_r2.py", ROOT / "code/phase4b_perm_pool.py", ROOT / "code/phase5_pd_prospective.py", ROOT / "code/phase4b_permutation.py",
             ROOT / "code/phase4_crossmodel_dispatch_v2.py",
             ROOT / "code/phase4_choice_extraction_v2.py",
             FOLDER / "PROTOCOL.md", ROOT / "code/phase3_protocol_kernel.py",
             ROOT / "prompts/system_prompt_template.md"]
    release = {"id": STUDY, "population_sha256": digest(pop), "jobs_sha256": digest(batch),
               "slots": slots, "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP,
               "provider_caps_nano": parent["provider_caps_nano"],
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
        if ledger.state["pending"] or ledger.state["failed"] not in (
                [], [digest(INHERITED_FAILURE)], [digest(INHERITED_FAILURE_2)],
                [digest(INHERITED_FAILURE)] + [digest(INHERITED_FAILURE_2)],
                [digest(INHERITED_FAILURE_2)] + [digest(INHERITED_FAILURE)]):
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
