"""Figures for the paper, drawn from paper_item_robustness.json. Zero API calls."""
import json, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("paper_item_robustness.json")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("figures")
OUT.mkdir(exist_ok=True)
C = json.load(open(SRC))["contrasts"]

BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#dcdad4"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": MUTED,
                     "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": INK,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.spines.left": False, "pdf.fonttype": 42})

# ---------- Figure 1: forest plot ----------
groups = [
    ("Field and position controls (§5)", [
        ("pd_prospective_r1:PD", "Pin the field (0.1 vs 0.9)"),
        ("label_semantics_r1:SWAP", "Same numeral on the partner field"),
        ("label_semantics_r1:TRUE-SWAP", "Field minus partner (difference)"),
        ("position_counterbalance_r1:D", "Partner field at the field's line"),
        ("position_counterbalance_r1:C", "Field moved to the partner's line"),
        ("parameter_followup:AW", "Partner field pinned alone (80 agents)"),
    ]),
    ("Name and definition controls (§6)", [
        ("semantics_r1:CANON", "CANON  name + definition"),
        ("semantics_r1:NONCE", "NONCE  definition, name replaced"),
        ("semantics_r1:FLIP", "FLIP  same name, ends of definition exchanged"),
        ("semantics_r1:INVERT", "INVERT  renamed and exchanged"),
        ("semantics_r1:CANON-FLIP", "CANON minus FLIP (difference)"),
    ]),
    ("Invented fields in the partner slot (§6.2)", [
        ("probe_fields_r1:SQ", "Status-quo Preference (predicted +)"),
        ("probe_fields_r1:SW", "Stated-Wish Deference (predicted +)"),
        ("probe_fields_r1:WO", "Worst-off Priority (predicted +)"),
        ("probe_fields_r1:NC", "Numbers Count (predicted −)"),
    ]),
]
rows, y, ticks, labels, heads = [], 0, [], [], []
for title, items in groups:
    heads.append((y, title)); y += 1
    for key, lab in items:
        rows.append((y, key)); ticks.append(y); labels.append(lab); y += 1
    y += 0.4
fig, ax = plt.subplots(figsize=(6.3, 5.4))
for yy, key in rows:
    c = C[key]
    ax.plot(c["crossed_ci"], [yy, yy], color=MUTED, lw=1, solid_capstyle="butt", zorder=1)
    ax.plot(c["unit_ci"], [yy, yy], color=BLUE, lw=3.2, solid_capstyle="round", zorder=2)
    ax.plot([c["estimate"]], [yy], "o", ms=5.5, color=BLUE, mec="white", mew=1.2, zorder=3)
    ax.text(0.86, yy, f"{c['estimate']:+.3f}".replace("-", "\u2212"), va="center", ha="left", color=INK, fontsize=8)
for yy, title in heads:
    ax.text(-0.88, yy, title, va="center", ha="left", fontweight="bold", color=INK, fontsize=8.5)
ax.axvline(0, color=MUTED, lw=0.8, zorder=0)
ax.set_yticks(ticks); ax.set_yticklabels(labels)
ax.tick_params(axis="y", length=0)
ax.set_ylim(y - 0.2, -0.8)
ax.set_xlim(-0.88, 0.98)
ax.set_xticks([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8])
ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.set_xlabel("Effect or difference in effects (keep-rate)")
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([], [], color=BLUE, lw=3.2, marker="o", ms=5, mec="white", label="estimate and 95% CI (agent-item units)"),
                   Line2D([], [], color=MUTED, lw=1, label="95% CI (agents and items resampled)")],
          loc="lower center", bbox_to_anchor=(0.25, 1.0), ncol=2, frameon=False, fontsize=7.5)
# y labels sit left of axis; group headers need to be in axis coords to the left
for yy, title in heads:
    pass
fig.tight_layout()
fig.savefig(OUT / "fig1_forest.pdf"); fig.savefig(OUT / "fig1_forest.png", dpi=200)

# ---------- Figure 2: per-item consistency ----------
order = ["desk_booking", "meeting_room", "on_call", "rest_break", "storage_unit", "tool_library", "weekend_rota"]
fig, axes = plt.subplots(1, 2, figsize=(6.3, 3.0), sharey=True)
axes[0].invert_yaxis()
def panel(ax, a, b, la, lb, title):
    A, Bv = C[a]["per_item"], C[b]["per_item"]
    for i, t in enumerate(order):
        ax.plot([A[t], Bv[t]], [i, i], color=GRID, lw=1.6, zorder=1)
        ax.plot(A[t], i, "o", color=BLUE, ms=6, mec="white", mew=1.2, zorder=2)
        ax.plot(Bv[t], i, "o", color=ORANGE, ms=6, mec="white", mew=1.2, zorder=2)
    ax.axvline(0, color=MUTED, lw=0.8, zorder=0)
    ax.set_yticks(range(len(order))); ax.set_yticklabels([t.replace("_", " ") for t in order])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(-0.95, 0.95); ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.set_title(title, fontsize=8.5, loc="left", color=INK, fontweight="bold", pad=18)
    ax.legend(handles=[Line2D([], [], ls="", marker="o", color=BLUE, label=la),
                       Line2D([], [], ls="", marker="o", color=ORANGE, label=lb)],
              loc="lower left", bbox_to_anchor=(-0.02, 0.99), ncol=2, frameon=False, fontsize=7.5, handletextpad=0.2)
panel(axes[0], "semantics_r1:CANON", "semantics_r1:FLIP", "CANON", "FLIP", "a  Exchanging the definition's ends")
panel(axes[1], "probe_fields_r1:SQ", "probe_fields_r1:NC", "Status-quo Preference", "Numbers Count", "b  Two invented fields, same slot")
fig.supxlabel("Change in keep-rate, 0.9 minus 0.1, per item (40 agents each)", fontsize=8, color=INK)
fig.tight_layout()
fig.savefig(OUT / "fig2_items.pdf"); fig.savefig(OUT / "fig2_items.png", dpi=200)
print("ok")
