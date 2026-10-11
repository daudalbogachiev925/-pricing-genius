from scipy import stats
import numpy as np

def ab_test(quantities_a: list, quantities_b: list,
            price_a: float, price_b: float) -> dict:
    a = np.asarray(quantities_a, dtype=float)
    b = np.asarray(quantities_b, dtype=float)
    t, p = stats.ttest_ind(a, b, equal_var=False)

    rev_a = price_a * a.mean()
    rev_b = price_b * b.mean()
    winner = "A" if rev_a > rev_b else "B"
    return {
        "revenue_a": float(rev_a),
        "revenue_b": float(rev_b),
        "t_stat": float(t),
        "p_value": float(p),
        "significant": bool(p < 0.05),
        "winner": winner,
    }
