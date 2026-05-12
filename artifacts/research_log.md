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

### Date: 2026-05-11
* **What I tried:** Executed Phase 2, a 10-run autonomous loop exploring "Mixture of Experts" (MoE) architectures. I locked the Extra Trees model and instructed the agent to test data partitioning and routing strategies (e.g., K-Means routing, Rule-based routing).
* **Why I tried it:** To determine if routing job descriptions to specialized, domain-specific tree ensembles would capture nuance better than a single global model.
* **What happened:** Every MoE architecture resulted in a metric regression (best attempt: 0.6579). The agent successfully executed the rollback protocol 10/10 times, defending the 66.01% baseline. The failure revealed that partitioning sparse text data starves the models of necessary cross-domain context.
* **What comes next:** Phase 3: Feature Engineering. Since model architecture and routing are optimized/exhausted, I will freeze the Extra Trees model and have the agent experiment with `ngram_range`, custom stop-words, and frequency thresholding.