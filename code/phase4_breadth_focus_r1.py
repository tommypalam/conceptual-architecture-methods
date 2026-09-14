"""Phase 4A closeout: standards breadth, and locating the sonnet crossover.

**Screen only. No profiled arm, no participant profiles, no moral score.**

Two arms, one designation, one review gate.

**BREADTH.** `magnitude_sweep_r1` tested one standard pair: deception against
utility. Five pool tasks have never been screened on any model and their
violating option is COERCIVE or UNFAIR rather than deceptive - `data_consent`,
`shelter_places`, `quarantine_notice` (coercion), `quota_shortfall`,
`triage_override` (unfairness). Run on all three models.

If haiku is flat here too, its rigidity is general across fixed standards. If it
disperses, the sweep's finding is deception-specific and narrower than it looks.
Both outcomes are reported.

These five tasks have `primary_discriminates() == False`. That is irrelevant to a
baseline dispersion screen and is stated so they are not later mistaken for
Phase 4B candidates: they close 4A, they cannot carry 4B.

**FOCUS.** `magnitude_sweep_r1` found `sonnet/safety_hold` at 0.72 (x1) and 0.12
(x20), Holm 0.0005. This brackets the crossover at factors 2, 5 and 12 to find a
magnitude sitting near 0.5 - both options live, maximum headroom in both
directions. That is the cell a profiled cross-model contrast needs and is what
`capstone_model2_r4` lacked.

Locating a crossover is selection on BASELINE DISPERSION, which the Phase 3
protocol requires, not on outcomes. It runs unprofiled, before any profiled call
exists, and every factor's result is reported whatever its shape. A cell near 0.5
is wanted for its headroom, not because it favours any hypothesis.

Scaling reuses `phase4_magnitude_sweep_tasks.scaled_task` unchanged, so factor-1
items remain byte-identical to the frozen originals.

Two stages, the second gated on the first:

  1. review - one independent design review. The breadth items are UNREVIEWED
              and the focus magnitudes are NEW, so this is a HARD GATE.
  2. screen - 25 unprofiled calls per cell.
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
from phase4_crossmodel_dispatch import dispatch as crossmodel_dispatch
from phase3_representation_diagnostic import profile_parts
from phase3_variant_round import save

import phase4_all_conflict_pool as T
import phase4_breadth_focus_tasks as B
import phase4_magnitude_sweep_tasks as M

FOLDER = ROOT / "experiments/phase4_coding/breadth_focus_r1"
PARENT = ROOT / "experiments/phase4_coding/magnitude_sweep_r1"
STUDY = "breadth_focus_r1"

SCREEN_N = 25
SATURATED_AT = 1.0
SEEDS = {"schedule": 2026091654, "analysis": 2026091655}
NEUTRAL = dict.fromkeys(AXES, "NEUTRAL")

HAIKU = "claude-haiku-4-5-20251001"
GPT = "gpt-5.4-mini-2026-03-17"
SONNET = "claude-sonnet-4-6"

BREADTH_MODELS = (HAIKU, GPT, SONNET)

CAP = 9_000_000_000      # $9.00 hard ceiling for this designation
PROVIDER_CAPS = {"anthropic": 32_000_000_000, "openai": 30_000_000_000}

# Unreviewed breadth items and new focus magnitudes: hard gate, not advisory.
REVIEW_ADVISORY = False

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")
_PLACEHOLDER = dict.fromkeys(PARAMETERS, 0.5)


def arm_tag(model):
    return "gpt" if "gpt" in model else model.split("-")[1]


def system():
    """Unprofiled system prompt: the profile block is removed entirely."""
    original = context_prompt(_PLACEHOLDER, NEUTRAL)
    prefix, block, suffix = profile_parts(original)
    suffix = suffix[:suffix.index("# Your task")] + (
        "# Your task\nUse the supplied information to make the requested decision. "
        "Do not infer a demographic identity or additional facts. "
        "Return only the requested JSON object.\n")
    return prefix + suffix


def body(situation, actions, ids, first):
    """Participant-visible text. `first` fixes which option is listed first."""
    order = list(ids)
    if not first:
        order.reverse()
    lines = [f"Option {a.upper()}: {actions[a]['description']} "
             f"{actions[a]['effect_text']}" for a in order]
    instruction = 'Return JSON only: {"choice":"<OPTION NAME>"}.'
    sep = chr(10) + chr(10)
    return sep.join((T.COMMON_FRAMING, situation,
                     "# Options" + chr(10) + chr(10).join(lines), instruction))


def breadth_body(task_id, first):
    spec = T.task(task_id)
    return body(spec["situation"], spec["actions"], T.action_ids(task_id), first)


def focus_body(factor, first):
    spec = M.scaled_task(B.FOCUS_TASK, factor)
    return body(spec["situation"], spec["actions"], M.action_ids(B.FOCUS_TASK), first)


def make_job(model, slot, stage, system_text, text, maximum=768):
    bound = len((system_text + text).encode("utf-8")) + 1024
    req = request(model, system_text, text, maximum, temperature=1)
    if MODELS[model] == "openai":
        req["response_format"] = {"type": "json_object"}
    return {"slot": f"{STUDY}/{slot}", "kind": "probe", "stage": stage, "request": req,
            "input_token_bound": bound,
            "reserved_nano": token_cost_nano(bound, maximum, *PRICES[model])}


def screen_jobs():
    """The full prespecified grid. Order is fixed and reconstructible."""
    batch = []
    for model in BREADTH_MODELS:
        tag = arm_tag(model)
        for task_id in B.BREADTH_TASKS:
            for i in range(SCREEN_N):
                job = make_job(model, f"breadth/{tag}/{task_id}/{i}", "breadth",
                               system(), breadth_body(task_id, i % 2 == 0))
                job["valid_actions"] = sorted(a.lower() for a in T.action_ids(task_id))
                job["cell"] = {"arm": tag, "stage": "breadth", "task": task_id,
                               "factor": 1, "index": i}
                batch.append(job)
    tag = arm_tag(B.FOCUS_MODEL)
    for factor in B.FOCUS_FACTORS:
        for i in range(SCREEN_N):
            job = make_job(B.FOCUS_MODEL, f"focus/{tag}/{B.FOCUS_TASK}/x{factor}/{i}",
                           "focus", system(), focus_body(factor, i % 2 == 0))
            job["valid_actions"] = sorted(a.lower() for a in M.action_ids(B.FOCUS_TASK))
            job["cell"] = {"arm": tag, "stage": "focus", "task": B.FOCUS_TASK,
                           "factor": factor, "index": i}
            batch.append(job)
    return batch


def review_packet():
    """Exactly what the reviewer sees: participant text and item kind only.

    Task identity, arm, standard type, stipulated price and the crossover target
    are all withheld. An earlier designation leaked a per-item price field, which
    revealed the manipulation; nothing of that kind appears here.
    """
    items = {}
    for i, task_id in enumerate(B.BREADTH_TASKS):
        items[f"item_{i:02d}"] = {"item": B.breadth_text(task_id), "kind": "conflict"}
    for j, factor in enumerate(B.FOCUS_FACTORS, start=len(B.BREADTH_TASKS)):
        items[f"item_{j:02d}"] = {"item": B.focus_text(factor), "kind": "conflict"}
    return {"items": items,
            "design_note": ("One situation recurs with different stipulated quantities. "
                            "That variation is intended and is a manipulation under test; "
                            "it is not an inconsistency between items.")}


def review_job():
    job = make_job(JUDGE, "review/0", "review", (
        "Review these decision items independently. Stipulated consequences are an "
        "intended and necessary part of every item; their presence is not a defect. "
        "Every item is a CONFLICT item: it must present a genuine conflict, with no "
        "option that is simply correct. One situation recurs at several magnitudes, "
        "and that magnitude is a manipulation under test - differing quantities across "
        "items are intended, not an inconsistency. Judge whether each item is "
        "answerable and non-leading. Flag an item only if it states which option the "
        "decision-maker ought to choose beyond the stipulated facts, if it names a "
        "psychological construct or reveals a study hypothesis, or if its stipulated "
        "quantities are internally contradictory. Do not flag an item merely for "
        "having large numbers, and do not accept merely because the design could show "
        "an effect. Return only JSON with an overall verdict accept/revise/reject, a "
        "blocking_issues list and a limits list. Under 150 words."),
        json.dumps(review_packet(), ensure_ascii=False, sort_keys=True), 1024)
    job["raw_text"] = True
    assert not job.get("valid_actions"), "Review job must not declare valid_actions"
    return job


def _json_objects(text):
    """Every balanced top-level {...} span in `text`, in order."""
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
    """Read a verdict from a reply in any shape these models produce."""
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


def leakage_gate():
    """Refuse to build a batch that leaks, editorialises, or is malformed."""
    leaks = B.audit_leakage()
    if leaks:
        raise BudgetStop("Task text leaks: " + str(leaks))
    pool = B.verify_pool()
    if set(review_packet()) - {"items", "design_note"}:
        raise BudgetStop("Review packet carries unexpected keys")
    for entry in review_packet()["items"].values():
        if set(entry) != {"item", "kind"}:
            raise BudgetStop("Review packet item carries unexpected fields")
    return {"forbidden_terms_found": 0, "pool_verified": pool,
            "review_packet_clean": True, "task_content_sha256": B.content_hash()}


def outcome(rows):
    """Modal share and clean-option share per cell."""
    cells = {}
    keys = ([(arm_tag(m), "breadth", t, 1) for m in BREADTH_MODELS for t in B.BREADTH_TASKS]
            + [(arm_tag(B.FOCUS_MODEL), "focus", B.FOCUS_TASK, f) for f in B.FOCUS_FACTORS])
    for arm, stage, task_id, factor in keys:
        votes = [r["choice"] for r in rows
                 if r["arm"] == arm and r["stage"] == stage
                 and r["task"] == task_id and r["factor"] == factor and r["choice"]]
        key = f"{arm}/{stage}/{task_id}/x{factor}"
        if not votes:
            cells[key] = {"n_valid": 0, "modal_share": None, "disperses": False}
            continue
        counts = {v: votes.count(v) for v in set(votes)}
        modal_choice = max(counts, key=counts.get)
        modal = counts[modal_choice] / len(votes)
        if stage == "breadth":
            preferred = B.clean_action(task_id)
            label = "clean_share"
            price = B.price_of_clean(task_id)
        else:
            preferred = M._honest_action(task_id)
            label = "honest_share"
            price = M.price_of_honesty(task_id, factor)
        cells[key] = {"n_valid": len(votes), "modal_share": round(modal, 4),
                      "modal_choice": modal_choice, "price": price,
                      label: round(sum(1 for v in votes if v == preferred) / len(votes), 4),
                      "disperses": modal < SATURATED_AT}
    return cells


def crossover(cells):
    """The focus curve with x1/x20 from the parent, and the nearest-to-0.5 cell."""
    tag = arm_tag(B.FOCUS_MODEL)
    series = [{"factor": 1, "honest_share": 0.72, "source": "magnitude_sweep_r1"}]
    for factor in B.FOCUS_FACTORS:
        cell = cells.get(f"{tag}/focus/{B.FOCUS_TASK}/x{factor}")
        if cell and cell["n_valid"]:
            series.append({"factor": factor, "honest_share": cell["honest_share"],
                           "price": cell["price"], "source": STUDY})
    series.append({"factor": 20, "honest_share": 0.12, "source": "magnitude_sweep_r1"})
    series.sort(key=lambda s: s["factor"])
    measured = [s for s in series if s["source"] == STUDY]
    best = min(measured, key=lambda s: abs(s["honest_share"] - 0.5)) if measured else None
    return {"series": series, "nearest_to_half": best,
            "monotone": all(a["honest_share"] >= b["honest_share"]
                            for a, b in zip(series, series[1:]))}


def prepare(persist=False):
    leak = leakage_gate()
    parent = read_checked(PARENT / "release.json")
    checkpoint = PARENT / "CHECKPOINT.json"
    check = read_checked(checkpoint) if checkpoint.exists() else parent
    verify(parent)
    with Ledger(LEDGER, parent) as ledger:
        if ledger.state["pending"] or ledger.state["failed"]:
            raise BudgetStop("Unresolved dispatch in inherited evidence")
        providers = dict(ledger.state["providers"])

    population = {"n_agents": 0, "agents": [], "note": "screen-only designation"}
    batch = [review_job()] + screen_jobs()
    slots = {j["slot"]: {"kind": j["kind"], "stage": j["stage"], "model": j["request"]["model"],
                         "input_token_bound": j["input_token_bound"],
                         "reserved_nano": j["reserved_nano"],
                         "max_output": j["request"].get("max_tokens",
                                                        j["request"].get("max_completion_tokens")),
                         "request_sha256": digest(j["request"])} for j in batch}
    bound = sum(j["reserved_nano"] for j in batch)
    for j in batch:
        providers[MODELS[j["request"]["model"]]] += j["reserved_nano"]

    expected = (1 + len(BREADTH_MODELS) * len(B.BREADTH_TASKS) * SCREEN_N
                + len(B.FOCUS_FACTORS) * SCREEN_N)
    if len(slots) != expected or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: "
                             f"{total / 1e9:.4f} > {PROVIDER_CAPS[provider] / 1e9:.2f}")

    paths = [Path(__file__), ROOT / "code/phase4_breadth_focus_tasks.py",
             ROOT / "code/phase4_magnitude_sweep_tasks.py",
             ROOT / "code/phase4_all_conflict_pool.py",
             ROOT / "code/phase4_crossmodel_dispatch.py",
             ROOT / "code/phase4_choice_extraction.py",
             FOLDER / "PROTOCOL.md", ROOT / "code/phase3_protocol_kernel.py",
             ROOT / "prompts/system_prompt_template.md"]
    release = {"id": STUDY, "population_sha256": digest(population), "jobs_sha256": digest(batch),
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
        save(FOLDER / "population.json", population)
        save(FOLDER / "requests.json", batch)
        save(FOLDER / "release.json", release)
    return release, population, batch


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
    if batch != [review_job()] + screen_jobs():
        raise BudgetStop("Reconstructed schedule differs")
    if release["leakage_gate"]["task_content_sha256"] != B.content_hash():
        raise BudgetStop("Task content changed after release")

    manifest = {"release_sha256": digest(release), "jobs_sha256": digest(batch)}
    save(folder / "execution_manifest.json", manifest)

    with Ledger(root, release) as ledger:
        if ledger.state["pending"] or ledger.state["failed"]:
            raise BudgetStop("Unexpected unresolved dispatch")
        seen = set()

        def dispatch(job):
            record, _ = crossmodel_dispatch(ledger, job, digest(manifest), responder, replay)
            if charge(record["raw"], job, False) != record["accounted_nano"]:
                raise BudgetStop("Cost replay mismatch")
            seen.add(digest(job["slot"]))
            return record["parsed"]

        review = read_review(dispatch(batch[0]))
        print(json.dumps({"review": review,
                          "accounted_usd": ledger.state["recognition_nano"] / 1e9}), flush=True)

        if review["verdict"] != "accept" and not REVIEW_ADVISORY:
            result = {"study": STUDY, "decision": "review_stop",
                      "screen_calls": 0, "participant_calls": 0}
        else:
            rows, done = [], 0
            for job in batch[1:]:
                rows.append({**job["cell"], "choice": dispatch(job)})
                done += 1
                if done % 100 == 0:
                    print(json.dumps({"progress": done, "of": len(batch) - 1,
                                      "usd": round(ledger.state["recognition_nano"] / 1e9, 6)}),
                          flush=True)
            cells = outcome(rows)
            save(folder / "screen_rows.json", rows)
            result = {"study": STUDY, "decision": "screen_complete", "cells": cells,
                      "crossover": crossover(cells), "screen_calls": len(rows),
                      "participant_calls": 0, "moral_scores_assigned": False,
                      "note": ("Unprofiled dispersion screening only. No profiled decision "
                               "was collected and no moral label assigned.")}
            print(json.dumps({"crossover": result["crossover"]}), flush=True)

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
                          "total_calls": len(batch), "seed": SEEDS["schedule"]}))
    else:
        if not args.yes:
            raise BudgetStop("Explicit execution flag required")
        print(json.dumps(collect()))
