#!/usr/bin/env python
# coding: utf-8

# College Scorecard ROI Analysis - Fairness & Gender Analysis

import pandas as pd
import gdown
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Create directory to save figures
figures_dir = Path('../figures')
figures_dir.mkdir(parents=True, exist_ok=True)

# Load processed Field of Study data
fos_path = Path('../data/processed/field_of_study_processed.csv')
if fos_path.exists():
    print(f"Loading processed data from: {fos_path}")
    df_fos = pd.read_csv(fos_path)
else:
    print(f"ERROR: Processed data file not found at {fos_path}")
    df_fos = None

# Download institution-level data
data_dir = Path('../data/raw')
file_path = data_dir / 'Most-Recent-Cohorts-Institution.csv'
drive_link = "https://drive.google.com/file/d/1EhS5gZPAqkQI23SJBPRN9ixaniogTnR8/view?usp=sharing"

data_dir.mkdir(parents=True, exist_ok=True)
if not file_path.exists():
    print(f"File not found at '{file_path}', downloading from Google Drive...")
    gdown.download(drive_link, str(file_path), fuzzy=True)
    print("Download complete!")
else:
    print(f"File already exists at '{file_path}', skip download.")

df_raw = pd.read_csv(file_path, low_memory=False)
print("Institution data loaded.")

# Add reliable join key (OPEID6) to Field of Study data
raw_fos_path = Path('../data/raw/Most-Recent-Cohorts-Field-of-Study.csv')
df_raw_fos_temp = pd.read_csv(raw_fos_path, usecols=['INSTNM', 'OPEID6'])
df_id_map = df_raw_fos_temp.drop_duplicates(subset=['INSTNM']).dropna()

df_fos_enhanced = pd.merge(df_fos, df_id_map, on='INSTNM', how='left')
df_fos_enhanced.dropna(subset=['OPEID6'], inplace=True)
df_fos_enhanced['OPEID6'] = df_fos_enhanced['OPEID6'].astype(int)
print("Enhanced Field of Study data with OPEID6.")

# Select and clean institution data
cols_to_select = ['OPEID6', 'TUITIONFEE_IN', 'UGDS_WOMEN']
df_inst_clean = df_raw[cols_to_select].copy()
df_inst_clean['TUITIONFEE_IN'] = pd.to_numeric(df_inst_clean['TUITIONFEE_IN'], errors='coerce')
df_inst_clean['UGDS_WOMEN'] = pd.to_numeric(df_inst_clean['UGDS_WOMEN'], errors='coerce')
df_inst_clean.dropna(subset=['OPEID6'], inplace=True)
df_inst_clean['OPEID6'] = df_inst_clean['OPEID6'].astype(int)
df_inst_clean.drop_duplicates(subset=['OPEID6'], keep='first', inplace=True)

print(f"Cleaned institution data has {df_inst_clean.shape[0]} unique schools.")

# Merge datasets
df_merged = pd.merge(df_fos_enhanced, df_inst_clean, on='OPEID6', how='left')
print("Merge complete. Final shape:", df_merged.shape)

# --- 图1: 分布直方图 ---
columns_to_describe = ['ROI_EARNINGS_TO_DEBT', 'TUITIONFEE_IN', 'UGDS_WOMEN']
df_merged[columns_to_describe].hist(bins=30, figsize=(18, 5), layout=(1, 3))
plt.tight_layout()
figure_path = figures_dir / 'notebook3' / 'distribution_of_key_numeric_data.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.show()

# --- 图2: 学费 vs ROI 散点 ---
plot_data = df_merged.dropna(subset=['TUITIONFEE_IN', 'ROI_EARNINGS_TO_DEBT'])
plot_data = plot_data[plot_data['TUITIONFEE_IN'] > 0]

plt.figure(figsize=(14, 8))
sns.scatterplot(
    data=plot_data.sample(n=min(5000, len(plot_data)), random_state=42),
    x='TUITIONFEE_IN', y='ROI_EARNINGS_TO_DEBT', hue='CONTROL', alpha=0.7, s=50
)
plt.title('Tuition vs ROI by Institution Type')
plt.xlabel('Annual In-State Tuition ($)')
plt.ylabel('Earnings-to-Debt Ratio (ROI)')
plt.legend(title='Institution Type')
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
figure_path = figures_dir / 'notebook3' / 'tuition_roi.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.show()

