# Quality control report

**Bottom line:** the original RevMan analysis reproduces exactly in Python, but quality control changed its conclusions. Under the primary analysis (random effects, all included studies), no NYHA or LVEF subgroup shows a statistically significant reduction in mortality or hospitalisation. The benefits in the earlier write-up came from a sensitivity analysis that removed every study with a hazard ratio above 1, which has been dropped.

All numbers below can be regenerated with `python analysis/meta_analysis.py` and `python analysis/sensitivity_checks.py`.

## 1. What reproduces

| Check | Result |
| --- | --- |
| Study rows transcribed from the 8 RevMan forest plots | 76 |
| Rows where exp(log HR ± 1.96 SE) matches RevMan's printed HR and CI | 76 / 76 |
| Pooled subgroup and total results matching RevMan (HR and 95% CI, ±0.01) | 22 / 25 |
| I² matching RevMan (±1 point) | 23 / 25 |
| Fixed-effect results matching the earlier sensitivity table (e.g. LVEF <35% hospitalisation 1.29 [1.25–1.32]) | Yes |

The three mismatches are all in Plot 7 (age, mortality). RevMan reports 4 studies under age <70 and 7 under age >70 (df = 3 and 6), but the image shows 3 and 6 rows. One row per subgroup is hidden in the screenshot, so Plot 7 cannot be rebuilt without the original RevMan file. It is excluded from all re-analysis here.

## 2. The main problem: the "removing HR > 1" analysis

The earlier sensitivity analysis removed every study with HR > 1. The headline numbers in the earlier write-up came from this analysis, not from the primary analysis:

| Earlier headline result | Primary analysis (random effects, all studies) | After removing all studies with HR > 1 |
| --- | --- | --- |
| LVEF <35%, mortality | 1.16 (0.72–1.87), 3 of 5 studies dropped | 0.65 (0.57–0.75) |
| LVEF <35%, hospitalisation | 1.09 (0.92–1.29), 3 of 5 dropped | 0.77 (0.69–0.86) |
| LVEF >35%, mortality | 0.67 (0.40–1.13) | 0.56 (0.39–0.80) |
| LVEF >35%, hospitalisation | 0.68 (0.38–1.21) | 0.50 (0.25–1.01) |

Removing studies because their result is unfavourable guarantees a favourable pooled result. It is selection on the outcome, not a sensitivity analysis. Valid alternatives are pre-specified: leave-one-out, excluding high risk-of-bias studies, or restricting to RCTs. Leave-one-out results are in `results/sensitivity_checks.csv`; no single study removal makes the LVEF <35% subgroups favour the device.

## 3. Corrections to the earlier write-up

| Section | Earlier text | Corrected (from the forest plot) |
| --- | --- | --- |
| Results, NYHA II mortality | Significant; CI excludes 1, P < 0.05 | 0.74 (0.48–1.13), P = 0.17: not significant |
| Results, NYHA III mortality | HR 1.14 is a "14% reduction" | A 14% increase (not significant) |
| Results, NYHA IV mortality | I² = 14% | I² = 97% |
| Results, NYHA overall mortality | 0.97 (0.78–1.05) | 0.97 (0.74–1.28) |
| Results, male mortality | 1.15 (0.76–1.45) | 1.05 (0.76–1.45) |
| Results, LVEF conclusion | Devices "significantly" reduce mortality and hospitalisation in LVEF <35% | 1.16 (0.72–1.87) and 1.09 (0.92–1.29): neither significant, both point towards harm |
| Summary, women | "Significant benefits" with HR 1.17 and 1.09 | HR > 1 means worse outcomes; these are fixed-effect values |
| Heterogeneity section | LVEF <35% I² = 0% (hospitalisation) and 24% (mortality), described as "reliable" | 96% and 98% in the primary analysis; 0% and 24% are the values after removing studies with HR > 1 |
| Summary | 50 studies included | 28 distinct study labels visible across the 8 main plots (Plot 7 hides up to 2 more) |
| Methods | Studies without reduced EF (LVEF ≥35%) excluded | An LVEF >35% subgroup is analysed |

## 4. Data issues to check against the source papers

**Studies counted more than once in "Total" rows.** Every plot pools all subgroups into a total, but the same study appears in several subgroups of one plot (e.g. Kronborg 2014 and Lindeberg 2022 each appear three times in Plot 1). This double-counts patients, so the "Total" estimates and their CIs are not valid. Only subgroup results are reported in the re-analysis.

