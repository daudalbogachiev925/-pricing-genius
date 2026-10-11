from app.core.elasticity import point_elasticity, curve

def test_elasticity_negative():
    m = {"type": "linear", "intercept": 1000.0, "slope": -4.0}
    e = point_elasticity(m, 100)
    assert e < 0

def test_curve_length():
    m = {"type": "linear", "intercept": 1000.0, "slope": -4.0}
    c = curve(m, [50, 100, 150])
    assert len(c) == 3
