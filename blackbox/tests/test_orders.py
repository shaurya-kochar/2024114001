import pytest


def _admin_products(api_client):
    res = api_client.get("/admin/products")
    assert res.status_code == 200
    return res.json()


def _stock_of(api_client, product_id):
    for p in _admin_products(api_client):
        if p.get("product_id") == product_id:
            return int(p["stock_quantity"])
    pytest.skip("Product not found")


def _place_order(api_client, product_id=1, quantity=1, payment_method="CARD"):
    api_client.delete("/cart/clear")
    add = api_client.post("/cart/add", json={"product_id": product_id, "quantity": quantity})
    assert add.status_code == 200
    res = api_client.post("/checkout", json={"payment_method": payment_method})
    assert res.status_code == 200
    return int(res.json()["order_id"])


def test_orders_list_and_get_by_id(api_client):
    order_id = _place_order(api_client, product_id=1, quantity=1)

    orders = api_client.get("/orders")
    assert orders.status_code == 200
    order_ids = {o.get("order_id") for o in orders.json()}
    assert order_id in order_ids

    detail = api_client.get(f"/orders/{order_id}")
    assert detail.status_code == 200
    assert detail.json().get("order_id") == order_id


def test_cancel_missing_order_returns_404(api_client):
    res = api_client.post("/orders/999999/cancel")
    assert res.status_code == 404


def test_invoice_has_consistent_totals(api_client):
    order_id = _place_order(api_client, product_id=1, quantity=2)
    inv = api_client.get(f"/orders/{order_id}/invoice")
    assert inv.status_code == 200

    data = inv.json()
    subtotal = float(data.get("subtotal", 0))
    gst = float(data.get("gst", data.get("gst_amount", 0)))
    total = float(data.get("total", data.get("total_amount", 0)))
    assert round(subtotal + gst, 2) == round(total, 2)


@pytest.mark.xfail(reason="Bug: cancelled order does not restore product stock")
def test_cancel_order_restores_stock(api_client):
    product_id = 1
    before = _stock_of(api_client, product_id)
    order_id = _place_order(api_client, product_id=product_id, quantity=2)

    cancel = api_client.post(f"/orders/{order_id}/cancel")
    assert cancel.status_code == 200

    after = _stock_of(api_client, product_id)
    assert after == before


@pytest.mark.xfail(reason="Bug: delivered orders can still be cancelled")
def test_cancel_delivered_order_rejected_if_present(api_client):
    orders = api_client.get("/orders")
    assert orders.status_code == 200
    delivered = [o for o in orders.json() if o.get("order_status") == "DELIVERED"]
    if not delivered:
        pytest.skip("No delivered order for this user")

    order_id = delivered[0]["order_id"]
    res = api_client.post(f"/orders/{order_id}/cancel")
    assert res.status_code == 400


@pytest.mark.parametrize("bad_id", ["abc", "1.5", " ", "-1"])
def test_order_endpoints_invalid_id_format_variants(api_client, bad_id):
    get_res = api_client.get(f"/orders/{bad_id}")
    cancel_res = api_client.post(f"/orders/{bad_id}/cancel")
    invoice_res = api_client.get(f"/orders/{bad_id}/invoice")

    assert get_res.status_code in (400, 404)
    assert cancel_res.status_code in (400, 404)
    assert invoice_res.status_code in (400, 404)
