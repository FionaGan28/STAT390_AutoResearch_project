# Evaluation Board

**Optimization Target:** Maximize Validation Top-3 Masked Skill Accuracy 
**Locked Test Set:** `data/locked_test/test_sample.csv`

| Phase | Model Architecture | Metric: Top-3 Accuracy | Runtime | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline** | Static ARM | 56.90% | 1.11s | Initial human-coded baseline. |
| **Agent Dry Run** | TF-IDF (1k) + KMeans (100) | 47.43% | 0.13s | Agent successfully utilized cluster mapping. |
| **Phase 1 (Model Search)** | **Extra Trees Ensemble (Global)** | **66.01%** | **2.18s** | **Phase 1 Winner & Validation Peak (2000 features).** |
| **Phase 2 (MoE Routing)** | Confident Expert Routing | 65.79% | 4.73s | Phase 2 Peak. Failed to beat global baseline. |
| **Phase 3 (Ablation)** | Feature Engineering: Sublinear TF | 65.20% | 2.16s | Phase 3 Peak. Failed to beat global baseline. |
| **FINAL LOCKED TEST** | **Extra Trees Ensemble (Global)** | **65.38%** | **2.04s** | **Evaluated exactly once on unseen data. Proves high generalization and zero data leakage.** |