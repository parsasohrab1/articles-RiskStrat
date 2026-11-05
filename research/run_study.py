"""Heart Failure Clinical Records (UCI 519, n=299, death event): calibrated risk tiers.

usage: python research/run_study.py /path/to/heart_failure_clinical_records_dataset.csv
"""

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from riskstrat.tiers import tier_agreement, tier_table

warnings.filterwarnings("ignore")
MODELS = {
    "logistic": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
    "random_forest": RandomForestClassifier(300, min_samples_leaf=3, random_state=0),
    "grad_boosting": GradientBoostingClassifier(random_state=0),
}


def oof_predictions(model, X, y, calibrate, repeats=10):
    """Out-of-fold probabilities averaged over repeated 5-fold CV."""
    P = np.zeros((repeats, len(y)))
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=repeats, random_state=0)
    for i, (tr, te) in enumerate(cv.split(X, y)):
        m = (
            CalibratedClassifierCV(clone(model), method="sigmoid", cv=3)
            if calibrate
            else clone(model)
        )
        m.fit(X[tr], y[tr])
        P[i // 5, te] = m.predict_proba(X[te])[:, 1]
    return P


def main(path: str):
    df = pd.read_csv(path)
    y = df["DEATH_EVENT"].to_numpy()
    X = df.drop(columns=["DEATH_EVENT", "time"]).to_numpy(
        float
    )  # 'time' = follow-up, leaks outcome
    out = {
        "note": "UCI Heart Failure Clinical Records, real patients, n=299; follow-up 'time' excluded "
        "because it is only known after the outcome; tiers: <0.2, 0.2-0.5, >=0.5",
        "n": len(y),
        "prevalence": float(y.mean()),
        "models": {},
    }
    for name, model in MODELS.items():
        for cal in (False, True):
            P = oof_predictions(model, X, y, cal)
            p = P.mean(axis=0)
            out["models"][f"{name}{'+sigmoid' if cal else ''}"] = {
                "auc": float(np.mean([roc_auc_score(y, r) for r in P])),
                "brier": float(np.mean([brier_score_loss(y, r) for r in P])),
                "tiers_repeat_averaged": tier_table(y, p),
                "tier_agreement_mean_over_repeats": float(np.mean(tier_agreement(P))),
                "share_patients_agreement_ge_0.8": float(np.mean(tier_agreement(P) >= 0.8)),
            }
    Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1))
    for k, v in out["models"].items():
        print(
            k,
            round(v["auc"], 3),
            round(v["brier"], 3),
            round(v["tier_agreement_mean_over_repeats"], 3),
            [
                (
                    t["tier"],
                    t["n"],
                    None if t["observed"] is None else round(t["observed"], 2),
                    None if t["mean_pred"] is None else round(t["mean_pred"], 2),
                )
                for t in v["tiers_repeat_averaged"]
            ],
        )


if __name__ == "__main__":
    main(sys.argv[1])
