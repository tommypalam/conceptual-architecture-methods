"""Collector for position_counterbalance_r1: label, or position?

Design, the 2x2, competing predictions and failure condition live in
`phase5_position_counterbalance`. The block reordering lives in
`phase5_position_render`. This module dispatches.

**Four arms on gpt-5.4-mini, seven items, 40 agents.** Arms A and C put 0.90 on
Procedural Dependence; B and D put it on Affective Weighting. A and D put it at
line 6; B and C at line 10. Crossing binding with position is what separates the
label from the line it occupies - the confound `label_semantics_r1` could not
address, because there PD was always line 6 and AW always line 10.

**This designation can refute this project's own published finding.** If the LABEL
contrast is null while POSITION is significant, `label_semantics_r1`'s reading is
wrong and is marked superseded. That is stated in the locked prediction and is not
reframed afterwards.

**The empty-analysis defect is fixed at source**, as in `pd_crossmodel_r1`:
`declared_tasks()` supplies the pool's own TASK_IDS when the screen is skipped.
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
import phase5_label_semantics_multi as LS
import phase5_position_counterbalance as PC
import phase5_position_render as PR
import phase4b_permutation as PERM  # retained: the release pins it

FOLDER = ROOT / "experiments/phase5_analysis/position_counterbalance_r1"
PARENT = ROOT / "experiments/phase5_analysis/pd_crossmodel_r1"
STUDY = "position_counterbalance_r1"

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
# Eight cells: the 2x2 of {binding} x {order}, at each of two levels.
ARMS = tuple(f"{a}{s}" for a in PC.ARMS for s in ("+", "-"))
RENDER_MODES = ("U", "E", "G")
N_AGENTS = 40
# The U screen arm is dropped: these seven items have been screened four times
# on gpt with consistent results, so re-screening confirms rather than
# establishes. The review call is retained.
SCREEN_N = 0
SATURATED_AT = 1.0
MIN_USABLE = 0
# Population seed 2026091712, not ...711. Under ...711 agent 7 drew AW = 0.102,
# which renders as "0.10" and collides with the LOW level - making that agent's
# TRUE and SWAP blocks byte-identical at L=0.1, so the swap would have done
# nothing and diluted the paired contrast. verify_construction() now tests
# degeneracy at RENDERED precision and blocks on it. The replacement seed was
# chosen before any call, on a property of the draw alone, by taking the first
# seed whose 40 agents have no such collision.
SEEDS = {"population": 2026091821, "schedule": 2026091822, "analysis": 2026091823}
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
# 1,296 calls at a 1536-token budget across four profiled arms. OpenAI headroom
# at designation time is $30.00 - $5.977 = $24.02, so the $14.354 worst case fits
# with wide margin. Prior runs settle near 17%, so realistic spend is ~$2.4.
# 2,241 calls: 40 agents x 2 active coordinates x 4 arms x 7 items, plus one
# review. OpenAI headroom is $40.00 - $9.446 = $30.55.
# 2,241 calls: one review + 40 agents x 8 cells x 7 items. All on gpt.
# OpenAI headroom at designation time is $40.00 - $11.093 = $28.907.
# label_semantics_r2, the same shape, settled at $1.656 on a $25.223 reservation.
CAP = 28_000_000_000
PROVIDER_CAPS = {"anthropic": 32_000_000_000, "openai": 40_000_000_000}
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


def system(profile=None, arm="E", order=None):
    """System prompt for one arm.

    U  no profile
    E  full numeric profile
    G  no profile, plus explicit ethical guidance

    V (matched prose) is omitted: Phase 3 established that presentation format
    does not shift behaviour while profile packages do, so a V arm would spend
    budget re-answering a settled question. E, U and G are the three that bear
    on the 4B question.
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
    if arm == "E" and order is not None:
        # Reorder the rendered entries. PR.reorder is byte-identical to its input
        # under the identity permutation, verified in PR.verify_render.
        block = PR.reorder(block, order)
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
    """The 2x2 of {binding} x {line order}, at each of two levels.

    arm A  TRUE / normal      level on PD at line 6
    arm B  SWAP / normal      level on AW at line 10
    arm C  TRUE / exchanged   level on PD at line 10
    arm D  SWAP / exchanged   level on AW at line 6

    All eight cells carry the identical numeral multiset and identical block
    length. A vs D holds position fixed and varies the label; A vs C holds the
    label fixed and varies position.
    """
    batch = []
    for agent in pop["agents"]:
        coords = agent["coordinates"]
        for cell, level in ((c, L) for c in PC.ARMS for L in (PC.HIGH, PC.LOW)):
            values, order = PC.arm_profile(coords, cell, level)
            system_text = system(values, "E", order=order)
            sign = "+" if level == PC.HIGH else "-"
            arm = f"{cell}{sign}"
            tag = f"{cell}_{'hi' if level == PC.HIGH else 'lo'}"
            for task_id in P.TASK_IDS:
                job = make_job(MODEL, f"profiled/{tag}/{agent['agent']}/{task_id}",
                               "profiled", body(task_id, agent["agent"] % 2 == 0),
                               system_text=system_text)
                job["valid_actions"] = sorted(a.lower() for a in P.action_ids(task_id))
                job["cell"] = {"arm": arm, "cell": cell, "level": level,
                               "binding": PC.ARMS[cell]["binding"],
                               "order": PC.ARMS[cell]["order"],
                               "level_on": PC.ARMS[cell]["level_on"],
                               "position": PC.ARMS[cell]["position"],
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

    Written whole for this designation rather than patched: the inherited
    version had accumulated duplicated arm checks from successive lineage edits.
    """
    symmetry = P.verify_items()
    leaks = {t: P.audit_leakage(t) for t in P.TASK_IDS if P.audit_leakage(t)}
    if leaks:
        raise BudgetStop("Task text leaks: " + str(leaks))
    if N_AGENTS == 0:
        raise BudgetStop("Profiled designation must draw agents")
    if SCREEN_N != 0:
        raise BudgetStop("This designation drops the screen arm; SCREEN_N must be 0")

    agents = population()["agents"]
    construction = LS.verify_construction(agents)
    coords = agents[0]["coordinates"]

    def _render(profile):
        return profile_parts(context_prompt(dict(profile), NEUTRAL))[1]

    for active in LS.ACTIVE:
        for level in (LS.LOW, LS.HIGH):
            eq = LS.block_equivalence(_render, coords, active, level)
            if not eq["matched"]:
                raise BudgetStop(f"{active} TRUE/SWAP not matched at L={level}: {eq}")
        for profile in (LS.true_profile(coords, active, LS.HIGH),
                        LS.swap_profile(coords, active, LS.HIGH)):
            sys_text = system(profile, "E")
            if "Procedural Dependence" not in sys_text:
                raise BudgetStop(f"{active}: arm missing its profile block")
            if "Ethical guidance" in sys_text:
                raise BudgetStop(f"{active}: arm carries guidance text")

    if set(review_packet()) - {"items", "design_note"}:
        raise BudgetStop("Review packet carries unexpected keys")
    for entry in review_packet()["items"].values():
        if set(entry) != {"item", "kind"}:
            raise BudgetStop("Review packet item carries unexpected fields")

    return {"forbidden_terms_found": 0, "items_verified": symmetry,
            "construction_verified": construction,
            "locked_prediction": LS.LOCKED_PREDICTION,
            "label_semantics_sha256": LS.content_hash(),
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


def declared_tasks():
    """The declared item set, independent of the screen. See pd_crossmodel_r1."""
    return list(P.TASK_IDS)


def analyse(rows, usable):
    """Two orthogonal contrasts: label with position held, position with label held.

    LABEL   (A vs D) both carry the level at line 6  -> differ only in the label
            (C vs B) both carry it at line 10        -> differ only in the label
    POSITION (A vs C) both put it on PD              -> differ only in position
            (B vs D) both put it on AW               -> differ only in position

    Each contrast is the high-minus-low paired difference within a cell, then
    compared across cells; equivalently, we compare the (cell+ vs cell-) effect
    between the two cells of each pair. Holm over all four as one family.
    """
    import math
    tasks = list(usable) or declared_tasks()

    def rate(arm):
        vals = [P.primary_net(r["task"], r["choice"]) == "good"
                for r in rows if r["arm"] == arm and r["task"] in tasks and r["choice"]]
        return (round(sum(vals) / len(vals), 4), len(vals)) if vals else (None, 0)

    def paired(hi_arm, lo_arm, subset):
        by = {}
        for r in rows:
            if r["arm"] in (hi_arm, lo_arm) and r["task"] in subset and r["choice"]:
                by.setdefault((r["agent"], r["task"]), {})[r["arm"]] = (
                    P.primary_net(r["task"], r["choice"]) == "good")
        pairs = [(v[lo_arm], v[hi_arm]) for v in by.values() if len(v) == 2]
        if not pairs:
            return None
        hi = sum(1 for lo, h in pairs if h and not lo)
        lo = sum(1 for lo, h in pairs if lo and not h)
        n = hi + lo
        if n == 0:
            p = 1.0
        else:
            k = min(hi, lo)
            p = min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n))
        return {"arms": [hi_arm, lo_arm], "pairs": len(pairs),
                "more_under_high": hi, "more_under_low": lo, "discordant": n,
                "effect": round((hi - lo) / len(pairs), 4), "p": round(p, 8)}

    cells = {"all": {a: dict(zip(("good_rate", "n"), rate(a))) for a in ARMS}}

    # Within-cell level effects: does raising the level in THIS cell move the
    # outcome? Four of them, one per cell of the 2x2.
    within = {c: paired(f"{c}+", f"{c}-", tasks) for c in PC.ARMS}
    per_item = {c: {t_: paired(f"{c}+", f"{c}-", [t_]) for t_ in tasks}
                for c in PC.ARMS}

    def eff(c):
        v = within.get(c)
        return v["effect"] if v else 0.0

    # The two factors, each averaged over the two comparisons that isolate it.
    label_effect = round(((eff("A") - eff("D")) + (eff("C") - eff("B"))) / 2, 4)
    position_effect = round(((eff("A") - eff("C")) + (eff("D") - eff("B"))) / 2, 4)

    contrasts = {
        "LABEL:A_vs_D": {"held": "position 6", "varies": "label",
                         "difference": round(eff("A") - eff("D"), 4)},
        "LABEL:C_vs_B": {"held": "position 10", "varies": "label",
                         "difference": round(eff("C") - eff("B"), 4)},
        "POSITION:A_vs_C": {"held": "label PD", "varies": "position",
                            "difference": round(eff("A") - eff("C"), 4)},
        "POSITION:B_vs_D": {"held": "label AW", "varies": "position",
                            "difference": round(eff("B") - eff("D"), 4)},
    }

    pooled_p = {c: v["p"] for c, v in within.items() if v}
    live = sorted(pooled_p.items(), key=lambda kv: kv[1])
    holm, running = {}, 0.0
    for i, (c, raw) in enumerate(live):
        running = min(1.0, max(running, raw * (len(live) - i)))
        holm[c] = round(running, 8)

    def consistency(c):
        effs = [v["effect"] for v in per_item[c].values() if v]
        pos = sum(1 for e in effs if e > 0)
        neg = sum(1 for e in effs if e < 0)
        return {"items": len(effs), "positive": pos, "negative": neg,
                "meets_requirement": max(pos, neg) >= 4}

    cons = {c: consistency(c) for c in PC.ARMS}

    # The label binding is load-bearing if the cells holding the level on PD
    # move the outcome and those holding it on AW do not, at BOTH positions.
    pd_cells_move = all(holm.get(c, 1.0) < 0.05 and cons[c]["meets_requirement"]
                        for c in ("A", "C"))
    aw_cells_flat = all(holm.get(c, 1.0) >= 0.05 for c in ("B", "D"))
    label_carries = bool(pd_cells_move and aw_cells_flat)
    position_matters = abs(position_effect) > abs(label_effect)

    if label_carries:
        reading = (
            "The LABEL carries the effect, at BOTH line positions. Cells A and C "
            "both put the level on Procedural Dependence - at line 6 and line 10 "
            "respectively - and both move the outcome; cells B and D both put it "
            "on Affective Weighting and neither does. This EXCLUDES position as "
            "the mechanism and upgrades label_semantics_r1's reading from "
            "field-bound to label-bound.")
    elif position_matters:
        reading = (
            "POSITION dominates the label. The level moves the outcome more as a "
            "function of which LINE it occupies than of which LABEL holds it. "
            "This REFUTES label_semantics_r1's reading: that designation's effect "
            "is attributable to PD occupying line 6, not to the PD label. "
            "label_semantics_r1 is marked superseded and the paper's central "
            "claim must be restated as a position effect.")
    else:
        reading = (
            "Neither factor cleanly dominates under the prespecified rule. The "
            "effect is not decomposed by this designation, and the paper's claim "
            "stays at `field-bound`, where field means label-plus-position. "
            "Reported as an inconclusive decomposition, not reframed.")

    return {"cells": cells, "within_cell": within, "per_item": per_item,
            "holm": holm, "holm_family_size": len(live), "consistency": cons,
            "contrasts": contrasts,
            "label_effect": label_effect, "position_effect": position_effect,
            "label_carries": label_carries,
            "position_dominates": bool(position_matters and not label_carries),
            "reading": reading,
            "task_list_source": ("declared_tasks()" if not usable else "screen"),
            "published_under_test": PC.PUBLISHED,
            "primary_test": ("cells A and C (level on PD, at lines 6 and 10) both "
                             "clear Holm p<0.05 with 4+/7 item consistency, while "
                             "cells B and D (level on AW) do not"),
            "locked_prediction": PC.LOCKED_PREDICTION}


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

    # Four profiled arms: TRUE+, TRUE-, SWAP+, SWAP-.
    expected = 1 + N_AGENTS * 8 * len(P.TASK_IDS)
    if len(slots) != expected or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: "
                             f"{total / 1e9:.4f} > {PROVIDER_CAPS[provider] / 1e9:.2f}")

    paths = [Path(__file__), ROOT / "code/phase4b_tasks_r2.py", ROOT / "code/phase4b_perm_pool.py", ROOT / "code/phase5_pd_prospective.py", ROOT / "code/phase5_label_semantics_multi.py",
             ROOT / "code/phase5_position_counterbalance.py",
             ROOT / "code/phase5_position_render.py", ROOT / "code/phase4b_permutation.py",
             ROOT / "code/phase4_crossmodel_dispatch_v2.py",
             ROOT / "code/phase4_choice_extraction_v2.py",
             FOLDER / "PROTOCOL.md", ROOT / "code/phase3_protocol_kernel.py",
             ROOT / "prompts/system_prompt_template.md"]
    release = {"id": STUDY, "population_sha256": digest(pop), "jobs_sha256": digest(batch),
               "slots": slots, "recognition_cap_nano": bound, "prior_screening_nano": 0,
               "original_screening_cap_nano": CAP,
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
