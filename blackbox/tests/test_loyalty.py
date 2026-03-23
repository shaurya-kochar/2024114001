import pytest


def _points(data):
    return int(data.get("points", data.get("loyalty_points", 0)))


def test_get_loyalty(api_client):
    res = api_client.get("/loyalty")
    assert res.status_code == 200
    assert _points(res.json()) >= 0


def test_loyalty_redeem_minimum_one(api_client):
    res = api_client.post("/loyalty/redeem", json={"points": 0})
    assert res.status_code == 400


def test_loyalty_redeem_negative_rejected(api_client):
    res = api_client.post("/loyalty/redeem", json={"points": -5})
    assert res.status_code == 400


def test_loyalty_redeem_insufficient_points(api_client):
    pts = _points(api_client.get("/loyalty").json())
    res = api_client.post("/loyalty/redeem", json={"points": pts + 10000})
    assert res.status_code == 400


@pytest.mark.parametrize("points", ["10", "1.5", None, " "])
def test_loyalty_redeem_points_type_variants_validation(api_client, points):
    res = api_client.post("/loyalty/redeem", json={"points": points})
    assert res.status_code == 400
