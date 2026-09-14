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
from phase4_crossmodel_dispatch import dispatch as crossmodel_dispatch
from phase3_representation_diagnostic import profile_parts
from phase3_variant_round import save

import phase4_pd_discriminant_tasks as P

FOLDER = ROOT / "experiments/phase4_coding/pd_discriminant_r1"
PARENT = ROOT / "experiments/phase4_coding/closeout_r1"
STUDY = "pd_discriminant_r1"

MODEL = "claude-haiku-4-5-20251001"
N_AGENTS = 40
SCREEN_N = 25
SATURATED_AT = 1.0
MIN_USABLE = 3
SEEDS = {"population": 2026091658, "schedule": 2026091659, "analysis": 2026091660}
NEUTRAL = dict.fromkeys(AXES, "NEUTRAL")

PARAMETERS = ("LL", "CS", "RT", "MoR", "RE", "PD", "TfA", "ID", "MS", "AW")
PD_LOW, PD_HIGH = 0.1, 0.9

CAP = 11_000_000_000
PROVIDER_CAPS = {"anthropic": 32_000_000_000, "openai": 30_000_000_000}
REVIEW_ADVISORY = False     # new items

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


def system(profile=None):
    """Unprofiled when profile is None; otherwise the full ten-coordinate block."""
    base = dict.fromkeys(PARAMETERS, 0.5) if profile is None else dict(profile)
    original = context_prompt(base, NEUTRAL)
    prefix, block, suffix = profile_parts(original)
    suffix = suffix[:suffix.index("# Your task")] + (
        "# Your task\nUse the supplied information to make the requested decision. "
        "Do not infer a demographic identity or additional facts. "
        "Return only the requested JSON object.\n")
    return prefix + (block if profile is not None else "") + suffix


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


def make_job(model, slot, stage, text, maximum=768, system_text=None):
    system_text = system() if system_text is None else system_text
    bound = len((system_text + text).encode("utf-8")) + 1024
    req = request(model, system_text, text, maximum, temperature=1)
    if MODELS[model] == "openai":
        req["response_format"] = {"type": "json_object"}
    return {"slot": f"{STUDY}/{slot}", "kind": "probe", "stage": stage, "request": req,
            "input_token_bound": bound,
            "reserved_nano": token_cost_nano(bound, maximum, *PRICES[model])}


def screen_jobs():
    """Unprofiled dispersion screen, and the U baseline for the analysis."""
    batch = []
    for task_id in P.TASK_IDS:
        for i in range(SCREEN_N):
            job = make_job(MODEL, f"screen/{task_id}/{i}", "screen",
                           body(task_id, i % 2 == 0))
            job["valid_actions"] = sorted(a.lower() for a in P.action_ids(task_id))
            job["cell"] = {"arm": "U", "task": task_id, "agent": None, "index": i}
            batch.append(job)
    return batch


def profiled_jobs(pop):
    """PD- and PD+ on identical agents and identical items."""
    batch = []
    for agent in pop["agents"]:
        for arm, level in (("PD-", PD_LOW), ("PD+", PD_HIGH)):
            profile = dict(agent["coordinates"])
            profile["PD"] = level
            system_text = system(profile)
            for task_id in P.TASK_IDS:
                tag = "lo" if arm == "PD-" else "hi"
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


def leakage_gate():
    symmetry = P.verify_symmetry()
    leaks = {t: P.audit_leakage(t) for t in P.TASK_IDS if P.audit_leakage(t)}
    if leaks:
        raise BudgetStop("Task text leaks: " + str(leaks))
    if set(review_packet()) - {"items", "design_note"}:
        raise BudgetStop("Review packet carries unexpected keys")
    for entry in review_packet()["items"].values():
        if set(entry) != {"item", "kind"}:
            raise BudgetStop("Review packet item carries unexpected fields")
    # The two profiled arms must differ in PD and nothing else.
    pop = population()
    sample = pop["agents"][0]["coordinates"]
    lo, hi = dict(sample), dict(sample)
    lo["PD"], hi["PD"] = PD_LOW, PD_HIGH
    if {k: v for k, v in lo.items() if k != "PD"} != {k: v for k, v in hi.items() if k != "PD"}:
        raise BudgetStop("Profiled arms differ outside PD")
    return {"forbidden_terms_found": 0, "symmetry_verified": symmetry,
            "locked_prediction": P.LOCKED_PREDICTION,
            "review_packet_clean": True, "task_content_sha256": P.content_hash()}


