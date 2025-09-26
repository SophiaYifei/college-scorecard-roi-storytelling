# Field of Study Data Dictionary (Most-Recent-Cohorts-Field-of-Study.csv)

This section documents the meaning of selected variables in the **Field of Study (FoS)** dataset, based on the official College Scorecard Glossary.  
Where official definitions are not provided, we note this and give a data-scientist interpretation based on Scorecard naming conventions.

---

## Basic Identifiers
| Variable   | Definition |
|------------|------------|
| `UNITID`   | **Official**. Unique IPEDS institutional ID; key to merge with Institution-level data. |
| `OPEID6`   | **Official**. 6-digit Office of Postsecondary Education ID, used in federal financial aid reporting. |
| `INSTNM`   | **Official**. Institution name. |
| `CONTROL`  | **Official**. Control of institution (1 = Public, 2 = Private nonprofit, 3 = Private for-profit). |
| `MAIN`     | **No glossary**. Likely indicator of main campus (1 = Yes, 0 = No). |
| `CIPCODE`  | **Official**. Classification of Instructional Programs code (2020 edition). |
| `CIPDESC`  | **Official**. CIP description. |
| `CREDLEV`  | **Official**. Credential level code. |
| `CREDDESC` | **Official**. Credential level description (e.g., “Bachelor’s degree”). |

---

## Graduate Counts
| Variable       | Definition |
|----------------|------------|
| `IPEDSCOUNT1`  | **No glossary**. Likely IPEDS completions count (alternative aggregation). |
| `IPEDSCOUNT2`  | **Official**. Number of awards earned in this field of study (2020–21 cohort). |

---

## Debt Variables
General naming rules:  
- `STGP` = Student borrowers; `PP` = Parent PLUS loans  
- `ANY` = Debt accumulated at any school; `EVAL` = Debt from this institution only  
- `N` = sample size; `MEAN` = mean; `MDN` = median; `MDN10YRPAY` = estimated monthly payment under 10-year plan

| Variable | Definition |
|----------|------------|
| `DEBT_ALL_STGP_ANY_N/MEAN/MDN` | **Official**. Total federal student loan debt (all schools) — sample size / mean / median. |
| `DEBT_ALL_STGP_EVAL_N/MEAN/MDN` | **Official**. Student loan debt (this school only) — sample size / mean / median. |
| `DEBT_ALL_PP_ANY_*` / `DEBT_ALL_PP_EVAL_*` | **Official**. Parent PLUS loan debt, across all schools / at this school. |
| `DEBT_MALE_STGP_ANY_*` / `DEBT_MALE_STGP_EVAL_*` | **No glossary**. Debt for male students (all / this school). |
| `DEBT_NOTMALE_STGP_ANY_*` / `DEBT_NOTMALE_STGP_EVAL_*` | **No glossary**. Debt for non-male students. |
| `DEBT_PELL_STGP_ANY_*` / `DEBT_PELL_STGP_EVAL_*` | **Official**. Debt for Pell Grant recipients. |
| `DEBT_NOPELL_STGP_ANY_*` / `DEBT_NOPELL_STGP_EVAL_*` | **Official**. Debt for non-Pell recipients. |
| `DEBT_ALL_PP_ANY_MDN10YRPAY` / `DEBT_ALL_PP_EVAL_MDN10YRPAY` | **Official**. Median monthly payment (10-year plan), Parent PLUS. |
| `DEBT_ALL_STGP_ANY_MDN10YRPAY` / `DEBT_ALL_STGP_EVAL_MDN10YRPAY` | **Official**. Median monthly payment (10-year plan), student loans. |

---

## Earnings Variables
General naming rules:  
- `WNE` = Working, Not Enrolled; `NWNE` = Not Working, Not Enrolled  
- `HI` = high-quality restricted sample  
- `MDN` = median; `COUNT` = sample size

| Variable | Definition |
|----------|------------|
| `EARN_COUNT_WNE_HI_1YR` / `EARN_MDN_HI_1YR` | **Official**. Number and median annual earnings of graduates working/not enrolled, 1 year after completion (high-quality). |
| `EARN_COUNT_WNE_HI_2YR` / `EARN_MDN_HI_2YR` | **Official**. Same, measured 2 years after completion. |
| `EARN_COUNT_NWNE_HI_1YR/2YR` | **No glossary**. Likely counts of graduates not working and not enrolled at 1/2 years. |
| `EARN_CNTOVER150_HI_1YR/2YR` | **No glossary**. Likely count of graduates with earnings above 150% of a threshold (e.g., poverty line). |
| `EARN_COUNT_WNE_3YR/4YR/5YR` / `EARN_MDN_3YR/4YR/5YR` | **Official**. WNE sample size and median earnings 3–5 years post-completion. |
| `EARN_COUNT_PELL_WNE_*` / `EARN_PELL_WNE_MDN_*` | **No glossary**. Earnings for Pell recipients, WNE group, at 1/4/5 years. |
| `EARN_COUNT_NOPELL_WNE_*` / `EARN_NOPELL_WNE_MDN_*` | **No glossary**. Earnings for non-Pell students, WNE group. |
| `EARN_COUNT_MALE_WNE_*` / `EARN_MALE_WNE_MDN_*` | **No glossary**. Earnings for male students, WNE group. |
| `EARN_COUNT_NOMALE_WNE_*` / `EARN_NOMALE_WNE_MDN_*` | **No glossary**. Earnings for non-male students, WNE group. |
| `EARN_GT_THRESHOLD_*YR` | **Official**. Fraction/number of individuals earning more than a high school graduate, X years after completion. |
| `EARN_COUNT_HIGH_CRED_*YR` | **No glossary**. Likely count of graduates with high credits (definition not documented). |
| `EARN_IN_STATE_*YR` | **No glossary**. Likely indicator/count of graduates working in-state, measured at X years. |

---

## Repayment Variables (BBRR)
| Variable | Definition |
|----------|------------|
| `BBRRx_FED_COMP_*` | **Official**. Borrower-Based Repayment Rate: distribution of federal loan borrowers’ repayment outcomes x years after entering repayment. <br>Subcategories: `N` = total borrowers; `DFLT` = default; `DLNQ` = delinquent; `FBR` = forbearance; `DFR` = deferment; `NOPROG` = no progress; `MAKEPROG` = making progress; `PAIDINFULL` = loans paid; `DISCHARGE` = discharged. |

---

## Other
| Variable | Definition |
|----------|------------|
| `DISTANCE` | **No glossary**. Likely indicates distance/online program (1 = Yes, 0 = No). |

---

## Notes on Time Coverage
- **Debt metrics** (e.g., `DEBT_ALL_STGP_EVAL_MDN`): measured for completers in **2018–19 and 2019–20 award years**.  
- **Earnings metrics** (e.g., `EARN_MDN_HI_2YR`): measured for earlier cohorts (e.g., 2014–16 completers), at 1–5 years after graduation, with IRS-based income data through **2020–21 calendar years**.  
- Thus, ROI estimates reflect outcomes for students graduating in the **mid-to-late 2010s**, with post-graduation earnings observed up to 2021.

