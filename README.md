# 🎓 College ROI & Fairness — A Data Storytelling Project

## 📌 What’s this?
This project quantifies the **return on investment (ROI)** of U.S. college majors using the Dept. of Education’s **College Scorecard** dataset.  
It explores how ROI varies by field of study and institution type.  

This repository contains:
- Reproducible code  
- The processed dataset  
- Final analysis outputs  

---

## 1️⃣ Project Overview

**Key Questions**
- Which college majors pay back the fastest (defined by the ratio of early-career earnings to student debt)?  
- How does this ROI vary across different types of institutions (e.g., Public vs. Private)?  

**Audience**
- High school students and parents deciding on majors  
- Educators and policymakers interested in the value of higher education  

**Deliverables**
- Public-facing data story (blog post / infographic)  
- Final presentation  
- Fully reproducible GitHub repository  

---

## 2️⃣ How to Reproduce

Follow the steps below to replicate the analysis.

### 🔧 Prerequisites
- Python **3.8+**  
- `git` installed on your system  

---

### 📥 Step 1: Clone the Repository
```bash
# Replace <USER>/<REPO> with your GitHub username and repository name
git clone https://github.com/SophiaYifei/college-scorecard-roi-storytelling.git
cd college-scorecard-roi-storytelling
```
### ⚙️ Step 2: Set up the Python Environment
```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install all required libraries
pip install -r requirements.txt
```
### 🧹 Step 3: Run the Data Preprocessing Pipeline
- **Action:** Open `notebooks/notebook1.ipynb` in Jupyter and run all cells.  
- **Output:** A clean dataset saved to `data/processed/field_of_study_processed.csv`.  

---

### 📊 Step 4: Run the Exploratory Data Analysis (EDA)
- **Action:** Open `notebooks/notebook2.ipynb` in Jupyter and run all cells.  
- **Output:** Key findings and charts for the final report & presentation.  

---

## 3️⃣ The Data

This section details the dataset used: **`field_of_study_processed.csv`**

**Source**
- Public data from the U.S. Department of Education’s [College Scorecard](https://collegescorecard.ed.gov/data/)  
- **Raw Data File:** `Most-Recent-Cohorts-Field-of-Study.csv`  
- **Size:** 26,905 reliable records across 18 fields  

---

### 🔑 Key Metrics (Engineered)
- **`ROI_EARNINGS_TO_DEBT` (float64):** Earnings-to-Debt Ratio = `EARN_MDN_5YR / DEBT_ALL_STGP_ANY_MDN`  
  - Higher = better ROI  

- **`PAYBACK_YEARS` (float64):** Payback Period (years) = `DEBT_ALL_STGP_ANY_MDN / EARN_MDN_5YR`  
  - Lower = better  

- **`MONTHLY_PAYMENT_PCT` (float64):** Monthly Loan Burden (%)  
  - Formula: `(DEBT_ALL_STGP_ANY_MDN10YRPAY / (EARN_MDN_5YR / 12)) * 100`  

---

### 🏷️ Categorical Labels (Engineered)
- **`MAJOR_FIELD` (object):** Broad study field (*Engineering*, *Business*, etc.)  
- **`ROI_CATEGORY` (category):** ROI rating (*Poor*, *Average*, *Excellent*)  
- **`AFFORDABILITY` (category):** Affordability rating (*Affordable*, *Expensive*)  
- **`CREDENTIAL_LEVEL_NAME` (object):** Human-readable credential (e.g., *Bachelor Degree*)  
- **`CIP_2DIGIT` (object):** First two digits of `CIPCODE`  

---

### 🏫 Program & Institution Identifiers (Source)
- **`INSTNM` (object):** Institution name  
- **`CIPCODE` (int64):** 6-digit program code  
- **`CIPDESC` (object):** Program description  
- **`CREDLEV` (int64):** Credential code (e.g., 3 = Bachelor’s)  
- **`CREDDESC` (object):** Credential description  
- **`CONTROL` (object):** Institution control (*Public*, *Private nonprofit*)  
- **`IPEDSCOUNT2` (float64):** Number of graduates  

---

### 💰 Core Financials (Source)
- **`EARN_MDN_5YR` (float64):** Median earnings 5 years after graduation  
- **`DEBT_ALL_STGP_ANY_MDN` (float64):** Median federal loan debt  
- **`DEBT_ALL_STGP_ANY_MDN10YRPAY` (float64):** Median monthly loan payment (10-year plan)  

---

## 4️⃣ License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