print("Correlation tuition vs ROI:", plot_data['TUITIONFEE_IN'].corr(plot_data['ROI_EARNINGS_TO_DEBT']))

# --- 图3: 学费 vs Earnings 散点 ---
earnings_plot_data = df_merged.dropna(subset=['TUITIONFEE_IN', 'EARN_MDN_5YR'])
earnings_plot_data = earnings_plot_data[earnings_plot_data['TUITIONFEE_IN'] > 0]

plt.figure(figsize=(14, 8))
sns.scatterplot(
    data=earnings_plot_data.sample(n=min(5000, len(earnings_plot_data)), random_state=42),
    x='TUITIONFEE_IN', y='EARN_MDN_5YR', hue='CONTROL', alpha=0.7, s=50
)
plt.title('Tuition vs Median Earnings by Institution Type')
plt.xlabel('Annual In-State Tuition ($)')
plt.ylabel('Median Earnings')
plt.legend(title='Institution Type')
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
figure_path = figures_dir / 'notebook3' / 'tuition_earnings.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.show()

print("Correlation tuition vs earnings:", earnings_plot_data['TUITIONFEE_IN'].corr(earnings_plot_data['EARN_MDN_5YR']))

# --- 图4: Earnings by Institution Type 箱线图 ---
box_plot_data = df_merged.dropna(subset=['CONTROL', 'EARN_MDN_5YR'])
order = ['Public', 'Private, nonprofit', 'Private, for-profit']

plt.figure(figsize=(12, 8))
sns.boxplot(
    data=box_plot_data,
    x='CONTROL', y='EARN_MDN_5YR', hue='CONTROL', order=order
)
plt.title('Distribution of Graduate Earnings by Institution Type')
plt.xlabel('Institution Type')
plt.ylabel('Median Earnings 5 Years After Graduation ($)')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, p: f'${int(y/1000):,}K'))
plt.tight_layout()
figure_path = figures_dir / 'notebook3' / 'earnings_by_institution_type.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.show()

# --- 图5: Gender vs ROI ---
df_school_summary = df_merged.groupby('INSTNM').agg(
    avg_roi=('ROI_EARNINGS_TO_DEBT', 'mean'),
    women_proportion=('UGDS_WOMEN', 'first'),
    program_count=('INSTNM', 'size')
).dropna()
df_school_summary = df_school_summary[df_school_summary['program_count'] >= 5]

plt.figure(figsize=(14, 8))
sns.regplot(data=df_school_summary, x='women_proportion', y='avg_roi', scatter_kws={'alpha':0.5})
plt.title('Institutional Gender Composition vs Average ROI')
plt.xlabel('Proportion Women')
plt.ylabel('Average ROI')
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x*100)}%'))
figure_path = figures_dir / 'notebook3' / 'gender_roi.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.show()

print("Correlation women proportion vs ROI:", df_school_summary['women_proportion'].corr(df_school_summary['avg_roi']))

# --- 图6: Gender vs Earnings ---
df_school_summary_extended = df_merged.groupby('INSTNM').agg(
    avg_roi=('ROI_EARNINGS_TO_DEBT', 'mean'),
    avg_earnings=('EARN_MDN_5YR', 'mean'),
    women_proportion=('UGDS_WOMEN', 'first'),
    program_count=('INSTNM', 'size')
).dropna()
df_school_summary_extended = df_school_summary_extended[df_school_summary_extended['program_count'] >= 5]

plt.figure(figsize=(14, 8))
sns.regplot(data=df_school_summary_extended, x='women_proportion', y='avg_earnings', scatter_kws={'alpha':0.5})
plt.title('Institutional Gender Composition vs Average Earnings')
plt.xlabel('Proportion Women')
plt.ylabel('Average Earnings ($)')
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x*100)}%'))
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, p: f'${int(y/1000):,}K'))
figure_path = figures_dir / 'notebook3' / 'gender_earnings.png'
plt.savefig(figure_path, bbox_inches='tight')
plt.show()

print("Correlation women proportion vs earnings:", df_school_summary_extended['women_proportion'].corr(df_school_summary_extended['avg_earnings']))
