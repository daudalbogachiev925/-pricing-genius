import numpy as np
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from typing import List, Tuple

def fit_linear(prices: np.ndarray, quantities: np.ndarray) -> dict:
    X = prices.reshape(-1, 1)
    lr = LinearRegression().fit(X, quantities)
    pred = lr.predict(X)
    r2 = r2_score(quantities, pred)
    n = len(prices)
    rss = float(((quantities - pred) ** 2).sum())
    aic = n * np.log(rss / n + 1e-9) + 2 * 2
    return {
        "type": "linear",
        "intercept": float(lr.intercept_),
        "slope": float(lr.coef_[0]),
        "r_squared": float(r2),
        "aic": float(aic),
    }

def _log_log(p, a, b):
    return a * np.power(p, -b)

def fit_log_log(prices: np.ndarray, quantities: np.ndarray) -> dict:
    popt, _ = curve_fit(_log_log, prices, quantities, p0=(1e5, 1.5), maxfev=10000)
    pred = _log_log(prices, *popt)
    r2 = r2_score(quantities, pred)
    n = len(prices)
    rss = float(((quantities - pred) ** 2).sum())
    aic = n * np.log(rss / n + 1e-9) + 2 * 2
    return {
        "type": "log_log",
        "a": float(popt[0]),
        "b": float(popt[1]),
        "r_squared": float(r2),
        "aic": float(aic),
    }

def predict(model: dict, price: float) -> float:
    if model["type"] == "linear":
        return max(0.0, model["intercept"] + model["slope"] * price)
    if model["type"] == "log_log":
        return max(0.0, model["a"] * (price ** -model["b"]))
    raise ValueError("Unknown model")
