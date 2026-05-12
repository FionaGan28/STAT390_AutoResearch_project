# AutoResearch Agent Instructions

## Objective
Maximize the **validation Top-3 Masked Skill Prediction Accuracy** for Data Analyst job postings.

## Rules
1. You may **ONLY** modify `agent_workspace/train_cluster.py` (Note: despite the filename, you are no longer restricted to clustering. You may use any `scikit-learn` algorithm).
2. `src/run.py` and `src/evaluator.py` are **FROZEN** — do not touch them under any circumstances.
3. The function `build_predict_fn(train_df)` inside `train_cluster.py` must return a callable function that takes a list of strings (visible skills) and returns a list of 3 strings (the top predicted masked skills).
4. Training and evaluation must complete in **under 100 seconds** on CPU.
5. No additional data sources or external downloads. 
6. **ANTI-TAMPERING RULE**: The TfidfVectorizer (max_features=2000) and ExtraTreesClassifier parameters (n_estimators=100, max_depth=30) are strictly FROZEN. Do not secretly downscale these parameters to afford the compute time for your routing architecture. If your combined routing logic + Extra Trees pipeline pushes the total runtime over 100 seconds, abort, log it as Code Instability, and discard the run.

## Workflow: Controlled Experiments
You must conduct experiments one variable at a time to ensure interpretable evidence.

**Phase 2: Mixture of Experts / Routing Architecture (Runs 11-20)**
* **Fixed Variable:** The terminal prediction model MUST be the exact architecture from Phase 1: `ExtraTreesClassifier(n_estimators=100, max_depth=30, n_jobs=-1, random_state=42)`. You may instantiate multiple copies of this exact model if your architecture requires it.
* **Independent Variable:** The routing mechanism, clustering, or data partitioning strategy used *before* the Extra Trees model trains/predicts. Change exactly ONE routing strategy per run.
    * *Examples to explore:* K-Means routing, Gaussian Mixture Models, DBSCAN, rule-based heuristics, or training separate Extra Trees models for different subsets of the data.
* **Action:** Run `.venv/bin/python src/run.py "Phase 2: [Specific Routing Strategy]"`. If the score drops, revert the code using `.venv/bin/python src/run.py "reverted to previous" --discard`. Keep the code state that achieves the highest accuracy.

## Crash Protocol
If any execution of `run.py` crashes with a Python traceback:
1. You must immediately create or append to the file `logs/crash_log.md`.
2. Record the exact error message, the code configuration you tried to run, and the date.
3. Revert your code in `train_cluster.py` to the last working state before attempting a new fix. Do NOT silently ignore crashes.

## What NOT to do
* Do not modify the `data/` directory or attempt to read `data/locked_test/`.
* Do not import libraries outside of `scikit-learn`, `pandas`, and standard Python libraries.