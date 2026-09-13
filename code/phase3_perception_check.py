"""Controlled Asch-family stimulus competence check, no peers or ethical profiles."""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import random
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFont
from phase3_budget import Budget, BudgetStop, canonical, digest, read_checked, token_cost_nano, write_once

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "experiments/phase3_benchmarks/perception_20260913"
LEDGER = ROOT / "data/raw/phase3_20260913_budget"
MODEL = "gpt-5.4-mini-2026-03-17"
SEED = 2026091305
FONT = Path("C:/Windows/Fonts/arial.ttf")
SYSTEM = "Answer the visual comparison question using the image. Return only the requested JSON."


def stimuli():
    rows = []
    palette = [[180, 60, 60], [60, 150, 80], [60, 90, 180],
               [170, 110, 40], [140, 60, 165], [40, 145, 155]]
    for kind in ("line", "colour"):
        for exemplar in range(6):
            for correct in range(3):
                reference = 120 + 12 * exemplar if kind == "line" else palette[exemplar]
                wrong = [reference - 48, reference + 48] if kind == "line" else [palette[(exemplar + 2) % 6], palette[(exemplar + 4) % 6]]
                choices = wrong.copy()
                choices.insert(correct, reference)
                rows.append({"id": f"{kind}_{exemplar}_{correct}", "kind": kind,
                             "reference": reference, "choices": choices, "correct": "ABC"[correct]})
    random.Random(SEED).shuffle(rows)
    return rows


def render(row):
    image = Image.new("RGB", (512, 384), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(FONT), 20)
    xs = (64, 192, 320, 448)
    for x, label in zip(xs, ("Reference", "A", "B", "C")):
        draw.text((x, 34), label, fill="black", anchor="mm", font=font)
    values = [row["reference"]] + row["choices"]
    for x, value in zip(xs, values):
        if row["kind"] == "line":
            draw.rectangle((x-3, 310-value, x+3, 309), fill="black")
        else:
            draw.rectangle((x-40, 140, x+39, 219), fill=tuple(value))
    stream = BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()


def request_for(row, png):
    question = ("Which line, A, B, or C, has the same length as the reference line? "
                if row["kind"] == "line" else
                "Which colour swatch, A, B, or C, matches the reference colour? ")
    question += 'Return exactly {"choice":"A"}, {"choice":"B"}, or {"choice":"C"}.'
    return {"model": MODEL, "messages": [{"role": "system", "content": SYSTEM},
        {"role": "user", "content": [{"type": "text", "text": question},
         {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(png).decode(), "detail": "high"}}]}],
        "max_completion_tokens": 64, "temperature": 1.0, "reasoning_effort": "none", "service_tier": "default"}


def reservation(request):
    # Full documented high-detail image maximum, not just this small PNG's estimate.
    image_bound = 3002  # 2,500 patches * 1.2, plus rounding margin.
    text = SYSTEM + request["messages"][1]["content"][0]["text"]
    bound = len(text.encode("utf-8")) + 1024 + image_bound
    return bound, token_cost_nano(bound, 64, ".75", "4.5")


