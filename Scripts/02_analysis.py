#!/usr/bin/env python
# coding: utf-8

# College Scorecard ROI Analysis - Data Exploration & Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from pathlib import Path

# Create directory to save figures
figures_dir = Path('../figures')
figures_dir.mkdir(parents=True, exist_ok=True)

# Configure plot style
plt.style.use("seaborn-v0_8")
sns.set_palette("Set2")

print("Current working directory:", os.getcwd())

# Load processed data
field_of_study = pd.read_csv("../data/processed/field_of_study_processed.csv")
print("Processed data loaded.")

print(field_of_study.head())

# Rename some variables for clarity
field_of_study = field_of_study.rename(columns={
    "CIPDESC": "DEG_DEPT",
    "CONTROL": "PUBL_OR_PRIV",
    "INSTNM": "UNI_NAME",
    "IPEDSCOUNT2": "CLASS_SIZE"
})

# Fix institution type values
field_of_study["PUBL_OR_PRIV"] = field_of_study["PUBL_OR_PRIV"].replace({
    "Private, nonprofit": "Private non-profit",
    "Private, for-profit": "Private for-profit"
})

print("Data shape:", field_of_study.shape)
field_of_study.info()

# Summary statistics
print(field_of_study.describe(include="all"))

# Value counts for categorical features
for col in field_of_study.select_dtypes(include="object").columns:
    print(f"\nValue counts for {col}:\n", field_of_study[col].value_counts().head())

# Remove redundant variables
field_of_study = field_of_study.drop(
    columns=[
        "DEBT_ALL_STGP_EVAL_MDN",
        "DEBT_ALL_STGP_ANY_MDN10YRPAY",
        "DEBT_ALL_STGP_EVAL_MDN10YRPAY",
        "CIPCODE",
        "CREDLEV",
        "CIP_2DIGIT",
        "AFFORDABILITY",
        "CREDDESC"
    ],
    errors="ignore"
)

print("Columns after dropping redundant:")
print(field_of_study.columns)

print(field_of_study.head())
print("Missing values per column:")
print(field_of_study.isnull().sum())

# Multicollinearity check using VIF
features = [
    "EARN_MDN_5YR",
    "DEBT_ALL_STGP_ANY_MDN",
    "CLASS_SIZE",
    "ROI_EARNINGS_TO_DEBT",
    "DEBT_TO_INCOME_RATIO",
    "MONTHLY_PAYMENT_PCT",
    "PAYBACK_YEARS"
]
X = field_of_study[features].dropna()
X_const = sm.add_constant(X)

vif_df = pd.DataFrame()
vif_df["Feature"] = X.columns
vif_df["VIF"] = [variance_inflation_factor(X_const.values, i+1)
                 for i in range(len(X.columns))]
print(vif_df.sort_values("VIF", ascending=False))

def reduce_vif(X, thresh=10.0):
    dropped = True
    while dropped:
        dropped = False
        X_const = sm.add_constant(X)
        vif = [variance_inflation_factor(X_const.values, i+1) for i in range(len(X.columns))]
        max_vif = max(vif)
        if max_vif > thresh:
            maxloc = vif.index(max_vif)
            print(f"Dropping '{X.columns[maxloc]}' with VIF={max_vif:.2f}")
            X = X.drop(columns=[X.columns[maxloc]])
            dropped = True
    return X

X_reduced = reduce_vif(X, thresh=10.0)
remaining_features = X_reduced.columns.tolist()
print("Remaining features:", remaining_features)

# Create reduced dataframe
field_of_study_reduced = field_of_study[remaining_features + [
    "DEG_DEPT", "UNI_NAME", "PUBL_OR_PRIV", "CREDENTIAL_LEVEL_NAME", "MAJOR_FIELD", "ROI_CATEGORY"
]]

print(field_of_study_reduced.head())

# Numeric distributions
field_of_study_reduced.hist(bins=50, figsize=(12, 10))
plt.suptitle("Distributions of Numeric Features")
figure_path = figures_dir / 'notebook2' / 'distribution_of_numeric_features.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.show()

