# Business Requirements Specification – RiskStrat

| ID | Requirement |
|----|-------------|
| BR-1 | Turn a predicted mortality risk into three tiers (<0.2, 0.2–0.5, >=0.5) and report the observed event rate with a confidence interval in each tier. |
| BR-2 | Measure how reproducible a patient's tier is across resampled model fits. |
| BR-3 | Compare uncalibrated and sigmoid-calibrated logistic regression, random forest and gradient boosting. |
| BR-4 | Report real-data results only; no clinical-utility claim. |

Out of scope: external validation, time-to-event modelling, deployment.
