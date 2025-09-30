# 🎓 College ROI & Fairness — A Data Storytelling Project

## 📌 What’s this?

This project explores the U.S. Department of Education's College Scorecard data to uncover insights about the financial return on investment (ROI) of higher education. Our goal is to tell a data-driven story for prospective students and their families, helping them understand how factors like field of study and institution type relate to post-graduation earnings and debt.

Beyond simple ROI calculations, we also investigate potential fairness and equity issues within the data, specifically examining the relationship between the gender composition of an institution and the average earnings of its graduates.


**Public Communication Deliverable:** https://bylinedocs.com/published/10bcde8e-8f14-438f-98d3-a276b87d094e


## 💾 Dataset

The data for this analysis is sourced from the U.S. Department of Education's **College Scorecard**. We utilize two main institution-level datasets for our analysis:

1.  **Most Recent Data by Field of Study:** This dataset provides detailed information on outcomes like debt and earnings, broken down by field of study within each institution.
    * **Direct Link:** [https://collegescorecard.ed.gov/data/](https://collegescorecard.ed.gov/data/) (Under "Field of Study")
2.  **Most Recent Institution-Level Data:** This dataset contains institutional characteristics, including student demographics like gender distribution.
    * **Direct Link:** [https://collegescorecard.ed.gov/data/](https://collegescorecard.ed.gov/data/) (Under "Institution-Level")

The official data dictionary and glossary of terms can be found here:
* **Glossary:** [https://collegescorecard.ed.gov/data/glossary/](https://collegescorecard.ed.gov/data/glossary/)

*Note: The raw data files are too large to be included in this GitHub repository. However, they are publicly available and will be downloaded automatically when running the 01_preprocess.ipynb and 03_fairness.ipynb.*

### 📊 Key Features & Data Dictionary

This project relies on several key variables from the source data and creates new features to facilitate the analysis.

### 🔑 Engineered Features

These features were created in our notebooks to calculate ROI and analyze fairness.

* **`ROI_EARNINGS_TO_DEBT` (float):** The core metric for our story, representing the return on investment.  
    * **Formula:** `EARN_MDN_5YR / DEBT_ALL_STGP_ANY_MDN`  
    * A higher value indicates a better financial return.
* **`AFFORDABILITY` (categorical):** Classification of repayment burden based on the percentage of income required for a 10-year loan plan.  
    * **Values:** Very Affordable (<8%), Affordable (8–12%), Moderate (12–20%), Expensive (>20%).
* **`MAJOR_FIELD` (string):** Grouped academic disciplines (e.g., Engineering, Business, Computer Science, Health), derived from CIP codes for easier comparison.
* **`women_proportion` (float):** The proportion of undergraduate students who are women at an institution.  
    * **Source:** Directly from `UGDS_WOMEN`.  
    * Used in the fairness analysis (`03_fairness.ipynb`).
* **`avg_earnings` (float):** The average 5-year median earnings of graduates across all programs at an institution.  
    * Used in the fairness analysis (`03_fairness.ipynb`).

### 📖 Key Source Variables

These are the most important columns from the original College Scorecard data used in our analysis.

* **`INSTNM` (string):** Institution name.  
* **`CIPDESC` (string):** The description of the academic program (field of study).  
* **`CONTROL` (string):** The control of the institution (e.g., Public, Private nonprofit, Private for-profit).  
* **`EARN_MDN_5YR` (float):** Median earnings of graduates 5 years after completion.  
* **`DEBT_ALL_STGP_ANY_MDN` (float):** Median debt for students who completed the program.  
* **`UGDS_WOMEN` (float):** Share of undergraduates who are women.  
* **`TUITIONFEE_IN` (float):** In-state tuition fee.  




## 🔧 How to Reproduce the Analysis

To replicate this analysis, please follow the steps below:

**1. Clone the Repository:**
```bash
git clone https://github.com/SophiaYifei/college-scorecard-roi-storytelling.git
cd college-scorecard-roi-storytelling
```

**2. Set up a Virtual Environment (Recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

**3. Install Dependencies:**
All required Python libraries are listed in the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

**4. Run the Jupyter Notebooks:**
The analysis is divided into three notebooks, which should be run in the following order:

* **`notebooks/01_preprocess.ipynb`**: This notebook downloads the raw "Field of Study" data, cleans it, performs feature engineering (e.g., creating an ROI score), and saves the processed data to `data/processed/`.
* **`notebooks/02_analysis.ipynb`**: This notebook conducts the primary exploratory data analysis (EDA) on the processed data from the previous step, generating key visualizations about ROI.
* **`notebooks/03_fairness.ipynb`**: This notebook downloads the institution-level data to analyze the relationship between tuitions and earnings, student gender demographics and earnings, exploring the ethical dimensions of the data.

After running these notebooks, the processed data will be available in the `data/processed` directory, and all figures will be saved in the `figures` directory.



## 📁 Project Structure

```
.
├── data
│   ├── processed/      # Cleaned data generated by preprocessing scripts
│   │   └── field_of_study_processed.csv
│   └── raw/            # Raw data is downloaded here by notebooks
│       ├── Most-Recent-Cohorts-Field-of-Study.csv
│       └── Most-Recent-Cohorts-Institution.csv
├── figures/            # Visualizations and figures generated during analysis
├── notebooks/          # Jupyter notebooks for exploration and documentation
│   ├── 01_preprocess.ipynb
│   ├── 02_analysis.ipynb
│   └── 03_fairness.ipynb
├── Scripts/            # Python scripts (converted from notebooks, reproducible pipeline)
│   ├── 01_preprocess.py
│   ├── 02_analysis.py
│   └── 03_fairness.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```




## 🤔 Ethical Considerations & Limitations

While the College Scorecard is a valuable resource, it's crucial to acknowledge its limitations:

* **Definition of ROI:** Our ROI metric (median earnings / median debt) is a simplification. It does not account for factors like quality of life, job satisfaction, career progression, or non-monetary benefits of education.
* **Data Representation:** The data may not represent all institutions equally. Smaller institutions or those with fewer federal student aid recipients may have less comprehensive data available.
* **Salary Variation:** Reported earnings are not adjusted for regional differences in cost of living, which can significantly impact the true value of a salary.
* **Bias in Demographics:** The analysis in `03_fairness.ipynb` reveals a correlation between institutional gender composition and graduate earnings. This highlights potential systemic biases and emphasizes that institutional averages can obscure deeper inequities.
* **Incomplete Costs:** The debt figures primarily reflect federal student loans and may not include private loans or the full cost of attendance (e.g., living expenses).

Our story aims to be a starting point for inquiry, not a definitive guide. We encourage users to consider these limitations and use this data as one of many tools in their decision-making process.

## 📄 License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.