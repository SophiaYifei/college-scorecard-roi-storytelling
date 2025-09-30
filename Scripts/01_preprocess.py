#!/usr/bin/env python
# coding: utf-8

# College Scorecard ROI Analysis - Data Preprocessing

# Part 1: Setup & Data Loading
import pandas as pd
import gdown
from pathlib import Path

# Setup file path and download link
data_dir = Path('../data/raw')
file_path = data_dir / 'Most-Recent-Cohorts-Field-of-Study.csv'
drive_link = "https://drive.google.com/file/d/1ER-vyYO-dxN-qLAwDFsovOU_-JSw30SP/view?usp=sharing"

data_dir.mkdir(parents=True, exist_ok=True)

if not file_path.exists():
    print(f"File not found at '{file_path}', downloading from Google Drive...")
    gdown.download(drive_link, str(file_path), fuzzy=True)
    print("Download complete!")
else:
    print(f"File already exists at '{file_path}', skip download.")

# Load CSV data
df_raw = pd.read_csv(file_path, low_memory=False)
print("Data loaded successfully!")

# Part 2: Initial Data Exploration
print(f"Dataset shape (rows, columns): {df_raw.shape}")
print("\nFirst 5 rows of the raw data:")
print(df_raw.head())
print("\nData types and non-null values:")
df_raw.info()

# Part 3: Column Selection for ROI Analysis
columns_to_keep = [
    'EARN_MDN_5YR',
    'DEBT_ALL_STGP_ANY_MDN',
    'DEBT_ALL_STGP_EVAL_MDN',
    'DEBT_ALL_STGP_ANY_MDN10YRPAY',
    'DEBT_ALL_STGP_EVAL_MDN10YRPAY',
    'INSTNM',
    'CIPCODE',
    'CIPDESC',
    'CREDLEV',
    'CREDDESC',
    'CONTROL',
    'IPEDSCOUNT2',
]

df_selected = df_raw[columns_to_keep].copy()
print("\nDataFrame after selecting columns:")
print(f"New shape: {df_selected.shape}")
print(df_selected.head())
df_selected.info()

# Part 4: Data Cleaning & Type Conversion
df_cleaned = df_selected.copy()
numeric_cols = [
    'EARN_MDN_5YR', 'DEBT_ALL_STGP_ANY_MDN', 'DEBT_ALL_STGP_EVAL_MDN',
    'DEBT_ALL_STGP_ANY_MDN10YRPAY', 'DEBT_ALL_STGP_EVAL_MDN10YRPAY', 'IPEDSCOUNT2'
]

for col in numeric_cols:
    df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

print("\nData types after conversion:")
df_cleaned.info()

missing_counts = df_cleaned.isnull().sum()
missing_percentage = (missing_counts / len(df_cleaned) * 100).round(2)
missing_summary = pd.DataFrame({
    'missing_count': missing_counts,
    'missing_percentage': missing_percentage
})
print("\nMissing value analysis:")
print(missing_summary[missing_summary['missing_count'] > 0].sort_values(by='missing_percentage', ascending=False))

# Part 5: Feature Engineering - ROI Metrics
df_roi = df_cleaned.copy()
df_roi['ROI_EARNINGS_TO_DEBT'] = df_roi['EARN_MDN_5YR'] / df_roi['DEBT_ALL_STGP_ANY_MDN']
df_roi['DEBT_TO_INCOME_RATIO'] = df_roi['DEBT_ALL_STGP_ANY_MDN'] / df_roi['EARN_MDN_5YR']
df_roi['PAYBACK_YEARS'] = df_roi['DEBT_ALL_STGP_ANY_MDN'] / df_roi['EARN_MDN_5YR']
monthly_earnings = df_roi['EARN_MDN_5YR'] / 12
df_roi['MONTHLY_PAYMENT_PCT'] = (df_roi['DEBT_ALL_STGP_ANY_MDN10YRPAY'] / monthly_earnings) * 100

print("\nPreview with new ROI metrics:")
print(df_roi.head())
print("\nStatistics for new ROI metrics:")
print(df_roi[['ROI_EARNINGS_TO_DEBT', 'PAYBACK_YEARS', 'MONTHLY_PAYMENT_PCT']].describe())

