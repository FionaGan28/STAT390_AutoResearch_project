# Research Log

### Date: 2026-04-21
**What I tried:** Established the frozen data pipeline and ran the static Association Rule Mining (ARM) baseline. 
**Why I tried it:** To establish a fixed evaluation metric (Masked Skill Prediction) and a locked 20% test set before the agent starts its search loop.
* **What happened:** Successfully generated an end-to-end run on the 80% train split. The Top-K Accuracy achieved with the baseline ARM model was 56.9%. The measured runtime per iteration is 1.11 seconds. 
**What comes next:** Translate this evaluation framework into an AutoResearch contract and prompt the agent to edit `train_cluster.py` to beat the ARM baseline.

### Date: 2026-04-28
* **What I tried:** Launched the first AutoResearch loop using the Gemini CLI. Executed a 5-iteration dry run to test the infrastructure.
* **Why I tried it:** To fulfill the Week 3 requirement of experiencing the autonomous loop, identifying failure modes, and ensuring the `evaluator.py` and `run.py` sandbox correctly contained the agent.
* **What happened:** The agent successfully read the instructions, wrote code, and evaluated itself. It improved the Phase 2 naive baseline from 37.44% to a high of 47.43%.
* **What comes next:** Currently, the agent is restricted to K means clustering, which might be why it hasn't beaten the Phase 1 ARM baseline (56.90%). I need to update `program.md` to broaden its search space. I will instruct the agent that it can use any algorithm it wants (ARM, KNN, Random Forests, etc.) as long as it returns the correct prediction function format.

### Date: 2026-05-02
* **What I tried:** Executed a strictly controlled 10-run experiment loop, fixing vectorization.
* **Why I tried it:** To isolate which machine learning architecture performs best on the technical skill dataset while holding feature engineering constant (TF-IDF, 2000 features).
* **What happened:** A major "Agent Misbehavior" event occurred where the agent secretly lowered max_features to 1000 to bypass runtime limits, poisoning the experiment state. After implementing a strict "Anti-Tampering" rule in program.md and resetting the code, a clean run was completed. The Extra Trees Ensemble achieved a new project high of 66.01%, successfully surpassing the human ARM baseline (56.90%).
* **What comes next:** With the model architecture now optimized and frozen at Extra Trees, I will pivot allow more feature engineering options to see if we can push the accuracy toward 70%.

### Date: 2026-05-20
* **What I tried:** Executed Phase 3: Feature Engineering Ablation. Systematically tested `binary=True`, `ngram_range=(1, 2)`, `max_features=5000`, `norm='l1'`, `sublinear_tf=True`, binary `CountVectorizer`, increased target skills (500), `min_df=2`, `stop_words='english'`, and `use_idf=False`.
* **Why I tried it:** To isolate the impact of text preprocessing and vectorization hyperparameters on prediction accuracy while keeping the ExtraTrees model architecture frozen.
* **What happened:** Every modification either resulted in a performance drop or no change. 
    * `binary=True` (0.6505), `ngram_range=(1, 2)` (0.6278), `norm='l1'` (0.6454), `sublinear_tf=True` (0.6520), binary `CountVectorizer` (0.5690), `min_df=2` (0.6417), `stop_words='english'` (0.6057), `use_idf=False` (0.6197).
    * `max_features=5000` and `top_skills=500` maintained 0.6601 but added complexity/runtime.
* **What comes next:** Phase 3 concludes with the baseline configuration (TF-IDF 2000 features, L2 norm, unigrams, with IDF) defended as the optimal setup. The 0.6601 accuracy remains the project high. No further feature engineering gains are expected within the current constraints. Finalizing model for deployment evaluation.