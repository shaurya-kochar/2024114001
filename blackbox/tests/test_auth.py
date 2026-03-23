import requests
import pytest

def test_missing_roll_number(base_url, user_id):
    headers = {"X-User-ID": user_id}
    response = requests.get(f"{base_url}/profile", headers=headers)
    assert response.status_code == 401

def test_invalid_roll_number(base_url, user_id):
    headers = {"X-Roll-Number": "abc", "X-User-ID": user_id}
    response = requests.get(f"{base_url}/profile", headers=headers)
    assert response.status_code == 400

def test_missing_user_id(base_url, roll_number):
    headers = {"X-Roll-Number": roll_number}
    response = requests.get(f"{base_url}/profile", headers=headers)
    assert response.status_code == 400

def test_invalid_user_id(base_url, roll_number):
    headers = {"X-Roll-Number": roll_number, "X-User-ID": "-1"}
    response = requests.get(f"{base_url}/profile", headers=headers)
    assert response.status_code == 400

def test_admin_missing_user_id(base_url, roll_number):
    # Admin endpoints should not require X-User-ID
    headers = {"X-Roll-Number": roll_number}
    response = requests.get(f"{base_url}/admin/users", headers=headers)
    assert response.status_code == 200


@pytest.mark.parametrize("bad_roll", ["", "2024101104x", "abc"])
def test_invalid_roll_number_variants(base_url, user_id, bad_roll):
    headers = {"X-Roll-Number": bad_roll, "X-User-ID": user_id}
    response = requests.get(f"{base_url}/profile", headers=headers)
    assert response.status_code in (400, 401)


@pytest.mark.parametrize("bad_user_id", ["-1", "abc", "1.5"])
def test_invalid_user_id_variants(base_url, roll_number, bad_user_id):
    headers = {"X-Roll-Number": roll_number, "X-User-ID": bad_user_id}
    response = requests.get(f"{base_url}/profile", headers=headers)
    assert response.status_code == 400
