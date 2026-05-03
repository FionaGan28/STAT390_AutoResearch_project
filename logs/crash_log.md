# Crash Log
- **Error:** `TypeError: Sparse data was passed, but dense data is required. Use '.toarray()' to convert to a dense numpy array.`
- **Configuration:** Ridge Regression with sparse `Y_top`.
- **Date:** 2026-05-02
- **Traceback:**
```
  File "/Users/fionagan/Desktop/NU/Courses/Spring_2026/STAT390/STAT390_AutoResearch_project/agent_workspace/train_cluster.py", line 50, in build_predict_fn
    model.fit(X, Y_top)
...
TypeError: Sparse data was passed, but dense data is required. Use '.toarray()' to convert to a dense numpy array.
```

- **Error:** Timeout Error / Code Instability
- **Configuration:** Bagging Naive Bayes (OneVsRest with BaggingClassifier)
- **Date:** 2026-05-02
- **Description:** Run manually aborted because it exceeded the 60-second runtime budget.
