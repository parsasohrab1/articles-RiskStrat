# TRL assessment – RiskStrat

**Claimed level: TRL 4** (laboratory validation on one public real dataset). Not TRL 5: no external cohort, no clinical setting.

Data: UCI Heart Failure Clinical Records, n = 299, event prevalence 0.321. Out-of-fold results, 10 x 5-fold CV.

Tier cells show: n / observed event rate (Wilson 95 % CI) / mean predicted risk.

| Model | AUC | Brier | Low | Medium | High | Mean tier agreement | Patients with agreement >= 0.8 |
|---|---|---|---|---|---|---|---|
| logistic | 0.766 | 0.177 | 114 / 0.12 (0.07–0.20) / 0.10 | 117 / 0.32 (0.25–0.41) / 0.33 | 68 / 0.65 (0.53–0.75) / 0.67 | 0.91 | 0.84 |
| logistic+sigmoid | 0.765 | 0.178 | 82 / 0.09 (0.04–0.17) / 0.13 | 166 / 0.33 (0.26–0.41) / 0.33 | 51 / 0.67 (0.53–0.78) / 0.62 | 0.92 | 0.85 |
| random_forest | 0.792 | 0.166 | 119 / 0.09 (0.05–0.16) / 0.13 | 110 / 0.38 (0.30–0.48) / 0.33 | 70 / 0.61 (0.50–0.72) / 0.62 | 0.88 | 0.75 |
| random_forest+sigmoid | 0.790 | 0.168 | 123 / 0.08 (0.04–0.14) / 0.15 | 109 / 0.39 (0.31–0.49) / 0.33 | 67 / 0.64 (0.52–0.75) / 0.63 | 0.89 | 0.80 |
| grad_boosting | 0.746 | 0.196 | 147 / 0.14 (0.09–0.20) / 0.08 | 77 / 0.38 (0.28–0.49) / 0.34 | 75 / 0.63 (0.51–0.73) / 0.74 | 0.83 | 0.68 |
| grad_boosting+sigmoid | 0.773 | 0.179 | 71 / 0.10 (0.05–0.19) / 0.17 | 187 / 0.33 (0.27–0.40) / 0.32 | 41 / 0.66 (0.51–0.78) / 0.58 | 0.85 | 0.74 |

## Findings and caveats
- All models separate tiers monotonically: observed event rate ~0.08–0.14 (low), ~0.32–0.39 (medium), ~0.61–0.67 (high).
- AUC 0.75–0.79: modest discrimination; random forest is best, logistic regression is almost as good and the most stable (mean tier agreement 0.91).
- Uncalibrated gradient boosting is over-confident at the extremes (high-tier mean prediction 0.74 vs observed 0.63); sigmoid calibration fixes much of that and moves many patients into the medium tier.
- Tier membership is not reproducible for every patient: 15–16 % of patients (logistic) and 20–25 % (random forest) fall in the modal tier in fewer than 80 % of the 10 repeated fits; gradient boosting is worst (26–32 %).
- Tier tables use repeat-averaged predictions, which are smoother than a single model's; a single-fit tier would be less stable.
- n = 299 single-source patients, 96 events; intervals are wide and there is no external validation.
