import pytest


def _admin_products(api_client):
    res = api_client.get("/admin/products")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    return data


def _user_products(api_client, **params):
    res = api_client.get("/products", params=params or None)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    return data


def test_get_products_only_active(api_client):
    admin_products = _admin_products(api_client)
    user_products = _user_products(api_client)

    inactive_ids = {p["product_id"] for p in admin_products if not p.get("is_active", True)}
    user_ids = {p["product_id"] for p in user_products}

    assert user_ids.isdisjoint(inactive_ids)


def test_get_product_by_invalid_id(api_client):
    res = api_client.get("/products/999999")
    assert res.status_code == 404


@pytest.mark.xfail(reason="Bug: product price differs between /products and /admin/products")
def test_product_price_matches_admin_data(api_client):
    admin_products = _admin_products(api_client)
    expected_price = {p["product_id"]: p["price"] for p in admin_products}

    user_products = _user_products(api_client)
    for p in user_products:
        assert p["price"] == expected_price[p["product_id"]]


def test_products_sort_price_ascending(api_client):
    data = _user_products(api_client, sort="price_asc")
    prices = [p["price"] for p in data]
    assert prices == sorted(prices)


def test_products_sort_price_descending(api_client):
    data = _user_products(api_client, sort="price_desc")
    prices = [p["price"] for p in data]
    assert prices == sorted(prices, reverse=True)


def test_products_filter_by_category(api_client):
    products = _user_products(api_client)
    if not products:
        pytest.skip("No active products available")

    category = products[0].get("category")
    if not category:
        pytest.skip("No category field in products")

    filtered = _user_products(api_client, category=category)
    assert all(p.get("category") == category for p in filtered)


def test_products_search_by_name(api_client):
    products = _user_products(api_client)
    if not products:
        pytest.skip("No active products available")

    name = products[0].get("name", "")
    if len(name) < 2:
        pytest.skip("No searchable product name")

    needle = name[:2]
    searched = _user_products(api_client, search=needle)
    assert all(needle.lower() in p.get("name", "").lower() for p in searched)


@pytest.mark.parametrize("sort_value", ["", "PRICE_ASC", "drop table", "null", "random"])
def test_products_sort_variants_do_not_500(api_client, sort_value):
    res = api_client.get("/products", params={"sort": sort_value})
    assert res.status_code in (200, 400)
    if res.status_code == 200:
        assert isinstance(res.json(), list)


@pytest.mark.parametrize("search_value", ["", " ", "a", "A", "@#$%", "x" * 120])
def test_products_search_variants_do_not_500(api_client, search_value):
    res = api_client.get("/products", params={"search": search_value})
    assert res.status_code in (200, 400)
    if res.status_code == 200:
        assert isinstance(res.json(), list)
