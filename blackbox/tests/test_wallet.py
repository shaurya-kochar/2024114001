import pytest


def _wallet_balance(data):
    return data.get("balance", data.get("wallet_balance"))


def test_get_wallet(api_client):
    res = api_client.get("/wallet")
    assert res.status_code == 200
    assert _wallet_balance(res.json()) is not None


def test_wallet_add_invalid_amount_zero(api_client):
    res = api_client.post("/wallet/add", json={"amount": 0})
    assert res.status_code == 400


def test_wallet_add_invalid_amount_too_large(api_client):
    res = api_client.post("/wallet/add", json={"amount": 100001})
    assert res.status_code == 400


def test_wallet_pay_invalid_amount_zero(api_client):
    res = api_client.post("/wallet/pay", json={"amount": 0})
    assert res.status_code == 400


def test_wallet_pay_invalid_amount_negative(api_client):
    res = api_client.post("/wallet/pay", json={"amount": -10})
    assert res.status_code == 400


@pytest.mark.xfail(reason="Bug: wallet pay deducts incorrect amount")
def test_wallet_add_and_pay_exact_deduction(api_client):
    start = _wallet_balance(api_client.get("/wallet").json())
    assert start is not None

    add = api_client.post("/wallet/add", json={"amount": 100})
    assert add.status_code == 200

    pay = api_client.post("/wallet/pay", json={"amount": 40})
    assert pay.status_code == 200

    end = _wallet_balance(api_client.get("/wallet").json())
    assert end is not None
    assert round(float(end), 2) == round(float(start) + 60, 2)


def test_wallet_pay_insufficient_balance(api_client):
    bal = float(_wallet_balance(api_client.get("/wallet").json()))
    res = api_client.post("/wallet/pay", json={"amount": bal + 999999})
    assert res.status_code == 400


@pytest.mark.parametrize("amount", ["100", "10.5", None, " "])
def test_wallet_add_amount_type_variants_validation(api_client, amount):
    res = api_client.post("/wallet/add", json={"amount": amount})
    assert res.status_code == 400


@pytest.mark.parametrize("amount", ["50", "1.25", None, " "])
def test_wallet_pay_amount_type_variants_validation(api_client, amount):
    res = api_client.post("/wallet/pay", json={"amount": amount})
    assert res.status_code == 400
