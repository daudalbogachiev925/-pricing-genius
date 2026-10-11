def test_health(client):
    assert client.get("/health").json()["status"] == "ok"

def test_add_observation(client):
    r = client.post("/api/ab-data", json={
        "experiment_id": "e1", "price": 100, "quantity": 600})
    assert r.status_code == 201
    assert r.json()["price"] == 100

def test_fit_insufficient(client):
    r = client.post("/api/models/fit", json={"model_type": "linear"})
    assert r.status_code == 400

def test_segments(client):
    r = client.get("/api/simulation/segments")
    assert r.status_code == 200
    assert len(r.json()) == 3
