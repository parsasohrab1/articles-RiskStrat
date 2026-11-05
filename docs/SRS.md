# Software Requirements Specification – RiskStrat

- SR-1 `tiers.assign` maps probabilities to tiers with fixed edges (0.2, 0.5).
- SR-2 `tiers.tier_table` returns per-tier n, events, observed rate, Wilson 95 % interval and mean prediction.
- SR-3 `tiers.tier_agreement` returns, per patient, the share of repeated fits that put the patient in the modal tier.
- SR-4 `research/run_study.py`: 10 x repeated stratified 5-fold CV; out-of-fold predictions per repeat; optional sigmoid calibration (3-fold inside the training folds); the follow-up variable `time` is excluded because it is only known after the outcome.
- SR-5 Tier tables use predictions averaged over the 10 repeats (a smoothed prediction); AUC and Brier are the mean of the per-repeat values.
- SR-6 Four unit tests.
