import pytest


def _admin_products(api_client):
    res = api_client.get("/admin/products")
    assert res.status_code == 200
    return res.json()


def _first_in_stock_product(api_client):
    for p in _admin_products(api_client):
        if p.get("is_active", True) and p.get("stock_quantity", 0) > 1:
            return p
    pytest.skip("No in-stock active products")


def _prepare_cart(api_client, quantity=1):
    api_client.delete("/cart/clear")
    p = _first_in_stock_product(api_client)
    add = api_client.post("/cart/add", json={"product_id": p["product_id"], "quantity": quantity})
    assert add.status_code == 200
    return p


def test_checkout_rejects_invalid_payment_method(reset_cart, api_client):
    _prepare_cart(api_client)
    res = api_client.post("/checkout", json={"payment_method": "UPI"})
    assert res.status_code == 400


def test_checkout_rejects_empty_cart(reset_cart, api_client):
    api_client.delete("/cart/clear")
    res = api_client.post("/checkout", json={"payment_method": "COD"})
    assert res.status_code == 400


def test_checkout_card_starts_paid(reset_cart, api_client):
    _prepare_cart(api_client)
    res = api_client.post("/checkout", json={"payment_method": "CARD"})
    assert res.status_code == 200
    status = res.json().get("payment_status")
    assert status == "PAID"


@pytest.mark.xfail(reason="Bug: COD checkout starts as PAID instead of PENDING")
def test_checkout_cod_starts_pending(reset_cart, api_client):
    _prepare_cart(api_client)
    res = api_client.post("/checkout", json={"payment_method": "COD"})
    assert res.status_code == 200
    status = res.json().get("payment_status")
    assert status == "PENDING"


@pytest.mark.xfail(reason="Bug: WALLET checkout starts as PAID instead of PENDING")
def test_checkout_wallet_starts_pending(reset_cart, api_client):
    _prepare_cart(api_client)
    res = api_client.post("/checkout", json={"payment_method": "WALLET"})
    assert res.status_code == 200
    status = res.json().get("payment_status")
    assert status == "PENDING"


def test_checkout_cod_over_5000_rejected(reset_cart, api_client):
    api_client.delete("/cart/clear")
    add = api_client.post("/cart/add", json={"product_id": 5, "quantity": 25})
    assert add.status_code == 200

    res = api_client.post("/checkout", json={"payment_method": "COD"})
    assert res.status_code == 400


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"payment_method": ""},
        {"payment_method": " "},
        {"payment_method": "card"},
        {"payment_method": "NETBANKING"},
        {"payment_method": None},
        {"payment_method": 123},
    ],
)
def test_checkout_payment_method_variants_validation(reset_cart, api_client, payload):
    _prepare_cart(api_client)
    res = api_client.post("/checkout", json=payload)
    assert res.status_code == 400
