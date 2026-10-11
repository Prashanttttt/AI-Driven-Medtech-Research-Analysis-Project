"""Draw the figures in /figures from the reproduced data.

Run from the repo root:  python analysis/make_figures.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd

from meta_analysis import pool

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE = "#2a78d6", "#eb6834"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "text.color": INK,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
    "ytick.color": INK, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
})

studies = pd.read_csv(ROOT / "data" / "study_level_data.csv")
TITLES = {
    1: "All-cause mortality by NYHA class", 2: "Hospitalisation by NYHA class",
    3: "All-cause mortality by LVEF", 4: "Hospitalisation by LVEF",
    5: "All-cause mortality by sex", 6: "Hospitalisation by sex",
    8: "Hospitalisation by age",
}


def forest(plot):
    g = studies[studies["plot"] == plot]
    rows = []  # (label, hr, lo, hi, kind)
    for sub, sg in g.groupby("subgroup", sort=False):
        rows.append((sub, None, None, None, "head"))
        for _, r in sg.iterrows():
            rows.append((f"   {r.study}", np.exp(r.log_hr), np.exp(r.log_hr - 1.96 * r.se),
                         np.exp(r.log_hr + 1.96 * r.se), "study"))
        p = pool(sg["log_hr"], sg["se"])
        rows.append((f"   Subtotal (I² = {p['i2_pct']:.0f}%)", p["re_hr"], p["re_low"],
                     p["re_high"], "pool"))
    n = len(rows)
    fig, ax = plt.subplots(figsize=(9, 0.32 * n + 1.4))
    for i, (lab, hr, lo, hi, kind) in enumerate(rows):
        y = n - i
        weight = "bold" if kind in ("head", "pool") else "normal"
        x0 = -0.52 if kind == "head" else -0.49
        ax.text(x0, y, lab.strip(), transform=ax.get_yaxis_transform(), ha="left",
                va="center", fontweight=weight, fontsize=9.5)
        if kind == "study":
            ax.plot([lo, hi], [y, y], color=MUTED, lw=1.2)
            ax.plot(hr, y, "s", color=MUTED, ms=5)
            txt = f"{hr:.2f} ({lo:.2f}–{hi:.2f})"
        elif kind == "pool":
            d = np.array([[lo, y], [hr, y + 0.28], [hi, y], [hr, y - 0.28]])
            ax.fill(d[:, 0], d[:, 1], color=BLUE)
            txt = f"{hr:.2f} ({lo:.2f}–{hi:.2f})"
        else:
            txt = ""
        ax.text(1.02, y, txt, transform=ax.get_yaxis_transform(), ha="left",
                va="center", fontsize=9, fontweight=weight, color=INK)
    ax.axvline(1, color=INK, lw=1)
    ax.set_xscale("log")
    ax.set_xlim(0.1, 10)
    ax.set_xticks([0.1, 0.25, 0.5, 1, 2, 4, 10])
    ax.set_xticklabels(["0.1", "0.25", "0.5", "1", "2", "4", "10"])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_ylim(0.3, n + 0.8)
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("Hazard ratio, random effects (log scale)\n← favours device      favours control →",
                  color=MUTED)
    ax.set_title(f"{TITLES[plot]} — original analysis Plot {plot}",
                 loc="left", fontweight="bold", pad=12, x=-0.52)
    fig.subplots_adjust(left=0.36, right=0.80, top=1 - 0.6 / (0.32 * n + 1.4),
                        bottom=1.0 / (0.32 * n + 1.4))
    fig.savefig(FIG / f"forest_plot{plot}.png", dpi=160)
    plt.close(fig)


def claim_vs_reanalysis():
    s = pd.read_csv(ROOT / "results" / "sensitivity_checks.csv")
    parse = s["re_hr_ci"].str.extract(r"([\d.]+) \(([\d.]+)-([\d.]+)\)").astype(float)
    rem = s["removing_hr_gt_1_ci"].str.extract(r"([\d.]+) \(([\d.]+)-([\d.]+)\)").astype(float)
    labels = [f"{'Mortality' if o == 'mortality' else 'Hospitalisation'}: {g}"
              for o, g in zip(s["outcome"], s["subgroup"])]
    n = len(s)
    fig, ax = plt.subplots(figsize=(9, 0.42 * n + 1.8))
    for i in range(n):
        y = n - i
        ax.plot(parse.iloc[i, 1:3], [y + 0.13] * 2, color=BLUE, lw=2)
        ax.plot(parse.iloc[i, 0], y + 0.13, "o", color=BLUE, ms=8,
                mec=SURFACE, mew=1.5)
        ax.plot(rem.iloc[i, 1:3], [y - 0.13] * 2, color=ORANGE, lw=2)
        ax.plot(rem.iloc[i, 0], y - 0.13, "D", color=ORANGE, ms=7, mec=SURFACE, mew=1.5)
    ax.axvline(1, color=INK, lw=1)
    ax.set_xscale("log")
    ax.set_xlim(0.2, 2.6)
    ax.set_xticks([0.25, 0.5, 0.75, 1, 1.5, 2.5])
    ax.set_xticklabels(["0.25", "0.5", "0.75", "1", "1.5", "2.5"])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_yticks(range(n, 0, -1))
    ax.set_yticklabels(labels)
    ax.set_ylim(0.4, n + 0.6)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_xlabel("Pooled hazard ratio with 95% CI (log scale)\n← favours device      favours control →",
                  color=MUTED)
    ax.plot([], [], "o-", color=BLUE, label="Primary analysis: all studies, random effects")
    ax.plot([], [], "D-", color=ORANGE, label="After removing every study with HR > 1")
    ax.legend(loc="upper center", bbox_to_anchor=(0.35, -0.11), ncol=1, frameon=False)
    fig.suptitle("Removing unfavourable studies turns null results into apparent benefit",
                 x=0.02, ha="left", fontweight="bold", y=0.985)
    fig.subplots_adjust(left=0.33, right=0.97, top=0.93, bottom=0.2)
    fig.savefig(FIG / "primary_vs_removing_hr_gt_1.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    for p in TITLES:
        forest(p)
    claim_vs_reanalysis()
    print("Figures written to", FIG)
