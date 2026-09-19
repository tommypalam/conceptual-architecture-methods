"""Figures for the thesis, drawn from the frozen record. Zero API calls.

Every number plotted is read from a designation's checksum-verified
`all_rows.json` (arm rates) or from `thesis_intervals.json` (paired effects and
bootstrap intervals, produced by `phase6_thesis_intervals.py`). Nothing is typed
in by hand. Outputs go to docs/figures/ as PDF (for the LaTeX build) and PNG.
"""
from __future__ import annotations

import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Patch
import numpy as np

from phase3_budget import read_checked
from phase3_recognition_run import ROOT

import phase4b_gpt_pool as GPTPOOL
import phase4b_profiled_pool as PROF

R = ROOT / "experiments"
OUT = ROOT / "docs" / "figures"
INTERVALS = json.loads((R / "phase5_analysis/thesis_intervals.json").read_text(encoding="utf-8"))["results"]
BY = {r["name"]: r for r in INTERVALS}

INK = "#1f2933"
PD = "#1b4f72"      # the parameter under test
INERT = "#9aa5b1"   # the inert partner / not load-bearing
ACCENT = "#b3541e"  # highlight
GRID = "#d9dee3"

serif = [f.name for f in font_manager.fontManager.ttflist if "Palatino" in f.name]
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": (["Palatino Linotype"] if serif else []) + ["DejaVu Serif"],
    "font.size": 9, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "axes.spines.top": False,
    "axes.spines.right": False, "axes.linewidth": 0.6, "xtick.major.width": 0.6,
    "ytick.major.width": 0.6, "pdf.fonttype": 42,
})


def arm_rates(path, pool, arms):
    rows = read_checked(R / path)
    out = {}
    for a in arms:
        ys = [1.0 if pool.primary_net(r["task"], r["choice"]) == "good" else 0.0
              for r in rows if r.get("arm") == a and r.get("choice")]
        out[a] = (float(np.mean(ys)), len(ys))
    return out


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", dpi=220)
    plt.close(fig)


def fig_egu():
    gpt = arm_rates("phase4_coding/phase4b_gpt_r2/all_rows.json", GPTPOOL, ["U", "G", "E"])
    hk = arm_rates("phase4_coding/phase4b_profiled_r1/all_rows.json", PROF, ["U", "G", "E"])
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    labels = ["no profile (U)", "ethical instruction (G)", "numeric profile (E)"]
    cols = [INERT, INERT, PD]
    x = np.arange(3)
    w = 0.36
    for i, (d, off) in enumerate([(gpt, -w / 2 - 0.02), (hk, w / 2 + 0.02)]):
        vals = [d[a][0] for a in ["U", "G", "E"]]
        bars = ax.bar(x + off, vals, w, color=cols, edgecolor="white", linewidth=1,
                      hatch=None if i == 0 else "////", alpha=1.0 if i == 0 else 0.85)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.012, f"{v:.2f}", ha="center",
                    va="bottom", fontsize=7.5, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("share classifying good")
    ax.yaxis.grid(True, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)
    eg_g = BY["E vs G (gpt)"]
    eg_h = BY["E vs G (haiku)"]
    ax.text(0.01, 0.97,
            f"paired E−G: gpt +{eg_g['effect']:.3f} [{eg_g['ci95'][0]:+.3f}, {eg_g['ci95'][1]:+.3f}]\n"
            f"                    haiku +{eg_h['effect']:.3f} [{eg_h['ci95'][0]:+.3f}, {eg_h['ci95'][1]:+.3f}]",
            transform=ax.transAxes, va="top", fontsize=7.5, color=INK)
    ax.legend(handles=[Patch(facecolor=INERT, label="gpt-5.4-mini"),
                       Patch(facecolor=INERT, hatch="////", alpha=0.85, label="claude-haiku-4-5")],
              loc="upper right", frameon=False, fontsize=7.5)
    save(fig, "fig1_profile_vs_instruction")


def effect_plot(ax, names, ylabels, colors):
    ys = np.arange(len(names))[::-1]
    for y, n, c in zip(ys, names, colors):
        r = BY[n]
        lo, hi = r["ci95"]
        clo, chi = r["cluster_ci95"]
        ax.plot([clo, chi], [y, y], color=c, linewidth=0.7, alpha=0.6, solid_capstyle="butt")
        ax.plot([lo, hi], [y, y], color=c, linewidth=2.2, solid_capstyle="butt")
        ax.plot(r["effect"], y, "o", color=c, markersize=5.5, markeredgecolor="white", markeredgewidth=0.8)
        ax.text(max(hi, chi) + 0.015, y, f"{r['effect']:+.3f}", va="center", fontsize=7.5, color=INK)
    ax.axvline(0, color=INK, linewidth=0.6)
    ax.set_yticks(ys)
    ax.set_yticklabels(ylabels)
    ax.xaxis.grid(True, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)
    return ys


