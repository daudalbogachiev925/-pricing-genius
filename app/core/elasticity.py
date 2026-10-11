from app.core.demand import predict

def point_elasticity(model: dict, price: float, eps: float = 0.5) -> float:
    q1 = predict(model, price)
    q2 = predict(model, price + eps)
    if q1 <= 0:
        return 0.0
    return ((q2 - q1) / q1) / (eps / price)

def curve(model: dict, prices) -> list:
    return [{"price": float(p), "elasticity": float(point_elasticity(model, float(p)))}
            for p in prices]
