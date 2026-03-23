import pytest


def test_admin_get_users(api_client):
    response = api_client.get("/admin/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "user_id" in data[0]

def test_admin_get_user_by_id(api_client):
    response = api_client.get("/admin/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1

def test_admin_get_carts(api_client):
    response = api_client.get("/admin/carts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_admin_get_orders(api_client):
    response = api_client.get("/admin/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_admin_get_products(api_client):
    response = api_client.get("/admin/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_admin_get_coupons(api_client):
    response = api_client.get("/admin/coupons")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_admin_get_tickets(api_client):
    response = api_client.get("/admin/tickets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_admin_get_addresses(api_client):
    response = api_client.get("/admin/addresses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.parametrize("bad_id", ["-1", "abc", "1.5", " "])
def test_admin_get_user_by_id_invalid_format_variants(api_client, bad_id):
    response = api_client.get(f"/admin/users/{bad_id}")
    assert response.status_code in (400, 404)


def test_admin_get_user_by_id_nonexistent_case(api_client):
    response = api_client.get("/admin/users/999999")
    assert response.status_code == 404
