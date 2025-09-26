# College ROI & Fairness — Data Storytelling

[![CI](https://github.com/<USER>/<REPO>/actions/workflows/ci.yml/badge.svg)](./actions) 
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**What’s this?**  
Quantifying the *return-on-investment (ROI)* of US college majors using the Dept. of Education’s **College Scorecard**, and exploring equity gaps by gender/race. Public-facing visuals + fully reproducible code.

## 1) Project Overview
- **Question:** Which majors pay back fastest (debt vs early-career earnings)? How does ROI vary by institution, gender, race?
- **Audience:** Students & parents deciding on majors; educators & policy folks.
- **Deliverables:** Blog/Infographic + 8-min talk + this repo.

## 2) Data & Citation
- **College Scorecard** (primary)  
- Optional: **IPEDS** (demographics, tuition), **BLS OES** (wages), **BLS Projections** (growth).  
See `data_card.md` for fields, caveats, ethics.

## 3) Reproduce
```bash
# 1) create env
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) get sample data & run minimal pipeline
make data_sample
make eda
make figures
