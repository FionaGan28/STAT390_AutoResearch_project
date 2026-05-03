# AutoResearch Agent Instructions

## Objective
Maximize the **validation Top-3 Masked Skill Prediction Accuracy** for Data Analyst job postings.

## Rules
1. You may **ONLY** modify `agent_workspace/train_cluster.py` (Note: despite the filename, you are no longer restricted to clustering. You may use any `scikit-learn` algorithm).
2. `src/run.py` and `src/evaluator.py` are **FROZEN** — do not touch them under any circumstances.
3. The function `build_predict_fn(train_df)` inside `train_cluster.py` must return a callable function that takes a list of strings (visible skills) and returns a list of 3 strings (the top predicted masked skills).
4. Training and evaluation must complete in **under 60 seconds** on CPU.
5. No additional data sources or external downloads. 
6. **ANTI-TAMPERING RULE:** Do not alter `max_features` (must stay at 2000) or any vectorizer settings to save compute time. If a model exceeds 60 seconds, let it crash or be manually aborted, and log it as a Code Instability timeout.

## Workflow: Controlled Experiments
You must conduct experiments one variable at a time to ensure interpretable evidence.

**Phase 1: Model Axis Exploration (Runs 1-10)**
* **Fixed Variable:** Use `TfidfVectorizer(max_features=2000, token_pattern=r"\S+")` and a standard prediction mapping logic. Do not change the feature engineering.
* **Independent Variable:** Test 5 completely different model architectures (e.g., Random Forest, KNN, Logistic Regression, Naive Bayes). 
* **Action:** Run `.venv/bin/python src/run.py "Phase 1: [Model Name]"`. If the score drops, revert using `.venv/bin/python src/run.py "reverted to previous" --discard`. Keep the model that achieves the highest accuracy.

## Crash Protocol
If any execution of `run.py` crashes with a Python traceback:
1. You must immediately create or append to the file `logs/crash_log.md`.
2. Record the exact error message, the code configuration you tried to run, and the date.
3. Revert your code in `train_cluster.py` to the last working state before attempting a new fix. Do NOT silently ignore crashes.

## What NOT to do
* Do not modify the `data/` directory or attempt to read `data/locked_test/`.
* Do not import libraries outside of `scikit-learn`, `pandas`, and standard Python libraries.