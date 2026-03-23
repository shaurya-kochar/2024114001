import pytest


def _first_product_id(api_client):
    res = api_client.get("/products")
    assert res.status_code == 200
    products = res.json()
    if not products:
        pytest.skip("No products available")
    return products[0]["product_id"]


def test_reviews_get(api_client):
    pid = _first_product_id(api_client)
    res = api_client.get(f"/products/{pid}/reviews")
    assert res.status_code == 200
    data = res.json()
    assert "average_rating" in data
    assert "reviews" in data


def test_reviews_reject_rating_out_of_range(api_client):
    pid = _first_product_id(api_client)
    res = api_client.post(f"/products/{pid}/reviews", json={"rating": 6, "comment": "too high"})
    assert res.status_code == 400


def test_reviews_reject_empty_comment(api_client):
    pid = _first_product_id(api_client)
    res = api_client.post(f"/products/{pid}/reviews", json={"rating": 4, "comment": ""})
    assert res.status_code == 400


def test_reviews_reject_comment_over_200(api_client):
    pid = _first_product_id(api_client)
    long_comment = "a" * 201
    res = api_client.post(f"/products/{pid}/reviews", json={"rating": 4, "comment": long_comment})
    assert res.status_code == 400


def test_reviews_average_in_range(api_client):
    pid = _first_product_id(api_client)
    api_client.post(f"/products/{pid}/reviews", json={"rating": 4, "comment": "good"})
    api_client.post(f"/products/{pid}/reviews", json={"rating": 5, "comment": "great"})
    res = api_client.get(f"/products/{pid}/reviews")
    assert res.status_code == 200
    avg = float(res.json().get("average_rating", 0))
    assert 0.0 <= avg <= 5.0


def _product_with_no_reviews(api_client):
    products = api_client.get("/products").json()
    for p in products:
        pid = p["product_id"]
        res = api_client.get(f"/products/{pid}/reviews")
        if res.status_code == 200 and res.json().get("reviews") == []:
            return pid
    pytest.skip("No product with empty reviews found")


@pytest.mark.xfail(reason="Bug: average rating rounded down instead of decimal")
def test_reviews_average_decimal_precision(api_client):
    pid = _product_with_no_reviews(api_client)

    a = api_client.post(f"/products/{pid}/reviews", json={"rating": 4, "comment": "r4"})
    b = api_client.post(f"/products/{pid}/reviews", json={"rating": 5, "comment": "r5"})
    assert a.status_code in (200, 201)
    assert b.status_code in (200, 201)

    res = api_client.get(f"/products/{pid}/reviews")
    assert res.status_code == 200
    avg = float(res.json().get("average_rating", 0))
    assert avg == 4.5


@pytest.mark.parametrize("rating", [0, -1, 6, "5", "bad", None, 3.5])
def test_reviews_rating_type_and_range_variants_validation(api_client, rating):
    pid = _first_product_id(api_client)
    res = api_client.post(
        f"/products/{pid}/reviews",
        json={"rating": rating, "comment": "variant comment"},
    )
    assert res.status_code == 400
