"""Local, read-only visual replay of the completed Phase 2 confirmation.

Run: py -3.11 -B code/serve_replay.py
No collector or API client is instantiated. Only allowlisted UI/API routes exist.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from functools import lru_cache
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "output" / "phase2_runtime"))
PACKAGE = ROOT / "experiments" / "phase2_confirmation_20260913"
RAW = ROOT / "data" / "raw" / "phase2_confirmation_20260913"
UI = ROOT / "viewer"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    ensure_ascii=False).encode("utf-8")).hexdigest()


def read_json(path, envelope=False):
    value = json.loads(path.read_text(encoding="utf-8"))
    if envelope:
        if digest(value["payload"]) != value["sha256"]:
            raise ValueError(f"Checksum mismatch: {path.name}")
        return value["payload"]
    return value


class ReplayStore:
    def __init__(self):
        if (RAW / "execution.lock").exists():
            raise ValueError("Replay requires a completed study; collection lock exists")
        self.manifest = read_json(PACKAGE / "manifest.json", True)
        for name, expected in self.manifest["source_hashes"].items():
            if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
                raise ValueError(f"Frozen source differs: {name}")
        # Import the verified frozen pure parser/state functions, never the runner.
        from phase2_confirmation_design import advance, initial_state, parse, resolve, group_messages
        from engine.population import Population
        self.advance, self.initial_state, self.parse = advance, initial_state, parse
        self.resolve, self.group_messages = resolve, group_messages
        population = read_json(PACKAGE / "population.json")
        schedule = read_json(PACKAGE / "schedule.json", True)
        if digest(population) != self.manifest["population_hash"] or digest(schedule) != self.manifest["schedule_hash"]:
            raise ValueError("Population or schedule differs from the frozen manifest")
        self.agents = {a.agent_id: a for a in Population.load(PACKAGE / "population.json").agents}
        self.groups = {}
        for group in schedule["groups"]:
            for config, arm in group["conditions"]:
                key = f"{group['problem']}-{group['group']}-{config}-{arm}"
                self.groups[key] = (group, config, arm)
        self.evidence = read_json(ROOT / "experiments" / "phase2_exploratory_20260912" / "evidence_schedule.json")
        self.parameters = [{k: v[k] for k in ("name", "label", "endpoint_0", "endpoint_1")}
                           for v in read_json(ROOT / "docs" / "variables.json")["variables"]
                           if v.get("role") == "agent_parameter"]

    def index(self):
        return {"study": "Phase 2 confirmation", "seed": self.manifest["root_seed"],
                "model": self.manifest["model"], "manifest_hash": digest(self.manifest),
                "parameters": self.parameters, "runs": [
                    {"id": key, "problem": g["problem"], "group": g["group"], "config": c, "arm": a}
                    for key, (g, c, a) in sorted(self.groups.items())]}

    @lru_cache(maxsize=300)
    def replay(self, key):
        group, config, arm = self.groups[key]
        problem = group["problem"]
        artifact_key = digest([problem, group["group"], config, arm])
        artifact = read_json(RAW / "groups" / f"{artifact_key}.json", True)
        state = self.initial_state(group)
        labels = list(artifact["result"]["final_tally"])
        labels.remove("missing")
        rounds = []
        previous_votes = {}
        for rnd in range(1, artifact["result"]["rounds"] + 1):
            before = deepcopy(state)
            parsed, responses = {}, []
            for agent in sorted(group["agent_ids"]):
                slot = ["complex", problem, group["group"], config, arm, rnd, agent]
                record_key = digest(slot)
                record = read_json(RAW / "records" / f"{record_key}.json", True)
                intent = read_json(RAW / "dispatches" / f"{record_key}.json", True)
                messages = self.group_messages(self.agents[agent], config, arm, group, state, rnd)
                if (record["slot"] != slot or intent["slot"] != slot or record["meta"] != intent["meta"]
                        or record["meta"]["state_hash_before"] != digest(state)
                        or record["intent_hash"] != digest(intent)
                        or intent["manifest_hash"] != digest(self.manifest)
                        or intent["request"]["messages"] != messages or record["mock"] or intent["mock"]):
                    raise ValueError(f"Request/state provenance differs: {key}, round {rnd}, agent {agent}")
                p = self.parse(record, labels)
                parsed[agent] = p
                own = sorted(item for delivered, items in group["direct_evidence"][str(agent)].items()
                             if int(delivered) <= rnd for item in items)
                vote_before = previous_votes.get(agent)
                responses.append({"agent": agent, "vote": p["vote"], "status": p["status"],
                                  "fields": p["fields"], "field_errors": p["field_errors"],
                                  "text": p["text"], "messages": messages, "held": own,
                                  "previous_vote": vote_before,
                                  "changed": bool(p["vote"] and vote_before and p["vote"] != vote_before),
                                  "record": f"data/raw/phase2_confirmation_20260913/records/{record_key}.json",
                                  "record_hash": digest(record)})
                # A missing vote breaks the adjacent-round comparison; do not infer a preference.
                previous_votes[agent] = p["vote"]
            done = self.advance(state, parsed, rnd)
            if done and rnd != artifact["result"]["rounds"]:
                raise ValueError("Saved run continued after its stopping rule")
            rounds.append({"number": rnd, "responses": responses, "tally": deepcopy(state["tallies"][-1]),
                           "public_before": before["public_evidence"], "public_after": list(state["public_evidence"]),
                           "proposals_before": before["proposals"], "proposals_after": dict(state["proposals"]),
                           "adopted_before": before["adopted"], "adopted_after": list(state["adopted"]),
                           "audit": deepcopy(state["audit"][len(before["audit"]):])})
        if state != artifact["state"] or self.resolve(state) != artifact["result"]:
            raise ValueError(f"Final state/outcome differs: {key}")
        from engine.questions import load_dilemma_body, PHASE0B_QUESTIONS
        from phase2_confirmation_design import FILES
        return {"id": key, "problem": problem, "group": group["group"], "config": config, "arm": arm,
                "group_seed": group["seed"], "ceo": group["ceo"], "labels": labels,
                "agents": [self.agents[a].as_record() for a in sorted(group["agent_ids"])],
                "scenario": load_dilemma_body(FILES[problem], PHASE0B_QUESTIONS),
                "evidence": self.evidence if problem == "C3" else [], "rounds": rounds,
                "result": artifact["result"], "verified": True}


class Handler(BaseHTTPRequestHandler):
    store: ReplayStore

    def do_GET(self):
        if self.headers.get("Host") not in {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}:
            self.send_error(403)
            return
        route = urlparse(self.path).path
        try:
            if route == "/api/index":
                payload, mime = json.dumps(self.store.index()).encode(), "application/json"
            elif route.startswith("/api/run/"):
                payload = json.dumps(self.store.replay(route.removeprefix("/api/run/")), ensure_ascii=False).encode("utf-8")
                mime = "application/json"
            elif route in {"/", "/index.html", "/app.js", "/style.css"}:
                name = "index.html" if route == "/" else route[1:]
                payload = (UI / name).read_bytes()
                mime = {"html": "text/html", "js": "text/javascript", "css": "text/css"}[name.split(".")[-1]]
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", mime + "; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(payload)
        except KeyError:
            self.send_error(404, "Unknown recorded run")
        except (ValueError, OSError) as exc:
            self.send_error(409, "Recording unavailable or failed verification")
            print(f"Replay refused: {exc}", flush=True)

    def log_message(self, *_args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--verify-all", action="store_true", help="Verify all 300 replays offline and exit")
    args = parser.parse_args()
    store = ReplayStore()
    if args.verify_all:
        count = invalid = 0
        for key in store.groups:
            for rnd in store.replay(key)["rounds"]:
                count += len(rnd["responses"])
                invalid += sum(r["vote"] is None for r in rnd["responses"])
        print(json.dumps({"verified_runs": len(store.groups), "response_rows": count,
                          "columns": ["agent", "vote", "status", "fields", "text", "messages", "held", "changed"],
                          "missing_vote_rows": invalid, "new_api_calls": 0}))
        return
    Handler.store = store
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"PARIA replay: http://127.0.0.1:{args.port} | 300 recorded runs | no API calls", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