# Class size distribution
field_of_study_reduced["CLASS_SIZE"].hist(bins=50, range=(0, 400))
plt.title("Distribution of Class Size")
plt.xlim(0, 400)
figure_path = figures_dir / 'notebook2' / 'distribution_of_class_size.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.show()

# ROI numeric score
field_of_study_reduced["ROI_Numeric_Score"] = (
    field_of_study_reduced["EARN_MDN_5YR"] / field_of_study_reduced["DEBT_ALL_STGP_ANY_MDN"]
)
print(field_of_study_reduced["ROI_Numeric_Score"].describe())

# Aggregate by major field
df_no_other = field_of_study_reduced[
    field_of_study_reduced["MAJOR_FIELD"].str.strip().str.lower() != "other"
].copy()

agg = (
    df_no_other.dropna(subset=["ROI_Numeric_Score"])
    .groupby("MAJOR_FIELD", as_index=False)
    .agg(ROI=("ROI_Numeric_Score", "median"), n=("ROI_Numeric_Score", "size"))
)
agg = agg[agg["n"] >= 20]

top7 = agg.nlargest(7, "ROI")
bottom7 = agg.nsmallest(7, "ROI")

fig, axes = plt.subplots(1, 2, figsize=(16, 8), sharex=False)

order_top = top7.sort_values("ROI", ascending=False)["MAJOR_FIELD"]
sns.barplot(x="ROI", y="MAJOR_FIELD", data=top7,
            order=order_top, ax=axes[0], errorbar=None)
axes[0].set_title("Top 7 Fields of Study by ROI (Median)")
axes[0].set_xlabel("ROI (Earnings / Debt)")
axes[0].set_ylabel("Field of Study")

order_bot = bottom7.sort_values("ROI", ascending=True)["MAJOR_FIELD"]
sns.barplot(x="ROI", y="MAJOR_FIELD", data=bottom7,
            order=order_bot, ax=axes[1], errorbar=None)
axes[1].set_title("Bottom 7 Fields of Study by ROI (Median)")
axes[1].set_xlabel("ROI (Earnings / Debt)")
axes[1].set_ylabel("")

plt.tight_layout()
figure_path = figures_dir / 'notebook2' / 'top_bottom_7.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.show()

# Storytelling visualizations
if {"EARN_MDN_5YR", "DEBT_ALL_STGP_ANY_MDN"}.issubset(field_of_study_reduced.columns):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x="DEBT_ALL_STGP_ANY_MDN", y="EARN_MDN_5YR",
        hue="PUBL_OR_PRIV", data=field_of_study_reduced, alpha=0.7
    )
    plt.title("Earnings vs Debt by Institution Control")
    plt.xlabel("Median Debt (All Federal Loans)")
    plt.ylabel("Median Earnings (5 Years After Graduation)")
    figure_path = figures_dir / 'notebook2' / 'earnings_debts_by_institution_control.png'
    plt.savefig(figure_path, bbox_inches='tight')
    plt.show()

if {"ROI_Numeric_Score", "CREDENTIAL_LEVEL_NAME"}.issubset(field_of_study_reduced.columns):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="CREDENTIAL_LEVEL_NAME", y="ROI_Numeric_Score",
        data=field_of_study_reduced, palette="Set2")
    plt.title("Distribution of ROI by Credential Level")
    plt.xlabel("Credential Level")
    plt.ylabel("ROI (Earnings / Debt)")
    plt.xticks(rotation=30)
    figure_path = figures_dir / 'notebook2' / 'distribution_of_roi_by_credential_level.png'
    plt.savefig(figure_path, bbox_inches='tight')
    plt.show()

if {"ROI_Numeric_Score", "PUBL_OR_PRIV"}.issubset(field_of_study_reduced.columns):
    plt.figure(figsize=(8, 6))
    sns.barplot(
        x="PUBL_OR_PRIV", y="ROI_Numeric_Score",
        data=field_of_study_reduced, estimator="mean", errorbar="sd", palette="Set2"
    )
    plt.title("Average ROI by Institution Type")
    plt.xlabel("Institution Type")
    plt.ylabel("Average ROI (Earnings / Debt)")
    figure_path = figures_dir / 'notebook2' / 'avg_roi_by_institution_type.png'
    plt.savefig(figure_path, bbox_inches='tight')
    plt.show()
