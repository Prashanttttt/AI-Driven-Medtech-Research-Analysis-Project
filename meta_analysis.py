"""Reproduce the original RevMan meta-analysis from study-level data.

Method matches RevMan's generic inverse-variance analysis:
- Fixed effect: inverse-variance weights 1/SE^2 on log hazard ratios
- Random effects: DerSimonian-Laird estimate of tau^2
- Heterogeneity: Cochran's Q, I^2 = max(0, (Q - df) / Q)
- "Total" pools every row in a forest plot, as RevMan does

Run from the repo root:  python analysis/meta_analysis.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"


def pool(y, se):
    """Return fixed- and random-effects pooled estimates for log HRs."""
    y, se = np.asarray(y, float), np.asarray(se, float)
    k = len(y)
    w = 1 / se**2
    fe = np.sum(w * y) / np.sum(w)
    fe_se = np.sqrt(1 / np.sum(w))
    q = float(np.sum(w * (y - fe) ** 2))
    df = k - 1
    c = np.sum(w) - np.sum(w**2) / np.sum(w)
    tau2 = max(0.0, (q - df) / c) if df > 0 else 0.0
    wr = 1 / (se**2 + tau2)
    re = np.sum(wr * y) / np.sum(wr)
    re_se = np.sqrt(1 / np.sum(wr))
    i2 = max(0.0, (q - df) / q) * 100 if q > 0 else 0.0
    z = re / re_se
    return {
        "k": k,
        "re_hr": np.exp(re),
        "re_low": np.exp(re - 1.96 * re_se),
        "re_high": np.exp(re + 1.96 * re_se),
        "re_log": re,
        "re_se": re_se,
        "z": abs(z),
        "p": 2 * stats.norm.sf(abs(z)),
        "fe_hr": np.exp(fe),
        "fe_low": np.exp(fe - 1.96 * fe_se),
        "fe_high": np.exp(fe + 1.96 * fe_se),
        "tau2": tau2,
        "chi2": q,
        "df": df,
        "i2_pct": i2,
        "weights_pct": wr / wr.sum() * 100,
    }


def subgroup_test(parts):
    """Test for subgroup differences between random-effects subtotals."""
    y = np.array([p["re_log"] for p in parts])
    w = 1 / np.array([p["re_se"] for p in parts]) ** 2
    mean = np.sum(w * y) / np.sum(w)
    q = float(np.sum(w * (y - mean) ** 2))
    df = len(parts) - 1
    return q, df, stats.chi2.sf(q, df)


def main():
    studies = pd.read_csv(DATA / "study_level_data.csv")
    revman = pd.read_csv(DATA / "revman_reported_results.csv")

    # 1. Check each transcribed row: does exp(logHR +/- 1.96 SE) match the CI RevMan printed?
    ci = studies["revman_hr_ci"].str.extract(r"([\d.]+) \[([\d.]+); ([\d.]+)\]").astype(float)
    studies["calc_hr"] = np.exp(studies["log_hr"]).round(2)
    studies["calc_low"] = np.exp(studies["log_hr"] - 1.96 * studies["se"]).round(2)
    studies["calc_high"] = np.exp(studies["log_hr"] + 1.96 * studies["se"]).round(2)
    studies["row_matches_revman"] = (
        (abs(studies["calc_hr"] - ci[0]) <= 0.011)
        & (abs(studies["calc_low"] - ci[1]) <= 0.011)
        & (abs(studies["calc_high"] - ci[2]) <= 0.011)
    )

    # 2. Re-pool every subgroup and total
    rows, subgroup_tests = [], []
    for plot, g in studies.groupby("plot", sort=True):
        parts = []
        for sub, sg in g.groupby("subgroup", sort=False):
            r = pool(sg["log_hr"], sg["se"])
            parts.append(r)
            rows.append({"plot": plot, "outcome": sg["outcome"].iat[0],
                         "subgroup_variable": sg["subgroup_variable"].iat[0],
                         "subgroup": sub, **{k: v for k, v in r.items() if k != "weights_pct"}})
        r = pool(g["log_hr"], g["se"])
        rows.append({"plot": plot, "outcome": g["outcome"].iat[0],
                     "subgroup_variable": g["subgroup_variable"].iat[0],
                     "subgroup": "Total", **{k: v for k, v in r.items() if k != "weights_pct"}})
        q, df, p = subgroup_test(parts)
        subgroup_tests.append({"plot": plot, "chi2": q, "df": df, "p": p})

    res = pd.DataFrame(rows)

    # 3. Compare with RevMan
    m = res.merge(revman, on=["plot", "outcome", "subgroup_variable", "subgroup"],
                  suffixes=("", "_revman"))
    m["hr_match"] = (abs(m["re_hr"].round(2) - m["hr"]) <= 0.011) \
        & (abs(m["re_low"].round(2) - m["ci_low"]) <= 0.011) \
        & (abs(m["re_high"].round(2) - m["ci_high"]) <= 0.011)
    m["i2_match"] = abs(m["i2_pct"].round(0) - m["i2_pct_revman"]) <= 1
    m["chi2_match"] = abs(m["chi2"] - m["chi2_revman"]) <= 0.5

    RESULTS.mkdir(exist_ok=True)
    out = res.copy()
    for c in ["re_hr", "re_low", "re_high", "fe_hr", "fe_low", "fe_high"]:
        out[c] = out[c].round(2)
    out[["tau2", "chi2", "z"]] = out[["tau2", "chi2", "z"]].round(2)
    out["i2_pct"] = out["i2_pct"].round(0)
    out["p"] = out["p"].map(lambda v: f"{v:.4f}")
    out.drop(columns=["re_log", "re_se"]).to_csv(RESULTS / "pooled_results.csv", index=False)

    ver = m[["plot", "outcome", "subgroup", "k", "df_revman", "re_hr", "re_low", "re_high",
             "hr", "ci_low", "ci_high", "i2_pct", "i2_pct_revman", "chi2", "chi2_revman",
             "hr_match", "i2_match", "chi2_match"]].copy()
    ver.columns = ["plot", "outcome", "subgroup", "k_transcribed", "df_revman",
                   "hr_python", "low_python", "high_python", "hr_revman", "low_revman",
                   "high_revman", "i2_python", "i2_revman", "chi2_python", "chi2_revman",
                   "hr_match", "i2_match", "chi2_match"]
    for c in ["hr_python", "low_python", "high_python"]:
        ver[c] = ver[c].round(2)
    ver[["i2_python", "chi2_python"]] = ver[["i2_python", "chi2_python"]].round(1)
    ver.to_csv(RESULTS / "verification_vs_revman.csv", index=False)
    studies.to_csv(RESULTS / "study_rows_checked.csv", index=False)
    pd.DataFrame(subgroup_tests).round(4).to_csv(RESULTS / "subgroup_difference_tests.csv",
                                                  index=False)

    print(f"Study rows matching RevMan's printed HR and CI: "
          f"{studies['row_matches_revman'].sum()} / {len(studies)}")
    print(f"Pooled results matching RevMan (HR and CI): {m['hr_match'].sum()} / {len(m)}")
    print(f"I2 matching (within 1 point): {m['i2_match'].sum()} / {len(m)}")
    bad = ver[~(ver.hr_match & ver.i2_match)]
    if len(bad):
        print("\nMismatches:")
        print(bad.to_string(index=False))


if __name__ == "__main__":
    main()
