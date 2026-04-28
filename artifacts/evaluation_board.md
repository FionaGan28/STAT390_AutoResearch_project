# Evaluation Board

**Optimization Target:** Maximize Validation Top-K Masked Skill Accuracy 
**Locked Test Set:** `data/locked_test/test_sample.csv`

| Phase | Model Architecture | Metric: Top-K Accuracy | Runtime Budget | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1 (Baseline)** | Static ARM | 56.90% | 1.11s | Current Best Result.  |
| **Phase 2 (Agent Dry Run)** | TF-IDF (1k) + KMeans (100) | 47.43% | 0.13s | Agent successfully utilized cluster mapping, but has not yet surpassed the ARM baseline. |