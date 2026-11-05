import numpy as np

from riskstrat.tiers import assign, tier_agreement, tier_table, wilson


def test_assign_edges():
    assert list(assign(np.array([0.0, 0.19, 0.2, 0.49, 0.5, 1.0]))) == [0, 0, 1, 1, 2, 2]


def test_wilson_contains_point_and_is_ordered():
    lo, hi = wilson(30, 100)
    assert lo < 0.3 < hi and 0 <= lo and hi <= 1


def test_tier_table_counts_sum_to_n():
    rng = np.random.default_rng(0)
    p = rng.uniform(size=500)
    y = (rng.uniform(size=500) < p).astype(int)
    rows = tier_table(y, p)
    assert sum(r["n"] for r in rows) == 500
    assert rows[0]["observed"] < rows[2]["observed"]


def test_agreement_is_one_when_models_identical():
    P = np.tile(np.array([0.1, 0.3, 0.7]), (5, 1))
    assert (tier_agreement(P) == 1.0).all()
