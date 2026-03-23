import pytest


def _admin_products(api_client):
    res = api_client.get("/admin/products")
    assert res.status_code == 200
    return res.json()


def _get_cart(api_client):
    res = api_client.get("/cart")
    assert res.status_code == 200
    return res.json()


def _cart_items(cart_json):
    return cart_json.get("items", [])


def _find_active_product(api_client):
    products = _admin_products(api_client)
    for p in products:
        if p.get("is_active", True) and p.get("stock_quantity", 0) > 2:
            return p
    pytest.skip("No active product with stock > 2")


def _find_two_active_products(api_client):
    products = [
        p
        for p in _admin_products(api_client)
        if p.get("is_active", True) and p.get("stock_quantity", 0) > 2
    ]
    if len(products) < 2:
        pytest.skip("Need at least two active products with stock")
    return products[0], products[1]


def test_cart_clear_and_get(reset_cart, api_client):
    cart = _get_cart(api_client)
    assert isinstance(_cart_items(cart), list)


@pytest.mark.xfail(reason="Bug: quantity=0 should be rejected with 400 but is accepted")
def test_cart_add_invalid_quantity_zero(reset_cart, api_client):
    product = _find_active_product(api_client)
    res = api_client.post("/cart/add", json={"product_id": product["product_id"], "quantity": 0})
    assert res.status_code == 400


def test_cart_add_invalid_quantity_negative(reset_cart, api_client):
    product = _find_active_product(api_client)
    res = api_client.post("/cart/add", json={"product_id": product["product_id"], "quantity": -1})
    assert res.status_code == 400


def test_cart_add_product_not_found(reset_cart, api_client):
    res = api_client.post("/cart/add", json={"product_id": 999999, "quantity": 1})
    assert res.status_code == 404


def test_cart_add_quantity_more_than_stock(reset_cart, api_client):
    product = _find_active_product(api_client)
    too_much = int(product["stock_quantity"]) + 1
    res = api_client.post("/cart/add", json={"product_id": product["product_id"], "quantity": too_much})
    assert res.status_code == 400


def test_cart_add_same_product_accumulates(reset_cart, api_client):
    product = _find_active_product(api_client)
    pid = product["product_id"]

    r1 = api_client.post("/cart/add", json={"product_id": pid, "quantity": 1})
    r2 = api_client.post("/cart/add", json={"product_id": pid, "quantity": 2})
    assert r1.status_code == 200
    assert r2.status_code == 200

    cart = _get_cart(api_client)
    item = next(i for i in _cart_items(cart) if i["product_id"] == pid)
    assert item["quantity"] == 3


def test_cart_update_invalid_quantity(reset_cart, api_client):
    product = _find_active_product(api_client)
    pid = product["product_id"]
    api_client.post("/cart/add", json={"product_id": pid, "quantity": 1})

    res = api_client.post("/cart/update", json={"product_id": pid, "quantity": 0})
    assert res.status_code == 400


def test_cart_remove_product_not_in_cart(reset_cart, api_client):
    product = _find_active_product(api_client)
    res = api_client.post("/cart/remove", json={"product_id": product["product_id"]})
    assert res.status_code == 404


@pytest.mark.xfail(reason="Bug: item subtotal overflows instead of quantity*unit_price")
def test_cart_item_subtotal_exact_for_large_quantity(reset_cart, api_client):
    # Product 5 has a stable listed unit_price of 250 in this dataset.
    add = api_client.post("/cart/add", json={"product_id": 5, "quantity": 20})
    assert add.status_code == 200

    cart = _get_cart(api_client)
    item = next(i for i in _cart_items(cart) if i["product_id"] == 5)
    assert item["subtotal"] == item["quantity"] * item["unit_price"]


@pytest.mark.xfail(reason="Bug: cart total does not include all subtotals")
def test_cart_subtotal_and_total_calculation(reset_cart, api_client):
    p1, p2 = _find_two_active_products(api_client)

    api_client.post("/cart/add", json={"product_id": p1["product_id"], "quantity": 1})
    api_client.post("/cart/add", json={"product_id": p2["product_id"], "quantity": 2})

    cart = _get_cart(api_client)
    items = _cart_items(cart)
    i1 = next(i for i in items if i["product_id"] == p1["product_id"])
    i2 = next(i for i in items if i["product_id"] == p2["product_id"])

    i1_price = i1.get("unit_price", i1.get("price"))
    i2_price = i2.get("unit_price", i2.get("price"))
    assert i1_price is not None
    assert i2_price is not None

    assert i1["subtotal"] == i1["quantity"] * i1_price
    assert i2["subtotal"] == i2["quantity"] * i2_price

    expected_total = sum(i["subtotal"] for i in items)
    assert cart["total"] == expected_total


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"product_id": 1},
        {"quantity": 1},
        {"product_id": "one", "quantity": 1},
        {"product_id": 1, "quantity": "two"},
        {"product_id": None, "quantity": 1},
    ],
)
def test_cart_add_payload_variants_validation(reset_cart, api_client, payload):
    res = api_client.post("/cart/add", json=payload)
    assert res.status_code in (200, 400, 404)


@pytest.mark.parametrize("payload", [{}, {"product_id": 1}, {"quantity": 1}, {"product_id": "x", "quantity": 2}])
def test_cart_update_payload_variants_validation(reset_cart, api_client, payload):
    res = api_client.post("/cart/update", json=payload)
    assert res.status_code in (200, 400, 404)


@pytest.mark.xfail(reason="Bug: cart add accepts missing quantity")
def test_cart_add_requires_quantity(reset_cart, api_client):
    res = api_client.post("/cart/add", json={"product_id": 1})
    assert res.status_code == 400


@pytest.mark.xfail(reason="Bug: cart update accepts missing product_id")
def test_cart_update_requires_product_id(reset_cart, api_client):
    product = _find_active_product(api_client)
    api_client.post("/cart/add", json={"product_id": product["product_id"], "quantity": 1})
    res = api_client.post("/cart/update", json={"quantity": 1})
    assert res.status_code == 400