def fig_counterbalance():
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    names = ["PD swap TRUE", "PD swap SWAP", "Counterbalance A (PD, line 6)",
             "Counterbalance C (PD, line 10)", "Counterbalance D (AW, line 6)",
             "Counterbalance B (AW, line 10)"]
    labels = ["TRUE   level on PD, line 6", "SWAP   level on AW, line 10",
              "A   level on PD, line 6", "C   level on PD, line 10",
              "D   level on AW, line 6", "B   level on AW, line 10"]
    cols = [PD, INERT, PD, PD, ACCENT, INERT]
    ys = effect_plot(ax, names, labels, cols)
    ax.axhline((ys[1] + ys[2]) / 2, color=GRID, linewidth=0.8, linestyle=(0, (3, 3)))
    ax.text(-0.19, ys[0] + 0.55, "original swap (label_semantics_r1)", fontsize=7.5, color=INK, style="italic")
    ax.text(-0.19, ys[2] + 0.62, "counterbalanced 2×2 (position_counterbalance_r1)", fontsize=7.5,
            color=INK, style="italic")
    ax.set_xlim(-0.2, 0.65)
    ax.set_ylim(-0.7, len(names) + 0.4)
    ax.set_xlabel("paired effect of the level (0.9 − 0.1) on the share classifying good")
    save(fig, "fig2_label_vs_position")


def fig_sweep():
    order = ["ID", "LL", "TfA", "MoR", "MS", "RE", "RT", "CS"]
    full = {"ID": "Internalisation Dependence", "LL": "Legitimacy Locus",
            "TfA": "Tolerance for Asymmetry", "MoR": "Mode of Response", "MS": "Moral Scope",
            "RE": "Relational Embedding", "RT": "Response Threshold", "CS": "Constraint Sensitivity"}
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    names = [f"sweep {c}" for c in order]
    cols = [PD if c == "ID" else (ACCENT if c == "LL" else INERT) for c in order]
    ax.axvspan(-0.20, 0.20, color="#f3f5f7", zorder=0)
    ax.axvspan(-0.10, 0.10, color="#e6eaee", zorder=0)
    ys = effect_plot(ax, names, [f"{c}  {full[c]}" for c in order], cols)
    ax.text(-0.199, ys[-1] - 0.5, "±0.20", fontsize=7, color=INK, ha="left", va="center")
    ax.text(-0.099, ys[-1] - 0.5, "±0.10", fontsize=7, color=INK, ha="left", va="center")
    ax.set_xlim(-0.35, 0.35)
    ax.set_ylim(-0.6, len(order) + 0.9)
    ax.set_xlabel("paired effect of pinning (0.9 − 0.1), 25 agents × 7 items")
    save(fig, "fig3_sweep_forest")


def fig_replication():
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    spec = [("PD", "PD prospective (gpt)", "gpt · prospective, 40 agents"),
            ("PD", "PD swap TRUE", "gpt · swap TRUE, 40 agents"),
            ("PD", "Counterbalance A (PD, line 6)", "gpt · counterbalance A, 40 agents"),
            ("PD", "Counterbalance C (PD, line 10)", "gpt · counterbalance C, 40 agents"),
            ("PD", "PD cross-provider (haiku)", "haiku · pinned, 40 agents"),
            ("ID", "sweep ID", "gpt · sweep, 25 agents"),
            ("ID", "ID swap TRUE", "gpt · swap TRUE, 40 agents"),
            ("ID", "ID cross-provider (haiku)", "haiku · pinned, 40 agents"),
            ("LL", "sweep LL", "gpt · sweep, 25 agents"),
            ("LL", "LL TRUE", "gpt · swap TRUE, 40 agents")]
    names = [s[1] for s in spec]
    labels = [s[2] for s in spec]
    cols = [PD if s[0] != "LL" else ACCENT for s in spec]
    ys = effect_plot(ax, names, labels, cols)
    groups = [("Procedural Dependence", 0, 5), ("Internalisation Dependence", 5, 8),
              ("Legitimacy Locus (withdrawn)", 8, 10)]
    for g, a, b in groups:
        ax.text(-0.28, ys[a] + 0.55, g, fontsize=7.5, color=INK, style="italic")
        if b < len(spec):
            ax.axhline((ys[b - 1] + ys[b]) / 2, color=GRID, linewidth=0.8, linestyle=(0, (3, 3)))
    ax.text(0.42, ys[8] + 0.05, "post-hoc r = +0.271", fontsize=7, color=ACCENT, va="center")
    ax.text(0.42, ys[4] + 0.05, "post-hoc r = +0.089", fontsize=7, color=PD, va="center")
    ax.set_xlim(-0.3, 0.65)
    ax.set_ylim(-0.7, len(spec) + 0.6)
    ax.set_xlabel("paired effect of the level (0.9 − 0.1) on the share classifying good")
    save(fig, "fig4_replication_map")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fig_egu()
    fig_counterbalance()
    fig_sweep()
    fig_replication()
    print("written:", sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