def prepare():
    PACKAGE.mkdir(parents=True, exist_ok=True)
    rows, jobs = stimuli(), []
    for row in rows:
        png = render(row)
        path = PACKAGE / "stimuli" / (row["id"] + ".png")
        path.parent.mkdir(exist_ok=True)
        if path.exists():
            if path.read_bytes() != png:
                raise BudgetStop("Existing stimulus differs")
        else:
            with path.open("xb") as handle:
                handle.write(png)
        request = request_for(row, png)
        bound, cost = reservation(request)
        jobs.append({"slot": "perception_r1/" + row["id"], "stimulus": row,
                     "image": path.relative_to(ROOT).as_posix(), "image_sha256": hashlib.sha256(png).hexdigest(),
                     "request_sha256": digest(request), "input_token_bound": bound, "reserved_nano": cost})
    sources = [Path(__file__), ROOT / "code/phase3_budget.py", PACKAGE / "PROTOCOL.md"]
    plan = {"status": "PERCEPTION_CHECK_ONLY", "seed": SEED, "model": MODEL,
            "jobs": jobs, "n_calls": 36, "n_profiles": 0, "configuration": None,
            "budget_category": "structural_review", "full_reservation_nano": sum(j["reserved_nano"] for j in jobs),
            "font_sha256": hashlib.sha256(FONT.read_bytes()).hexdigest(),
            "source_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    if plan["full_reservation_nano"] > 200_000_000:
        raise BudgetStop("Perception check cannot fit $0.20 reservation")
    manifest = PACKAGE / "manifest.json"
    if manifest.exists():
        if read_checked(manifest) != plan:
            raise BudgetStop("Frozen perception plan changed")
    else:
        write_once(manifest, plan)
    return plan


def parse(raw, job):
    if raw.get("model") != MODEL:
        raise ValueError("Unexpected snapshot")
    usage = raw.get("usage", {})
    if any(type(usage.get(k)) is not int or usage[k] < 0 for k in ("prompt_tokens", "completion_tokens")):
        raise ValueError("Invalid usage")
    if usage["prompt_tokens"] > job["input_token_bound"] or usage["completion_tokens"] > 64:
        raise ValueError("Reservation bound exceeded")
    choices = raw.get("choices", [])
    if len(choices) != 1 or choices[0].get("finish_reason") != "stop":
        raise ValueError("Incomplete output")
    answer = json.loads(choices[0]["message"]["content"])
    if set(answer) != {"choice"} or answer["choice"] not in ("A", "B", "C"):
        raise ValueError("Invalid choice")
    return answer["choice"]


def network_call(request):
    req = Request("https://api.openai.com/v1/chat/completions", data=canonical(request),
                  headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"],
                           "Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=90) as response:
        return json.loads(response.read())


def run(plan, root=LEDGER, responder=network_call, *, replay=False):
    results, n_new = [], 0
    with Budget(root) as budget:
        state = budget.audit()
        if state["pending"] or state["failed"]:
            raise BudgetStop("Existing unresolved dispatch prevents continuation")
        # Reserve capacity for the entire still-missing schedule before dispatch.
        remaining = sum(j["reserved_nano"] for j in plan["jobs"] if digest(j["slot"]) not in state["reservations"])
        if state["by_stage_nano"]["structural_review"] + remaining > 2_000_000_000:
            raise BudgetStop("Whole remaining schedule cannot fit review allocation")
        for job in plan["jobs"]:
            png = (ROOT / job["image"]).read_bytes()
            request = request_for(job["stimulus"], png)
            if hashlib.sha256(png).hexdigest() != job["image_sha256"] or digest(request) != job["request_sha256"]:
                raise BudgetStop("Stimulus/request changed")
            key = digest(job["slot"])
            path = Path(root) / "records" / f"{key}.json"
            if key in state["reservations"]:
                intent = state["reservations"][key]
                if intent["request"] != request or intent["manifest_sha256"] != digest(plan):
                    raise BudgetStop("Replay identity mismatch")
                record = read_checked(path)
                settlement = read_checked(Path(root) / "settlements" / f"{key}.json")
                if settlement["response_sha256"] != digest(record):
                    raise BudgetStop("Response/settlement mismatch")
                answer = parse(record["raw"], job)
            else:
                if replay:
                    raise BudgetStop("Offline replay found a missing call")
                budget.reserve(job["slot"], "structural_review", request, job["reserved_nano"], digest(plan))
                raw, error, answer = None, None, None
                try:
                    raw = responder(request)
                    answer = parse(raw, job)
                except Exception as exc:
                    error = {"type": type(exc).__name__, "status": exc.code if isinstance(exc, HTTPError) else None}
                usage = (raw or {}).get("usage", {})
                known = all(type(usage.get(k)) is int and usage[k] >= 0 for k in ("prompt_tokens", "completion_tokens"))
                cost = token_cost_nano(usage["prompt_tokens"], usage["completion_tokens"], ".75", "4.5") if known else job["reserved_nano"]
                if error:
                    cost = max(cost, job["reserved_nano"])
                record = {"raw": raw, "error": error, "answer": answer, "accounted_nano": cost,
                          "manifest_sha256": digest(plan), "timestamp": datetime.now(timezone.utc).isoformat()}
                write_once(path, record)
                budget.settle(key, cost, digest(record), status="failed" if error else "complete")
                n_new += 1
                if error:
                    raise BudgetStop("Perception check halted; raw failure retained")
            results.append({"id": job["stimulus"]["id"], "kind": job["stimulus"]["kind"],
                            "answer": answer, "correct": answer == job["stimulus"]["correct"],
                            "accounted_nano": record["accounted_nano"]})
            print(f"Perception check: {len(results)}/{len(plan['jobs'])}", flush=True)
    return results, n_new


def summary(rows):
    return {kind: {"n": sum(r["kind"] == kind for r in rows),
                   "correct": sum(r["kind"] == kind and r["correct"] for r in rows),
                   "stimulus_gate_passed": sum(r["kind"] == kind for r in rows) == 18 and all(r["correct"] for r in rows if r["kind"] == kind)} for kind in ("line", "colour")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "run", "replay"))
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        plan = prepare()
        print(json.dumps({"calls": 36, "maximum_reserved_usd": plan["full_reservation_nano"] / 1e9, "seed": SEED}))
    else:
        plan = read_checked(PACKAGE / "manifest.json")
        for name, sha in plan["source_sha256"].items():
            if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != sha:
                raise BudgetStop("Frozen source changed")
        if args.command == "run" and (not args.yes or not os.environ.get("OPENAI_API_KEY")):
            parser.error("Requires --yes and configured OpenAI key")
        rows, n_new = run(plan, replay=args.command == "replay")
        report = {"seed": SEED, "configuration": None, "n_profiles": 0, "results": rows,
                  "summary": summary(rows), "accounted_usd": sum(r["accounted_nano"] for r in rows)/1e9,
                  "note": "Stimulus competence only; no peer influence, ethical encoding or human-rate test."}
        path = PACKAGE / "result.json"
        if path.exists():
            if read_checked(path) != report:
                raise BudgetStop("Existing result changed")
        else:
            write_once(path, report)
        print(json.dumps({"new_calls": n_new, "summary": report["summary"], "accounted_usd": report["accounted_usd"]}))
