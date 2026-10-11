"""Sensitivity checks on the reproduced meta-analysis.

1. Reproduces the earlier "removing HR > 1" analysis to show what it does:
   dropping every study whose point estimate is above 1 removes all unfavourable
   evidence, so the pooled result can only move towards benefit. It is reported
   here for transparency, not as a valid analysis.
2. A pre-specifiable alternative: leave-one-out on the random-effects subtotals.
3. Hartung-Knapp-Sidik-Jonkman (HKSJ) adjustment, recommended when heterogeneity
   is high and studies are few.

Run from the repo root:  python analysis/sensitivity_checks.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from meta_analysis import pool

ROOT = Path(__file__).resolve().parents[1]
studies = pd.read_csv(ROOT / "data" / "study_level_data.csv")
# Plot 7 is excluded: the exported plot is missing one study per subgroup.
studies = studies[studies["plot"] != 7]


def hksj(y, se):
    y, se = np.asarray(y, float), np.asarray(se, float)
    k = len(y)
    if k < 2:
        return np.nan, np.nan, np.nan
    r = pool(y, se)
    w = 1 / (se**2 + r["tau2"])
    q = np.sum(w * (y - r["re_log"]) ** 2) / (k - 1)
    se_h = np.sqrt(q / np.sum(w))
    t = stats.t.ppf(0.975, k - 1)
    return np.exp(r["re_log"]), np.exp(r["re_log"] - t * se_h), np.exp(r["re_log"] + t * se_h)


rows = []
for (plot, sub), g in studies.groupby(["plot", "subgroup"], sort=False):
    full = pool(g["log_hr"], g["se"])
    kept = g[g["log_hr"] <= 0]
    rem = pool(kept["log_hr"], kept["se"]) if len(kept) else None
    h = hksj(g["log_hr"], g["se"])
    loo = []
    for i in range(len(g)):
        if len(g) > 2:
            r = pool(g["log_hr"].drop(g.index[i]), g["se"].drop(g.index[i]))
            loo.append(r["re_hr"])
    rows.append({
        "plot": plot, "outcome": g["outcome"].iat[0], "subgroup": sub, "k": len(g),
        "re_hr_ci": f"{full['re_hr']:.2f} ({full['re_low']:.2f}-{full['re_high']:.2f})",
        "i2_pct": round(full["i2_pct"]),
        "hksj_ci": f"{h[0]:.2f} ({h[1]:.2f}-{h[2]:.2f})" if not np.isnan(h[0]) else "",
        "leave_one_out_range": f"{min(loo):.2f}-{max(loo):.2f}" if loo else "k<3",
        "studies_dropped_if_hr_gt_1": len(g) - len(kept),
        "removing_hr_gt_1_ci": (f"{rem['re_hr']:.2f} ({rem['re_low']:.2f}-{rem['re_high']:.2f})"
                                if rem else "no studies left"),
    })

out = pd.DataFrame(rows)
out.to_csv(ROOT / "results" / "sensitivity_checks.csv", index=False)
print(out.to_string(index=False))
