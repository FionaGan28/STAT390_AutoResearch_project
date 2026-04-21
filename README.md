# STAT390_AutoResearch_project

**Project Summary:** This project investigates job title inflation by utilizing an AutoResearch agent to cluster data-related professions based purely on required technical skills, rather than employer-given titles.

**Data:** 5,000-row deterministic sample of the Kaggle "Data Analyst Job Postings" dataset. 
**Method:** Human-coded Association Rule Mining (Baseline) vs. Agent-driven K-Means Clustering (AutoResearch). 
**Metric:** Top-K Masked Skill Prediction Accuracy (default Top-3). 
**Current Best Result:** 56.90% (Baseline ARM)

## How to Run the Pipeline
To reproduce the deterministic data split and run the baseline evaluator end-to-end:
1. Generate the Train/Test split (Raw data exceeds file size for git. Download raw data file from Kaggle, or use the generated test and train sets.Running again would not change the existent data in data/):
   `python src/data_loader.py`
2. Run the baseline model and evaluation:
   `python src/baseline_arm.py`