def screen_outcome(rows):
    out = {}
    for task_id in P.TASK_IDS:
        votes = [r["choice"] for r in rows if r["task"] == task_id and r["choice"]]
        if not votes:
            out[task_id] = {"n_valid": 0, "modal_share": None, "usable": False}
            continue
        counts = {v: votes.count(v) for v in set(votes)}
        modal = max(counts.values()) / len(votes)
        hold = P.hold_action(task_id)
        out[task_id] = {"n_valid": len(votes), "modal_share": round(modal, 4),
                        "hold_share": round(sum(1 for v in votes if v == hold) / len(votes), 4),
                        "procedure_helps": P.procedure_helps(task_id),
                        "usable": modal < SATURATED_AT}
    return out


def analyse(rows, usable):
    """Hold-rate per arm and cell, and the prespecified PD+ vs PD- contrast."""
    import math

    def hold_rate(arm, tasks):
        vals = [(r["agent"], r["task"], r["choice"] == P.hold_action(r["task"]))
                for r in rows if r["arm"] == arm and r["task"] in tasks and r["choice"]]
        return (sum(v for _, _, v in vals) / len(vals), len(vals)) if vals else (None, 0)

    helps = [t for t in usable if P.procedure_helps(t)]
    harms = [t for t in usable if not P.procedure_helps(t)]
    cells = {}
    for label, tasks in (("helps", helps), ("harms", harms), ("all", list(usable))):
        cells[label] = {arm: dict(zip(("hold_rate", "n"), hold_rate(arm, tasks)))
                        for arm in ("U", "PD-", "PD+")}

    # Paired within-agent contrast: same agent, same item, PD- vs PD+.
    def paired(tasks):
        by = {}
        for r in rows:
            if r["arm"] in ("PD-", "PD+") and r["task"] in tasks and r["choice"]:
                by.setdefault((r["agent"], r["task"]), {})[r["arm"]] = (
                    r["choice"] == P.hold_action(r["task"]))
        pairs = [(v["PD-"], v["PD+"]) for v in by.values() if len(v) == 2]
        if not pairs:
            return None
        hi_only = sum(1 for lo, hi in pairs if hi and not lo)
        lo_only = sum(1 for lo, hi in pairs if lo and not hi)
        n = hi_only + lo_only
        # Exact two-sided sign test on discordant pairs.
        if n == 0:
            p = 1.0
        else:
            k = min(hi_only, lo_only)
            p = min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n))
        return {"pairs": len(pairs), "hold_more_under_PD_high": hi_only,
                "hold_more_under_PD_low": lo_only, "discordant": n,
                "effect": round((hi_only - lo_only) / len(pairs), 4), "p": round(p, 6)}

    # Per-item contrasts as well as per-cell, so a single item cannot carry the
    # result unnoticed.
    per_item = {t: paired([t]) for t in usable}

    # Holm correction across the prespecified family: the two cell contrasts plus
    # every per-item contrast. Uncorrected p-values over this many comparisons
    # produce spurious hits; a simulated null run showed one at p = 0.014.
    family = {"cell:helps": paired(helps), "cell:harms": paired(harms)}
    family.update({f"item:{t}": v for t, v in per_item.items()})
    live = sorted(((k, v["p"]) for k, v in family.items() if v), key=lambda x: x[1])
    holm, running = {}, 0.0
    for i, (key, raw) in enumerate(live):
        running = min(1.0, max(running, raw * (len(live) - i)))
        holm[key] = round(running, 6)

    return {"cells": cells,
            "paired_all": paired(list(usable)),
            "paired_helps": paired(helps),
            "paired_harms": paired(harms),
            "per_item": per_item,
            "holm": holm,
            "holm_family_size": len(live),
            "discriminating_cell": "harms",
            "primary_test": ("cell:harms under Holm correction. The helps-cell and the "
                             "per-item contrasts are reported but are secondary: only the "
                             "harms-cell separates PD from welfare, prosociality and "
                             "harm-avoidance."),
            "locked_prediction": P.LOCKED_PREDICTION}


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

    expected = 1 + len(P.TASK_IDS) * SCREEN_N + N_AGENTS * 2 * len(P.TASK_IDS)
    if len(slots) != expected or bound > CAP:
        raise BudgetStop(f"Size or cap exceeded: {len(slots)} calls, {bound / 1e9:.6f} USD")
    for provider, total in providers.items():
        if total > PROVIDER_CAPS[provider]:
            raise BudgetStop(f"{provider} ceiling would be exceeded: "
                             f"{total / 1e9:.4f} > {PROVIDER_CAPS[provider] / 1e9:.2f}")

    paths = [Path(__file__), ROOT / "code/phase4_pd_discriminant_tasks.py",
             ROOT / "code/phase4_crossmodel_dispatch.py",
             ROOT / "code/phase4_choice_extraction.py",
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
    n_screen = len(P.TASK_IDS) * SCREEN_N

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
