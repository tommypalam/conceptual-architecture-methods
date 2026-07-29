"""
score_engine.py — bare-bones scorer for engine output records.

Reads the write-once records under experiments/phase2_simple/ and
experiments/phase2_complex/ and writes tidy scored summaries (per-config
decision rates + Wilson 95% CIs). Point estimates only; the mixed-effects
model and bootstrap (spec §9.1–9.2) are later work.

Examples
--------
python code/score_engine.py --simple experiments/phase2_simple
python code/score_engine.py --complex experiments/phase2_complex
python code/score_engine.py --simple <dir> --complex <dir> --out results.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import scoring


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--simple", type=Path, help="Simple-problem runs root.")
    p.add_argument("--complex", type=Path, help="Complex-problem runs root.")
    p.add_argument("--out", type=Path, help="Write combined JSON summary here.")
    args = p.parse_args()

    result = {}
    if args.simple:
        result["simple"] = scoring.score_simple(args.simple)
    if args.complex:
        result["complex"] = scoring.score_complex(args.complex)
    if not result:
        p.error("pass --simple and/or --complex")

    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
