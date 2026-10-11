# How AI was used, and how its output was checked

This project used an AI assistant (Claude) to transcribe data, write the analysis code, quality-check the earlier analysis and research European reimbursement. Every AI output was checked against an independent source before it was used.

## 1. Data extraction from forest plot images

**Task:** read 76 study rows (study, log HR, SE, weight, HR and 95% CI) from the 8 RevMan forest plot exports from the original analysis.

**How it was checked:** two independent tests, both scripted in `analysis/meta_analysis.py`.

| Check | What it tests | Result |
| --- | --- | --- |
| Internal consistency | For each row, exp(log HR ± 1.96 × SE) must equal the HR and CI that RevMan printed on the same row | 76 / 76 rows match to 2 decimal places |
| Reproduction | Re-pooling the transcribed rows must reproduce RevMan's subtotals, I² and χ² | 22 / 22 results match on the 7 complete plots |
| Completeness | The number of rows must agree with RevMan's degrees of freedom | Caught that Plot 7 hides one row per subgroup |

A transcription error in either log HR or SE would break the first check, and an error in any row would shift the pooled result in the second. Passing both is strong evidence the extraction is correct.

## 2. Analysis code

The AI wrote the DerSimonian-Laird random-effects and inverse-variance fixed-effect code. It was validated by reproducing RevMan's own output (above) and the earlier fixed-effect results (for example, LVEF <35% hospitalisation 1.29 [1.25–1.32]).

## 3. Quality control

The AI compared each statement in the earlier write-up against the reproduced numbers. Every issue listed in [`quality_control/QUALITY_CONTROL.md`](../quality_control/QUALITY_CONTROL.md) cites the plot and value it was checked against, so each can be confirmed by eye.

## 4. European reimbursement research

Every fact in [`market_access/`](../market_access) links to the public page or document it came from (NICE, NHS England, HAS, IQTIG, GKV-Spitzenverband, the Spanish ICD Registry). Points the AI could not confirm from a source were left out.

## What was not done, and why

- **Screening validation (AI vs manual):** the original screening records (11,670 hits reduced to 1,680, then 50 included) are not available, so AI screening could not be scored against them.
- **Re-extraction from source papers:** the study PDFs are not in this repository. The data here is as extracted in the original analysis, which quality control shows needs checking against the source papers.
- **Plot 7 (age, mortality):** cannot be rebuilt without the RevMan file.

## Prompt library

Prompts used, so the method can be reused:

**Forest plot extraction**
> From this RevMan forest plot image, transcribe every study row into CSV with columns: subgroup, study, year, log_hr, se, weight_pct, hr_ci exactly as printed. Also transcribe each subtotal's HR, CI, Tau², Chi², df, I², Z and P. Do not calculate or correct anything. If a cell is unreadable or missing, leave it blank and say which.

**Discrepancy check**
> Here is the results text of a meta-analysis and a table of the reproduced pooled results. List every statement where the text's HR, CI, I², P value, direction ("reduction"/"increase") or significance claim differs from the table. Quote the text (under 15 words) and give the table value. Do not judge which is right.

**Payer document extraction**
> From the attached HTA or reimbursement document only, list the eligibility criteria for [CRT / ICD]: NYHA class, LVEF threshold, QRS duration and morphology, required prior therapy, other conditions, listing or payment mechanism and date. Give the page or section for every point. Write "not stated" where the document is silent, and keep the original wording in brackets when translating.