# Part 6: Data Filtering
df_filtered = df_roi.copy()
initial_rows = len(df_filtered)
print(f"\nStarting with {initial_rows} rows.")

df_filtered = df_filtered.dropna(subset=['ROI_EARNINGS_TO_DEBT'])
df_filtered = df_filtered[df_filtered['IPEDSCOUNT2'] >= 10]
df_filtered = df_filtered[df_filtered['EARN_MDN_5YR'].between(10000, 500000)]

final_rows = len(df_filtered)
print(f"Filtering complete. {final_rows} rows remaining ({(final_rows/initial_rows*100):.2f}% of original).")
print("\nStatistics after filtering:")
print(df_filtered[['ROI_EARNINGS_TO_DEBT', 'PAYBACK_YEARS', 'MONTHLY_PAYMENT_PCT']].describe())

# Part 7: Advanced Feature Engineering
df_final = df_filtered.copy()

credential_map = {
    1: 'Undergraduate Certificate',
    2: 'Associate Degree',
    3: 'Bachelor Degree',
    4: 'Post-baccalaureate Certificate',
    5: 'Master Degree',
    6: 'Doctoral Degree',
    7: 'First Professional Degree',
    8: 'Graduate Certificate'
}
df_final['CREDENTIAL_LEVEL_NAME'] = df_final['CREDLEV'].map(credential_map)

df_final['CIP_2DIGIT'] = df_final['CIPCODE'].astype(str).str[:2]
major_map = {
    '11': 'Computer Science',
    '14': 'Engineering',
    '15': 'Engineering Technology',
    '26': 'Biological Sciences',
    '27': 'Mathematics',
    '40': 'Physical Sciences',
    '52': 'Business',
    '51': 'Health Professions',
    '42': 'Psychology',
    '45': 'Social Sciences',
    '23': 'English Language',
    '24': 'Liberal Arts & Humanities',
    '50': 'Visual & Performing Arts',
    '13': 'Education',
}
df_final['MAJOR_FIELD'] = df_final['CIP_2DIGIT'].map(major_map).fillna('Other')

roi_bins = [0, 1, 1.5, 2.5, 4, float('inf')]
roi_labels = ['Poor (<1)', 'Low (1-1.5)', 'Average (1.5-2.5)', 'Good (2.5-4)', 'Excellent (>4)']
df_final['ROI_CATEGORY'] = pd.cut(df_final['ROI_EARNINGS_TO_DEBT'], bins=roi_bins, labels=roi_labels, right=False)

afford_bins = [0, 8, 12, 20, float('inf')]
afford_labels = ['Very Affordable (<8%)', 'Affordable (8-12%)', 'Moderate (12-20%)', 'Expensive (>20%)']
df_final['AFFORDABILITY'] = pd.cut(df_final['MONTHLY_PAYMENT_PCT'], bins=afford_bins, labels=afford_labels, right=False)

print("\nPreview with new categorical features:")
print(df_final.head())
print(df_final[['INSTNM', 'MAJOR_FIELD', 'CIPDESC', 'CREDENTIAL_LEVEL_NAME', 'ROI_EARNINGS_TO_DEBT', 'ROI_CATEGORY', 'AFFORDABILITY']].head())

print("\nDistribution of ROI Categories:")
print(df_final['ROI_CATEGORY'].value_counts(normalize=True).sort_index())

print("\nMajor field distribution:")
print(df_final['MAJOR_FIELD'].value_counts())
print(df_final['MAJOR_FIELD'].value_counts(normalize=True) * 100)

# Part 8: Final Validation & Export
print("Final DataFrame shape:", df_final.shape)
print("\nFinal DataFrame columns:")
print(df_final.columns.tolist())
print("\nFinal DataFrame info:")
df_final.info()

# Export processed data
processed_dir = Path('../data/processed')
processed_dir.mkdir(parents=True, exist_ok=True)
output_path = processed_dir / 'field_of_study_processed.csv'

df_final.to_csv(output_path, index=False)
print(f"\nSuccessfully exported processed data to: {output_path}")
print("This file is now ready for analysis and visualization.")

