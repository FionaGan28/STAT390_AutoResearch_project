# AutoResearch Agent Instructions

## Objective
Maximize the **validation Top-3 Masked Skill Prediction Accuracy** for Data Analyst job postings.

## Rules
1. You may **ONLY** modify `agent_workspace/train_cluster.py` (Note: despite the filename, you are no longer restricted to clustering. You may use any `scikit-learn` algorithm).
2. `src/run.py` and `src/evaluator.py` are **FROZEN** — do not touch them under any circumstances.
3. The function `build_predict_fn(train_df)` inside `train_cluster.py` must return a callable function that takes a list of strings (visible skills) and returns a list of 3 strings (the top predicted masked skills).
4. Training and evaluation must complete in **under 100 seconds** on CPU.
5. No additional data sources or external downloads. 
6. ANTI-TAMPERING RULE: The ExtraTreesClassifier parameters (n_estimators=100, max_depth=30) are strictly FROZEN. Do not secretly downscale the model or your ablation parameters to save compute time. If an ablation run (like trigrams) exceeds the time limit, let it crash/abort, log it as Code Instability, and discard the run.
7. Knowledge Base: When writing or modifying text vectorization code (TfidfVectorizer, CountVectorizer, etc.), you must first read agent_skills/scikit_learn/SKILL.md to ensure your hyperparameters and syntax align with scikit-learn best practices. You may also take inspiration from this knowledge base.

## Workflow: Controlled Experiments
You must conduct experiments one variable at a time to ensure interpretable evidence.

Phase 3: Feature Engineering Ablation (Runs 26-40)
Fixed Variable: The model architecture is strictly locked to the Phase 1 winner: ExtraTreesClassifier(n_estimators=100, max_depth=30, n_jobs=-1, random_state=42). Do not use Mixture of Experts.
Independent Variable: Text vectorization and preprocessing.
Ablation Strategy: Systematically stack or remove text processing techniques to measure their isolated impact on both Accuracy and Runtime (Efficiency).
Action: Run .venv/bin/python src/run.py "Phase 3: [Ablation Tweak]". Carefully log the execution time of each run. Revert and log --discard if the score drops, but retain the execution time data for your efficiency analysis.

## Crash Protocol
If any execution of `run.py` crashes with a Python traceback:
1. You must immediately create or append to the file `logs/crash_log.md`.
2. Record the exact error message, the code configuration you tried to run, and the date.
3. Revert your code in `train_cluster.py` to the last working state before attempting a new fix. Do NOT silently ignore crashes.

## What NOT to do
* Do not modify the `data/` directory or attempt to read `data/locked_test/`.
* Do not import libraries outside of `scikit-learn`, `pandas`, and standard Python libraries.