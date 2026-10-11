# Device-Based Therapies in Heart Failure: Evidence Synthesis and European Market Access

**An ongoing project on cardiac resynchronisation therapy (CRT) and implantable cardioverter-defibrillators (ICD) versus drug therapy in heart failure with reduced ejection fraction (HFrEF): a reproducible Python meta-analysis pipeline, quality-controlled evidence, and a review of how European payers assess these devices.**

The study-level data comes from my earlier systematic review and meta-analysis, originally run in RevMan (searches to August 2024). This project moves that work into a reproducible, version-controlled pipeline, tests its robustness, and connects the clinical evidence to market access.

## Project status

| Workstream | Status |
| --- | --- |
| Reproducible Python pipeline, verified against RevMan | Done |
| Quality control of data and sensitivity analyses | Done |
| European reimbursement and HTA review (EU4 + UK) | Done |
| Value story for European payers | Done |
| Re-extraction of each study from source, CRT and ICD analysed separately | In progress |
| QRS duration and LBBB subgroups, to match payer criteria | Planned |

## Key findings so far

1. **The pipeline is verified.** All 76 study rows and all 22 pooled results on the seven complete forest plots reproduce RevMan's output to two decimal places.
2. **Quality control changed the conclusions.** An earlier sensitivity analysis removed every study with HR > 1, which suggested strong benefits (for example LVEF <35% mortality HR 0.65). The primary random-effects analysis gives 1.16 (0.72–1.87) for the same subgroup, so that approach was dropped.
3. **No NYHA or LVEF subgroup shows a significant effect** in the primary analysis, and heterogeneity is very high (I² 84–98% in 13 of 15 subgroups). This conflicts with the large RCT evidence base and points to study selection and extraction issues, now being fixed. Details are in the [quality control report](quality_control/QUALITY_CONTROL.md).
4. **The one robust signal** is fewer hospitalisations in patients over 70: HR 0.80 (0.73–0.88), I² 0%.

![Primary analysis vs removing studies with HR > 1](figures/primary_vs_removing_hr_gt_1.png)

## European market access

Every pathway reviewed (NICE in England, HAS in France, the German DRG and quality assurance system, Italy and Spain) restricts devices to LVEF ≤35% and chooses between ICD, CRT-P and CRT-D by QRS duration and LBBB. That is why the next phase adds QRS and LBBB subgroups. See [European access](market_access/EUROPEAN_ACCESS.md) and the [value story](market_access/VALUE_STORY.md).

## Repository structure

| Path | Contents |
| --- | --- |
| `data/study_level_data.csv` | 76 study rows from the original RevMan analysis |
| `data/revman_reported_results.csv` | RevMan's pooled results, used to verify the pipeline |
| `analysis/meta_analysis.py` | Random-effects (DerSimonian-Laird) and fixed-effect pooling, with verification against RevMan |
| `analysis/sensitivity_checks.py` | Leave-one-out, Hartung-Knapp-Sidik-Jonkman, and the "removing HR > 1" comparison |
| `analysis/make_figures.py` | Forest plots and summary chart |
| `results/` | Pooled results, verification table, sensitivity checks |
| `figures/` | Forest plots for each analysis |
| `quality_control/QUALITY_CONTROL.md` | Data and analysis issues found, with the value each was checked against |
| `market_access/` | European reimbursement and HTA review, and value story |
| `ai_validation/AI_METHOD.md` | How AI was used, how each output was verified, and the prompts |
| `archive/` | Earlier version of the project, kept for transparency |

## Run it

```bash
pip install -r requirements.txt
python analysis/meta_analysis.py
python analysis/sensitivity_checks.py
python analysis/make_figures.py
```

## Forest plots

<details>
<summary>All forest plots</summary>

![Mortality by NYHA class](figures/forest_plot1.png)
![Hospitalisation by NYHA class](figures/forest_plot2.png)
![Mortality by LVEF](figures/forest_plot3.png)
![Hospitalisation by LVEF](figures/forest_plot4.png)
![Mortality by sex](figures/forest_plot5.png)
![Hospitalisation by sex](figures/forest_plot6.png)
![Hospitalisation by age](figures/forest_plot8.png)

Mortality by age (Plot 7) is not yet included: one study per subgroup is missing from the exported data.

</details>

## Limitations

The study-level data is as extracted in the original analysis and is being re-checked against the source papers. Pooled "total" rows are not reported because some studies contribute to more than one subgroup. Reimbursement details were researched in October 2026 and may change.
