import datetime as dt
import pytest


def _admin_products(api_client):
    res = api_client.get("/admin/products")
    assert res.status_code == 200
    return res.json()


def _admin_coupons(api_client):
    res = api_client.get("/admin/coupons")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    return data


def _first_in_stock_product(api_client):
    for p in _admin_products(api_client):
        if p.get("is_active", True) and p.get("stock_quantity", 0) > 0:
            return p
    pytest.skip("No in-stock active products")


def _prepare_cart(api_client):
    api_client.delete("/cart/clear")
    p = _first_in_stock_product(api_client)
    add = api_client.post("/cart/add", json={"product_id": p["product_id"], "quantity": 1})
    assert add.status_code == 200


def _parse_expiry(value):
    if not value:
        return None
    value = str(value)
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return dt.datetime.strptime(value[:19], fmt)
        except ValueError:
            continue
    return None


def test_apply_coupon_invalid_code(reset_cart, api_client):
    _prepare_cart(api_client)
    res = api_client.post("/coupon/apply", json={"coupon_code": "NO_SUCH_COUPON"})
    assert res.status_code in (400, 404)


def test_apply_expired_coupon_rejected(reset_cart, api_client):
    _prepare_cart(api_client)
    now = dt.datetime.now()
    expired = None
    for c in _admin_coupons(api_client):
        exp = _parse_expiry(c.get("expiry_date") or c.get("expires_at") or c.get("expiry"))
        if exp and exp < now:
            expired = c
            break

    if not expired:
        pytest.skip("No expired coupon found in dataset")

    code = expired.get("coupon_code") or expired.get("code")
    if not code:
        pytest.skip("Expired coupon has no visible code field")

    res = api_client.post("/coupon/apply", json={"coupon_code": code})
    assert res.status_code == 400


def test_remove_coupon_without_apply(reset_cart, api_client):
    _prepare_cart(api_client)
    res = api_client.post("/coupon/remove")
    assert res.status_code in (200, 400)


@pytest.mark.xfail(reason="Bug: percent coupon discount computed as flat value")
def test_apply_percent_coupon_calculation(reset_cart, api_client):
    # 3 x product_id=1 (unit price 120) gives base amount 360.
    api_client.delete("/cart/clear")
    add = api_client.post("/cart/add", json={"product_id": 1, "quantity": 3})
    assert add.status_code == 200

    res = api_client.post("/coupon/apply", json={"coupon_code": "PERCENT10"})
    assert res.status_code == 200
    data = res.json()

    assert data.get("discount") == 36
    assert data.get("new_total") == 324


@pytest.mark.parametrize("coupon_code", ["", " ", "percent10", "PERCENT10 ", " PERCENT10", "@@@", "X" * 80])
def test_apply_coupon_code_variants_do_not_500(reset_cart, api_client, coupon_code):
    _prepare_cart(api_client)
    res = api_client.post("/coupon/apply", json={"coupon_code": coupon_code})
    assert res.status_code in (200, 400, 404)
