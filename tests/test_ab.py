from app.core.ab_test import ab_test

def test_ab_test_significant():
    a = [100, 102, 98, 101, 99]
    b = [50, 48, 52, 51, 49]
    r = ab_test(a, b, 100, 80)
    assert r["significant"] is True
    assert r["winner"] in ("A", "B")

def test_ab_test_no_difference():
    a = [100, 101, 99, 100, 100]
    b = [100, 99, 101, 100, 100]
    r = ab_test(a, b, 100, 100)
    assert r["p_value"] > 0.05
