from __future__ import annotations

import numpy as np

TIER_EDGES = (0.2, 0.5)  # low < 0.2 <= medium < 0.5 <= high
TIER_NAMES = ("low", "medium", "high")


def assign(p: np.ndarray, edges=TIER_EDGES) -> np.ndarray:
    return np.digitize(p, edges)


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return float(c - h), float(c + h)


def tier_table(y: np.ndarray, p: np.ndarray, edges=TIER_EDGES) -> list[dict]:
    t = assign(p, edges)
    rows = []
    for i, name in enumerate(TIER_NAMES):
        m = t == i
        n = int(m.sum())
        k = int(y[m].sum())
        lo, hi = wilson(k, n)
        rows.append(
            {
                "tier": name,
                "n": n,
                "events": k,
                "observed": k / n if n else None,
                "ci_low": lo,
                "ci_high": hi,
                "mean_pred": float(p[m].mean()) if n else None,
            }
        )
    return rows


def tier_agreement(P: np.ndarray, edges=TIER_EDGES) -> np.ndarray:
    """P: (n_models, n_patients) predictions -> per-patient share of models in the modal tier."""
    T = assign(P, edges)
    out = np.empty(P.shape[1])
    for j in range(P.shape[1]):
        out[j] = np.bincount(T[:, j], minlength=3).max() / P.shape[0]
    return out
