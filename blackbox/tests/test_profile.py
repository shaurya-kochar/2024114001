import pytest

def test_get_profile(api_client):
    response = api_client.get("/profile")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "phone" in data

def test_update_profile_valid(api_client):
    payload = {"name": "Test User", "phone": "1234567890"}
    response = api_client.put("/profile", json=payload)
    assert response.status_code == 200
    
    # Verify update
    get_resp = api_client.get("/profile")
    assert get_resp.json()["name"] == "Test User"
    assert get_resp.json()["phone"] == "1234567890"

def test_update_profile_invalid_name_short(api_client):
    payload = {"name": "A", "phone": "1234567890"}
    response = api_client.put("/profile", json=payload)
    assert response.status_code == 400

def test_update_profile_invalid_name_long(api_client):
    payload = {"name": "A" * 51, "phone": "1234567890"}
    response = api_client.put("/profile", json=payload)
    assert response.status_code == 400

def test_update_profile_invalid_phone_short(api_client):
    payload = {"name": "Valid Name", "phone": "123456789"}
    response = api_client.put("/profile", json=payload)
    assert response.status_code == 400

def test_update_profile_invalid_phone_long(api_client):
    payload = {"name": "Valid Name", "phone": "12345678901"}
    response = api_client.put("/profile", json=payload)
    assert response.status_code == 400

@pytest.mark.xfail(reason="Bug: profile accepts non-digit characters in 10-char phone")
def test_update_profile_invalid_phone_chars(api_client):
    payload = {"name": "Valid Name", "phone": "12345abcde"}
    response = api_client.put("/profile", json=payload)
    assert response.status_code == 400


@pytest.mark.xfail(reason="Bug: profile accepts whitespace-only name")
def test_update_profile_whitespace_name_rejected(api_client):
    payload = {"name": "  ", "phone": "1234567890"}
    response = api_client.put("/profile", json=payload)
    assert response.status_code == 400


@pytest.mark.parametrize("bad_name", ["", "A", "A" * 51])
def test_update_profile_invalid_name_variants(api_client, bad_name):
    payload = {"name": bad_name, "phone": "1234567890"}
    response = api_client.put("/profile", json=payload)
    assert response.status_code == 400


@pytest.mark.parametrize("bad_phone", ["", "123", "123456789012"])
def test_update_profile_invalid_phone_variants(api_client, bad_phone):
    payload = {"name": "Valid Name", "phone": bad_phone}
    response = api_client.put("/profile", json=payload)
    assert response.status_code == 400


@pytest.mark.xfail(reason="Bug: profile accepts phone containing spaces")
def test_update_profile_phone_with_space_rejected(api_client):
    payload = {"name": "Valid Name", "phone": "12345 7890"}
    response = api_client.put("/profile", json=payload)
    assert response.status_code == 400
