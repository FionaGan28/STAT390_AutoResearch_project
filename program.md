# AutoResearch Agent Instructions

## Objective
Maximize the **validation Top-3 Masked Skill Prediction Accuracy** for Data Analyst job postings.

## Rules
1. You may **ONLY** modify `agent_workspace/train_cluster.py`.
2. `src/run.py` and `src/evaluator.py` are **FROZEN** — do not touch them under any circumstances.
3. The function `build_predict_fn(train_df)` inside `train_cluster.py` must return a callable function that takes a list of strings (visible skills) and returns a list of 3 strings (the top predicted masked skills).
4. Training and evaluation must complete in **under 60 seconds** on CPU.
5. No additional data sources or external downloads. 

## Workflow
1. Read the current `agent_workspace/train_cluster.py`.
2. Propose a structural modification to the clustering or feature engineering logic.
3. Edit `train_cluster.py`.
4. Run the evaluation: `python src/run.py "description of what you changed"`
5. Check the `val_accuracy` in the terminal output.
6. If improved: KEEP the change. (Log your reasoning).
7. If worse: REVERT `train_cluster.py` to the previous working version. (Run `python src/run.py "reverted to previous" --discard`).
8. Repeat from step 1.

## Ideas to explore
* **Feature Engineering:** Try `TfidfVectorizer` instead of `CountVectorizer`. Adjust `max_features`, `ngram_range`, or `min_df`.
* **Clustering Hyperparameters:** Test different `n_clusters` (K values) to find the optimal taxonomy size for data roles. Try changing `init` methods or `max_iter`.
* **Alternative Clustering:** If K-Means plateaus, try `MiniBatchKMeans` or other scalable sklearn clustering algorithms. 
* **Prediction Logic:** Improve the logic inside the nested `predict_masked_skill` function to utilize the cluster centers more intelligently.

## What NOT to do
* Do not modify the `data/` directory or attempt to read `data/locked_test/`.
* Do not import libraries outside of `scikit-learn`, `pandas`, and standard Python libraries.