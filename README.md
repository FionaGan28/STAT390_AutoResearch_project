# STAT390_AutoResearch_project

**Project Summary:** This project investigates job title inflation by utilizing an AutoResearch agent to cluster data-related professions based purely on required technical skills, rather than employer-given titles.

* **Data:** 10000-row deterministic sample of the Kaggle "Data Analyst Job Postings [Pay, Skills, Benefits]" dataset ([LINK](https://www.kaggle.com/datasets/lukebarousse/data-analyst-job-postings-google-search)). 

* **Method:** Human-coded Association Rule Mining (Baseline) vs. Agent-driven K-Means Clustering (AutoResearch). 

* *Metric:** Top-K Masked Skill Prediction Accuracy (default Top-3). 

* *Current Best Result: **66.01%** (Extra Trees Ensemble)
   * Phase 1 (Baseline): 56.90% (ARM)
   * Phase 2 (Agent Loop): 66.01% (Extra Trees Ensemble)

## Project Structure

This repository is  partitioned to support a safe autonomous research loop:
* `src/evaluator.py` & `src/run.py`: **FROZEN**. These files load the data and calculate the metric. The agent cannot touch them.
* `agent_workspace/train_cluster.py`: **EDITABLE**. This is the *only* file the agent is allowed to modify.
* `program.md`: The instruction that the agent reads to understand the rules and constraints of the loop.

---

## How to Run the Pipeline

The deterministic 10000-row train and test splits are already generated and included under the `data/` directory.

### 1. Run the Human Baseline (Phase 1)
To verify the initial ARM baseline score:
`python src/baseline_arm.py`

### 2. Run the AutoResearch Loop (Phase 2)
This project uses an AI CLI agent to autonomously rewrite the prediction logic.
After installing and launching the agent, start the loop using the following command:

"Read program.md for your instructions. Read agent_workspace/train_cluster.py. Start the AutoResearch loop and try different modifications to improve the validation accuracy. Explain your reasoning for each keep/discard decision."