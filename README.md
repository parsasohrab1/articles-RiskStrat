# articles-RiskStrat

Calibrated patient risk tiers (low / medium / high) and their **stability across repeated cross-validation**,
on real data: UCI Heart Failure Clinical Records (n = 299, death event). TRL 4 (public real data, laboratory validation only).

```
pip install -e ".[dev]" && python -m pytest
# data: https://archive.ics.uci.edu/dataset/519 (not committed)
python research/run_study.py /path/to/heart_failure_clinical_records_dataset.csv
```
