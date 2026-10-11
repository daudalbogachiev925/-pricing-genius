from typing import List, Dict

DEFAULT_SEGMENTS = [
    {"name": "economy", "willingness": 70, "size": 0.4, "unit_cost": 30},
    {"name": "mid", "willingness": 130, "size": 0.4, "unit_cost": 35},
    {"name": "premium", "willingness": 220, "size": 0.2, "unit_cost": 45},
]

def segment_optimal(segments: List[Dict]) -> List[Dict]:
    out = []
    for s in segments:
        # монопольная цена на линейной функции спроса
        price = s["willingness"] * 0.7
        q = max(0.0, 1000 - 4 * price)
        revenue = price * q * s["size"]
        profit = (price - s["unit_cost"]) * q * s["size"]
        out.append({
            "segment": s["name"],
            "optimal_price": round(price, 2),
            "quantity": round(q, 1),
            "revenue": round(revenue, 2),
            "profit": round(profit, 2),
        })
    return out
