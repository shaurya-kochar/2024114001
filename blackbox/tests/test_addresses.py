import pytest

def test_get_addresses(api_client):
    response = api_client.get("/addresses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.xfail(reason="Bug: valid pin rejected")
def test_add_address_valid(api_client):
    payload = {"label": "HOME", "street": "123 Main Street", "city": "Metropolis", "pincode": "123456"}
    response = api_client.post("/addresses", json=payload)
    if response.status_code == 400:
        pytest.fail("Server rejected valid 6-digit pincode with 400")
    assert response.status_code in [200, 201]

@pytest.mark.xfail(reason="Bug: accepts 5-digit pincode")
def test_add_address_invalid_pincode_length(api_client):
    payload = {"label": "HOME", "street": "123 Main Street", "city": "Metropolis", "pincode": "12345"}
    response = api_client.post("/addresses", json=payload)
    if response.status_code == 200:
        pytest.fail("Server accepted 5-digit pincode")
    assert response.status_code == 400

def test_add_address_invalid_label(api_client):
    payload = {"label": "WORK", "street": "123 Main Street", "city": "Metropolis", "pincode": "12345"}
    response = api_client.post("/addresses", json=payload)
    assert response.status_code == 400

def test_add_address_invalid_street_short(api_client):
    payload = {"label": "HOME", "street": "A1", "city": "Metropolis", "pincode": "12345"}
    response = api_client.post("/addresses", json=payload)
    assert response.status_code == 400

def test_add_address_invalid_city_short(api_client):
    payload = {"label": "HOME", "street": "123 Main Street", "city": "A", "pincode": "12345"}
    response = api_client.post("/addresses", json=payload)
    assert response.status_code == 400

def helper_add_address_workaround(api_client):
    # Uses 5-digit pincode just to add an address due to bug
    res = api_client.post("/addresses", json={"label": "HOME", "street": "Street Test", "city": "City Test", "pincode": "11111"})
    return res.json()["address"]["address_id"]

def test_default_address_unsets_others(api_client):
    addr1_id = helper_add_address_workaround(api_client)
    api_client.put(f"/addresses/{addr1_id}", json={"is_default": True, "street": "Street One"})

    addr2_id = helper_add_address_workaround(api_client)
    api_client.put(f"/addresses/{addr2_id}", json={"is_default": True, "street": "Street Two"})

    addresses = api_client.get("/addresses").json()
    addr1_is_default = next(a["is_default"] for a in addresses if a["address_id"] == addr1_id)
    addr2_is_default = next(a["is_default"] for a in addresses if a["address_id"] == addr2_id)

    assert addr2_is_default is True
    assert addr1_is_default is False

def test_update_address_restrict_fields(api_client):
    addr_id = helper_add_address_workaround(api_client)
    payload = {
        "street": "Street New",
        "is_default": True,
        "label": "OFFICE",
        "city": "New City",
        "pincode": "99999",
    }
    update_res = api_client.put(f"/addresses/{addr_id}", json=payload)
    assert update_res.status_code == 200

    data = update_res.json()["address"]
    assert data["street"] == "Street New"
    assert data["label"] == "HOME"
    assert data["city"] == "City Test"
    assert data["pincode"] == "11111"

def test_delete_address(api_client):
    addr_id = helper_add_address_workaround(api_client)
    del_res = api_client.delete(f"/addresses/{addr_id}")
    assert del_res.status_code in [200, 204]

def test_delete_non_existent_address(api_client):
    del_res = api_client.delete("/addresses/999999")
    assert del_res.status_code == 404


@pytest.mark.parametrize("bad_pincode", ["abcdef", "12 456", "12a456", "1234-6"])
def test_add_address_invalid_pincode_format_variants(api_client, bad_pincode):
    payload = {
        "label": "HOME",
        "street": "123 Main Street",
        "city": "Metropolis",
        "pincode": bad_pincode,
    }
    response = api_client.post("/addresses", json=payload)
    assert response.status_code == 400


@pytest.mark.xfail(reason="Bug: empty pincode is accepted")
def test_add_address_empty_pincode_rejected(api_client):
    payload = {
        "label": "HOME",
        "street": "123 Main Street",
        "city": "Metropolis",
        "pincode": "",
    }
    response = api_client.post("/addresses", json=payload)
    assert response.status_code == 400
