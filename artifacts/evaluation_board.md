# Evaluation Board

**Optimization Target:** Maximize Validation Top-K Masked Skill Accuracy 
**Locked Test Set:** `data/locked_test/test_sample.csv`

| Phase | Model Architecture | Metric: Top-K Accuracy | Runtime Budget | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline** | Static ARM | 56.90% | 1.11s | Current Best Result.  |
| **Agent Dry Run** | TF-IDF (1k) + KMeans (100) | 47.43% | 0.13s | Agent successfully utilized cluster mapping, but has not yet surpassed the ARM baseline. |
| **Agent Controlled Experiment (Phase 1)** | **Extra Trees Ensemble** | **0.6601** | **2026-05-02** | **Phase 1 Experiment Winner (2000 features)** |
| **Agent Controlled Experiment (Phase 2)** | MoE: Confident Expert Routing | 0.6579 | 2026-05-11 | Phase 2 Peak. Failed to beat global baseline. |
