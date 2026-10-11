# European reimbursement and HTA for CRT and ICD (EU4 + UK)

*Researched October 2026 from public sources (listed at the end). Reimbursement rules change; check the sources before relying on any detail.*

**Key finding:** every European pathway reviewed limits CRT and ICD to patients with LVEF ≤35%, and the CRT criteria turn on QRS duration and left bundle branch block (LBBB), not on NYHA class alone. The meta-analysis subgroups so far (NYHA, LVEF, age, sex) do not include QRS or LBBB, so the results cannot be mapped directly onto how payers decide who gets a device.

## How each market assesses and pays

| Market | Who decides | How the device is paid | Eligibility criteria used |
| --- | --- | --- | --- |
| **UK (England)** | NICE technology appraisal [TA314](https://www.nice.org.uk/guidance/ta314/chapter/1-Guidance), June 2014; moved to NICE's static list in 2017 ([decision paper](https://nice.org.uk/guidance/ta314/evidence/static-list-review-decision-paper-august-2017-pdf-4595433230)) | ICDs and CRT-D are categories 4 and 5 of NHS England's [national supply system for tariff-excluded devices](https://www.england.nhs.uk/commissioning/spec-services/key-docs/medical-devices/): bought centrally via NHS Supply Chain and paid outside the procedure tariff | LVEF ≤35%; a grid of NYHA class × QRS duration × LBBB decides between ICD, CRT-P and CRT-D |
| **France** | HAS (CNEDiMTS) assesses each device by brand name; listed on the LPPR | Brand-name LPPR listing for 5 years, e.g. the [Quadra Allure MP CRT-P renewal](https://www.has-sante.fr/upload/docs/evamed/CNEDIMTS-7598_QUADRA%20ALLURE%20MP_9%20juillet%202024_7598_avis.pdf) of 9 July 2024 (service rendered "sufficient", ASR V) | Sinus rhythm: NYHA II–IV, optimal medical therapy, LVEF ≤35%, wide QRS (thresholds differ between sections of the opinion). Permanent AF: NYHA III–IV, QRS ≥120 ms, near-100% biventricular pacing |
| **Germany** | Statutory hospital DRG system (InEK); G-BA mandates national quality assurance run by IQTIG | aG-DRGs F01A–F01F cover ICD implantation, split by one-, two- or three-chamber (CRT-D) systems and complexity ([2025 catalogue extract](https://www.gkv-spitzenverband.de/media/dokumente/krankenversicherung_1/krankenhaeuser/drg/drg_2025/Fallpauschalenkatalog_2025_FDA_DRGs_mit_hohem_Sachkostenanteil_14.10.2024.pdf)) | Guideline-based; hospitals are measured on it. IQTIG indicator "guideline-concordant indication" was met in 91.02% of ICD implants in 2023, and "guideline-concordant system choice" in 93.78% ([IQTIG 2024 report](https://www.iqtig.org/downloads/auswertung/aj2024/hsmdef-defi-impl/DeQS-RL_HSMDEF-DEFI-IMPL_AJ2024_BUAW_V02_2024-08-15.pdf)) |
| **Italy** | AGENAS (national HTA) plus regional HTA bodies; national HTA programme for medical devices fully running since early 2024 ([MTRC overview](https://mtrconsult.com/market-access-medical-technologies-italy)) | DRG-based (CMS-DRG v24, procedure codes not updated since 2007); regions set their own tariffs and can add payments for expensive devices | Follows ESC guidelines; access varies by region |
| **Spain** | Ministry of Health and regional health services | Regional budgets and tenders | Follows ESC guidelines. ICD use is the lowest of the European countries compared: 171 implants per million in 2023 vs ~300 European average, ranging from 126 (Balearic Islands, Murcia) to 314 (Cantabria) ([Spanish ICD Registry 2023](https://www.revespcardiol.org/en-spanish-implantable-cardioverter-defibri-articulo-S1885585724002779-pdf-file)) |

**Common clinical reference:** the 2021 ESC heart failure guidelines recommend a primary-prevention ICD for symptomatic HFrEF with LVEF ≤35% after 3 months of guideline-directed therapy and expected survival over one year, and CRT for symptomatic patients with LVEF <35%, sinus rhythm and LBBB with QRS over 150 ms ([ACC summary](https://www.acc.org/latest-in-cardiology/ten-points-to-remember/2021/08/29/18/05/2021-esc-guidelines-for-hf-esc-2021)).

## Do payer criteria match the meta-analysis findings?

| Meta-analysis subgroup | Result (random effects) | European payer position | Match? |
| --- | --- | --- | --- |
| LVEF <35% | Mortality 1.16 (0.72–1.87); hospitalisation 1.09 (0.92–1.29) | The core eligible population in every market | **No.** The large trial evidence payers rely on shows clear benefit here, so this points to problems in the dataset |
| LVEF >35% | Mortality 0.67 (0.40–1.13) | Not eligible in any market reviewed | Not relevant to reimbursement; the review's own inclusion criteria also excluded it |
| NYHA II–IV | No significant effect in any class | NICE and HAS use NYHA, but always combined with QRS and LBBB | **Cannot compare:** QRS and LBBB were not analysed |
| Age >70 | Hospitalisation 0.80 (0.73–0.88), robust | No age cut-off; ESC requires expected survival over one year | Supports access for older patients |
| Sex | No significant mortality difference | No sex-specific criteria | The IPD evidence below suggests women gain more from CRT |

## The benchmark payers use

Two UK studies built on individual patient data from 13 RCTs (12,638 patients) underpin how payers view these devices:

- **Clinical:** compared with medical therapy, mortality fell by 42% with CRT-D, 29% with ICD and 28% with CRT-P. Patients with QRS ≥150 ms, LBBB, or female sex gained more from CRT ([Woods et al., Heart 2015](https://researchonline.lshtm.ac.uk/id/eprint/2274449)).
- **Economic:** at £30,000 per QALY, CRT-D was cost-effective in 10 of 24 subgroups, including all LBBB patients in NYHA I–III; ICD and CRT-P were the cost-effective choice in other subgroups ([Mealing et al., Heart 2016](https://eprints.whiterose.ac.uk/id/eprint/100095/)).

Note that Mealing 2016 is a cost-effectiveness model, not a primary outcome study, yet it appears as a study in the original mortality forest plot. Its estimates come from the same RCTs as other included evidence, so it is being removed in the re-extraction.

## Implications for a manufacturer's market access strategy

1. **Evidence must be stratified by QRS duration and LBBB**, because that is how NICE, HAS and the cost-effectiveness evidence define who benefits.
2. **The UK and France reward differentiation differently.** In England devices are bought nationally through NHS Supply Chain, so price and category frameworks matter most. In France each brand is listed separately, and an ASR V rating means no price premium over existing devices.
3. **Germany rewards appropriate use.** National quality indicators track guideline-concordant indication and system choice, so supporting correct patient selection is part of the value offer.
4. **Spain and Italy are about regional access.** Implant rates vary more than twofold between Spanish regions, and Italian regions set their own tariffs. Regional budget-impact evidence and engagement with regional HTA bodies matter more than a single national submission.
