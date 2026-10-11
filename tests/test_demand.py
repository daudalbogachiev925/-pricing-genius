import numpy as np
from app.core.demand import fit_linear, fit_log_log, predict

def test_fit_linear_perfect():
    prices = np.array([50.0, 100.0, 150.0, 200.0])
    q = 1000 - 4 * prices
    m = fit_linear(prices, q)
    assert abs(m["slope"] - (-4.0)) < 0.1
    assert m["r_squared"] > 0.99

def test_predict_linear():
    m = {"type": "linear", "intercept": 1000.0, "slope": -4.0}
    assert predict(m, 100) == 600.0
    assert predict(m, 1000) == 0.0

def test_predict_log_log():
    m = {"type": "log_log", "a": 1e5, "b": 1.5}
    assert predict(m, 100) > 0