**Identical estimates in different places.** Five pairs share the same log HR *and* SE, which is unlikely unless a value was copied:

| First entry | Second entry |
| --- | --- |
| Tang 2010, NYHA II mortality | Cleland 2022, NYHA III mortality |
| Shivakumar 2023, NYHA IV mortality | Mmalekrah 2023, female mortality |
| Zhang 2015, LVEF >35% mortality | Zhang 2015, LVEF >35% hospitalisation |
| Epstein 2012, NYHA II mortality | Epstein 2012, NYHA I/II hospitalisation |
| Cleland 2022, LVEF <35% hospitalisation | Cleland 2022, age >70 hospitalisation |

**Effect direction.** 19 study rows show a statistically significant *increase* in risk with the device (e.g. Lindeberg 2022 NYHA IV mortality HR 2.69 [2.26–3.20]). That conflicts with the established trial evidence for CRT and ICD. Each should be checked for: a reversed comparison (control vs device), a comparison that is not device vs drug therapy (e.g. a prognostic association with LVEF), or an outcome other than all-cause mortality or hospitalisation.

**A modelling study included as a primary study.** Mealing 2016 appears in the NYHA II and IV mortality analyses, but it is a cost-effectiveness model built on individual patient data from 13 RCTs ([Mealing et al., Heart 2016](https://eprints.whiterose.ac.uk/id/eprint/100095/)). It is not a primary outcome study, and its data overlap with the trials it models.

**Missing landmark trials.** The introduction cites COMPANION and CARE-HF, but neither appears by name in the forest plots. Nor do MADIT-II, SCD-HeFT, MADIT-CRT, RAFT or DANISH. A review of CRT/ICD vs drug therapy in HFrEF would normally include them.

**Heterogeneity.** I² is 84–98% in 13 of 15 reproducible subgroups. Pooling CRT with ICD, and RCTs with observational studies, in one analysis is a likely cause. Separate analyses by device type and design would be more interpretable.

## 5. The earlier workbook

The earlier `HeartFailure_Device_MetaAnalysis.xlsx` (now in `archive/`) did not match the RevMan analysis:

- **Study Data sheet:** 12 studies with log HRs that mostly differ from the forest plots, each tagged as a single age, LVEF, NYHA and gender category. There are no standard errors, so nothing can be pooled from it.
- **Mortality Results sheet:** mixes values from different analyses (e.g. female mortality 1.12 [1.05–1.21] does not appear in any plot; NYHA IV 1.38 [1.02–1.86] does not match the plot's 1.07 [0.53–2.12]).
- **Earlier README headline:** "benefit concentrates in NYHA III/IV and LVEF <35%" is not supported by the forest plots, and the workbook's own "severe HF" mortality estimate is 1.17 (1.09–1.25), which favours control.

The workbook is kept in `archive/` for transparency and replaced by `results/`.

## 6. What the evidence in this dataset supports

| Outcome | Subgroup | Random-effects HR (95% CI) | I² | Robust? |
| --- | --- | --- | --- | --- |
| Hospitalisation | Age >70 | 0.80 (0.73–0.88) | 0% | Yes: holds under HKSJ and leave-one-out (3 studies) |
| Hospitalisation | Male | 0.71 (0.60–0.84) | 0% | Fragile: 2 studies, one carrying 99% of the weight; HKSJ 0.50–1.01 |
| Mortality | Age <70 | 0.77 (0.68–0.88) as reported | 0% | Cannot verify: Plot 7 incomplete |
| All other subgroups | — | CI crosses 1 | 84–98% | No significant effect |

**Conclusion so far:** as assembled, this dataset does not show a consistent mortality or hospitalisation benefit for CRT/ICD in any LVEF or NYHA subgroup, and its heterogeneity is too high for pooled estimates to be meaningful. That conflicts with the large RCT evidence base: an individual patient data network meta-analysis of 13 RCTs (12,638 patients) found mortality reductions of 42% with CRT-D, 29% with ICD and 28% with CRT-P ([Woods et al., Heart 2015](https://researchonline.lshtm.ac.uk/id/eprint/2274449)). The gap points to problems in study selection and data extraction rather than to device harm. The next phase, now under way, is to re-extract each study from source, restrict to device-vs-control comparisons, and analyse CRT and ICD separately.
