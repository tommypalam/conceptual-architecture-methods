"""Phase 4A closeout on repaired materials: re-baseline, breadth, crossover.

**Screen only. No profiled arm, no participant profiles, no moral score.**

`breadth_focus_r1` stopped at its hard gate on a correct blocking issue: a
violating option whose DESCRIPTION carried the violation, where its paired option
carried no corresponding clause. `phase4_repaired_tasks` removes three such
clauses; the information survives in `effect_text`, and every flag, delta and
classification rule is unchanged.

Three arms, one review gate.

**RE-BASELINE.** The six tasks with a discriminating primary, at original
magnitudes, on all three models. Prior measurements were taken on the unrepaired
text and DO NOT TRANSFER: `haiku_screen_r4`'s modal shares and
`magnitude_sweep_r1`'s x1 cells describe different stimuli. This arm re-measures
them, and by comparison with those records also shows how much of the earlier
saturation the wording was carrying - which is itself a finding either way.

**BREADTH.** The five coercion/unfairness tasks, never screened on any model.
`magnitude_sweep_r1` tested deception against utility only. If haiku is flat here
too its rigidity is general across fixed standards; if it disperses, that finding
is deception-specific. These five have `primary_discriminates() == False` and so
can close 4A but cannot carry 4B; that is stated here so they are not later
mistaken for 4B candidates.

**FOCUS.** The `sonnet/safety_hold` crossover, at factors 2, 5 and 12 on the
REPAIRED text. On the unrepaired item sonnet ran 0.72 (x1) to 0.12 (x20), Holm
0.0005; those endpoints are not assumed here and the repaired x1 comes from the
re-baseline arm in this same designation. The aim is a cell near 0.5 - both
options live - which is what a profiled cross-model contrast needs and what
`capstone_model2_r4` lacked.

Locating a crossover is selection on BASELINE DISPERSION, which the Phase 3
protocol requires, not on outcomes. Every cell is reported whatever its shape. A
cell near 0.5 is wanted for its headroom, not because it favours any hypothesis
about profiles.

The review is a HARD GATE: the repaired descriptions are new materials.
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

import phase4_repaired_tasks as R
import phase4_magnitude_sweep_tasks as M

FOLDER = ROOT / "experiments/phase4_coding/breadth_r2"
PARENT = ROOT / "experiments/phase4_coding/pd_discriminant_r2"
STUDY = "breadth_r2"

SCREEN_N = 25
SATURATED_AT = 1.0
SEEDS = {"schedule": 2026091664, "analysis": 2026091665}
NEUTRAL = dict.fromkeys(AXES, "NEUTRAL")

HAIKU = "claude-haiku-4-5-20251001"
GPT = "gpt-5.4-mini-2026-03-17"
SONNET = "claude-sonnet-4-6"
MODELS_ALL = (HAIKU, GPT, SONNET)

# Tasks whose net primary can differ between options: 4B-capable.
BASELINE_TASKS = ()   # no re-baseline arm in this designation
# Coercion/unfairness tasks, never screened. Not 4B-capable by construction.
# Only the three tasks the closeout_r1 audit verified clean: neither option
# carries a closing sentence, so there is no presence-asymmetry in non-unit text.
# triage_override and quarantine_notice are EXCLUDED - both carry a one-sided
# closing sentence and were never repaired.
BREADTH_TASKS = ("quota_shortfall", "data_consent", "shelter_places")
FOCUS_TASK = "safety_hold"
FOCUS_MODEL = SONNET
FOCUS_FACTORS = ()   # no focus arm in this designation

CAP = 5_000_000_000
PROVIDER_CAPS = {"anthropic": 32_000_000_000, "openai": 30_000_000_000}
REVIEW_ADVISORY = False     # repaired descriptions are new materials

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")
_PLACEHOLDER = dict.fromkeys(PARAMETERS, 0.5)


def arm_tag(model):
    return "gpt" if "gpt" in model else model.split("-")[1]


def system():
    original = context_prompt(_PLACEHOLDER, NEUTRAL)
    prefix, block, suffix = profile_parts(original)
    suffix = suffix[:suffix.index("# Your task")] + (
        "# Your task\nUse the supplied information to make the requested decision. "
        "Do not infer a demographic identity or additional facts. "
        "Return only the requested JSON object.\n")
    return prefix + suffix


def _scaled_repaired(task_id, factor):
    """The repaired task at a magnitude factor.

    Repair and scaling are independent and must compose without either undoing
    the other: the repair deletes a clause from a description, the scaling
    multiplies a third-party cost and rewrites `effect_text`. Applying the
    repair's descriptions onto the scaled spec keeps both.
    """
    scaled = M.scaled_task(task_id, factor)
    repaired = R.task(task_id)
    for action_id in scaled["actions"]:
        scaled["actions"][action_id]["description"] = (
            repaired["actions"][action_id]["description"])
    return scaled


def body(spec, ids, first):
    order = list(ids)
    if not first:
        order.reverse()
    lines = [f"Option {a.upper()}: {spec['actions'][a]['description']} "
             f"{spec['actions'][a]['effect_text']}" for a in order]
    instruction = 'Return JSON only: {"choice":"<OPTION NAME>"}.'
    sep = chr(10) + chr(10)
    return sep.join((R.COMMON_FRAMING, spec["situation"],
                     "# Options" + chr(10) + chr(10).join(lines), instruction))


def make_job(model, slot, stage, text, maximum=768, system_text=None):
    """Build one job. `system_text` defaults to the unprofiled participant prompt;
    the review call supplies its own reviewer instructions instead."""
    system_text = system() if system_text is None else system_text
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
    for stage, tasks in (("baseline", BASELINE_TASKS), ("breadth", BREADTH_TASKS)):
        for model in MODELS_ALL:
            tag = arm_tag(model)
            for task_id in tasks:
                spec = R.task(task_id)
                for i in range(SCREEN_N):
                    job = make_job(model, f"{stage}/{tag}/{task_id}/{i}", stage,
                                   body(spec, R.action_ids(task_id), i % 2 == 0))
                    job["valid_actions"] = sorted(a.lower() for a in R.action_ids(task_id))
                    job["cell"] = {"arm": tag, "stage": stage, "task": task_id,
                                   "factor": 1, "index": i}
                    batch.append(job)
    tag = arm_tag(FOCUS_MODEL)
    for factor in FOCUS_FACTORS:
        spec = _scaled_repaired(FOCUS_TASK, factor)
        for i in range(SCREEN_N):
            job = make_job(FOCUS_MODEL, f"focus/{tag}/{FOCUS_TASK}/x{factor}/{i}",
                           "focus", body(spec, R.action_ids(FOCUS_TASK), i % 2 == 0))
            job["valid_actions"] = sorted(a.lower() for a in R.action_ids(FOCUS_TASK))
            job["cell"] = {"arm": tag, "stage": "focus", "task": FOCUS_TASK,
                           "factor": factor, "index": i}
            batch.append(job)
    return batch


def review_packet():
    """Participant text and item kind only, under neutral keys.

    Task identity, arm, standard type, stipulated price, magnitude factor and the
    crossover target are all withheld.
    """
    items, n = {}, 0
    for task_id in BASELINE_TASKS + BREADTH_TASKS:
        items[f"item_{n:02d}"] = {"item": R.participant_text(task_id), "kind": "conflict"}
        n += 1
    for factor in FOCUS_FACTORS:
        spec = _scaled_repaired(FOCUS_TASK, factor)
        lines = [f"Option {a.upper()}: {spec['actions'][a]['description']} "
                 f"{spec['actions'][a]['effect_text']}" for a in R.action_ids(FOCUS_TASK)]
        items[f"item_{n:02d}"] = {
            "item": "\n\n".join((R.COMMON_FRAMING, spec["situation"],
                                 "# Options\n" + "\n".join(lines))),
            "kind": "conflict"}
        n += 1
    return {"items": items,
            "design_note": ("One situation recurs with different stipulated quantities. "
                            "That variation is intended and is a manipulation under test; "
                            "it is not an inconsistency between items.")}


def review_job():
    job = make_job(JUDGE, "review/0", "review",
                   json.dumps(review_packet(), ensure_ascii=False, sort_keys=True),
                   1024, (
        "Review these decision items independently. Stipulated consequences are an "
        "intended and necessary part of every item; their presence is not a defect. "
        "Every item is a CONFLICT item: it must present a genuine conflict, with no "
        "option that is simply correct. One situation recurs at several magnitudes, "
        "and that magnitude is a manipulation under test - differing quantities across "
        "items are intended, not an inconsistency. Judge whether each item is "
        "answerable and non-leading. Flag an item only if it states which option the "
        "decision-maker ought to choose beyond the stipulated facts, if an option's "
        "DESCRIPTION labels it with a norm violation that its paired option's "
        "description does not carry, if it names a psychological construct or reveals "
        "a study hypothesis, or if its stipulated quantities are internally "
        "contradictory. Do not flag an item merely for having large numbers, and do "
        "not accept merely because the design could show an effect. Return only JSON "
        "with an overall verdict accept/revise/reject, a blocking_issues list and a "
        "limits list. Under 150 words."))
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


def leakage_gate():
    """Every gate that must pass before a single call is built."""
    repair = R.verify_repair()
    appended = R.audit_descriptions()
    if appended:
        raise BudgetStop("Option description still labels a violation: " + str(appended))
    leaks = {t: R.audit_leakage(t) for t in R.TASK_IDS if R.audit_leakage(t)}
    if leaks:
        raise BudgetStop("Task text leaks: " + str(leaks))
    # The focus arm must compose repair and scaling without losing either.
    for factor in FOCUS_FACTORS:
        spec = _scaled_repaired(FOCUS_TASK, factor)
        for action_id, action in spec["actions"].items():
            if action["description"] != R.task(FOCUS_TASK)["actions"][action_id]["description"]:
                raise BudgetStop(f"focus@{factor}: repair lost in scaling")
        if spec["situation"] != R.task(FOCUS_TASK)["situation"]:
            raise BudgetStop(f"focus@{factor}: situation changed")
    if set(review_packet()) - {"items", "design_note"}:
        raise BudgetStop("Review packet carries unexpected keys")
    for entry in review_packet()["items"].values():
        if set(entry) != {"item", "kind"}:
            raise BudgetStop("Review packet item carries unexpected fields")
    return {"forbidden_terms_found": 0, "repair_verified": repair,
            "appended_label_audit": "clean", "review_packet_clean": True,
            "task_content_sha256": R.content_hash()}


def outcome(rows):
    cells = {}
    keys = ([(arm_tag(m), "baseline", t, 1) for m in MODELS_ALL for t in BASELINE_TASKS]
            + [(arm_tag(m), "breadth", t, 1) for m in MODELS_ALL for t in BREADTH_TASKS]
            + [(arm_tag(FOCUS_MODEL), "focus", FOCUS_TASK, f) for f in FOCUS_FACTORS])
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
        clean = [a for a in R.action_ids(task_id)
                 if not any(R.task(task_id)["actions"][a][f]
                            for f in ("deceptive", "coercive", "unfair"))]
        entry = {"n_valid": len(votes), "modal_share": round(modal, 4),
                 "modal_choice": modal_choice,
                 "disperses": modal < SATURATED_AT,
                 "near_ceiling": bool(modal < SATURATED_AT and modal >= 0.85)}
        if len(clean) == 1:
            entry["clean_share"] = round(
                sum(1 for v in votes if v == clean[0]) / len(votes), 4)
        cells[key] = entry
    return cells


def crossover(cells):
    """The repaired focus curve, and the measured cell nearest 0.5."""
    tag = arm_tag(FOCUS_MODEL)
    series = []
    base = cells.get(f"{tag}/baseline/{FOCUS_TASK}/x1")
    if base and base["n_valid"]:
        series.append({"factor": 1, "clean_share": base.get("clean_share"),
                       "modal_share": base["modal_share"]})
    for factor in FOCUS_FACTORS:
        cell = cells.get(f"{tag}/focus/{FOCUS_TASK}/x{factor}")
        if cell and cell["n_valid"]:
            series.append({"factor": factor, "clean_share": cell.get("clean_share"),
                           "modal_share": cell["modal_share"]})
    shares = [s["clean_share"] for s in series if s["clean_share"] is not None]
    best = (min(series, key=lambda s: abs((s["clean_share"] or 0) - 0.5))
            if shares else None)
    return {"series": series, "nearest_to_half": best,
            "monotone_decreasing": all(a >= b for a, b in zip(shares, shares[1:])),
            "note": ("Measured on REPAIRED text. The unrepaired sonnet/safety_hold "
                     "curve from magnitude_sweep_r1 (0.72 at x1, 0.12 at x20) is a "
                     "different stimulus and is not comparable cell for cell.")}


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

    expected = (1 + len(MODELS_ALL) * (len(BASELINE_TASKS) + len(BREADTH_TASKS)) * SCREEN_N
                + len(FOCUS_FACTORS) * SCREEN_N)
    if len(slots) != expected or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: "
                             f"{total / 1e9:.4f} > {PROVIDER_CAPS[provider] / 1e9:.2f}")

    paths = [Path(__file__), ROOT / "code/phase4_repaired_tasks.py",
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
    if release["leakage_gate"]["task_content_sha256"] != R.content_hash():
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
                if done % 150 == 0:
                    print(json.dumps({"progress": done, "of": len(batch) - 1,
                                      "usd": round(ledger.state["recognition_nano"] / 1e9, 6)}),
                          flush=True)
            cells = outcome(rows)
            save(folder / "screen_rows.json", rows)
            usable = [k for k, v in cells.items() if v["disperses"]]
            result = {"study": STUDY, "decision": "screen_complete", "cells": cells,
                      "crossover": crossover(cells), "dispersing_cells": usable,
                      "screen_calls": len(rows), "participant_calls": 0,
                      "moral_scores_assigned": False,
                      "note": ("Unprofiled dispersion screening on repaired materials. No "
                               "profiled decision was collected and no moral label assigned. "
                               "Prior measurements on the unrepaired text are different "
                               "stimuli and are not comparable cell for cell.")}
            print(json.dumps({"crossover": result["crossover"],
                              "dispersing": len(usable)}), flush=True)

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
