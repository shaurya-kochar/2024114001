import pytest
import requests

BASE_URL = "http://localhost:5000"

# ==========================================
# 1. VALID REQUESTS
# ==========================================

def test_get_all_products_returns_200():
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200

def test_get_all_products_is_list():
    response = requests.get(f"{BASE_URL}/products")
    assert isinstance(response.json(), list)

def test_create_valid_product():
    payload = {"name": "Test Product", "price": 99.99, "stock": 50}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 201

def test_create_product_response_contains_id():
    payload = {"name": "Box", "price": 10.0, "stock": 5}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    data = response.json()
    assert "id" in data

def test_get_single_product_valid():
    # Attempting to fetch a valid known product (Assuming ID 1 exists)
    response = requests.get(f"{BASE_URL}/products/1")
    if response.status_code == 200:
        assert "name" in response.json()
        assert "price" in response.json()

def test_update_valid_product():
    # Assuming ID 1 exists
    payload = {"name": "Updated Name", "price": 150.0, "stock": 100}
    response = requests.put(f"{BASE_URL}/products/1", json=payload)
    assert response.status_code in [200, 404] # 404 if it doesn't exist, 200 if valid updates

def test_update_product_response_structure():
    payload = {"name": "Updated Name", "price": 150.0, "stock": 100}
    response = requests.put(f"{BASE_URL}/products/1", json=payload)
    if response.status_code == 200:
        data = response.json()
        assert data.get("name") == "Updated Name"

def test_delete_existing_product():
    # Creating a temp product to delete
    payload = {"name": "Temp", "price": 1.0, "stock": 1}
    post_res = requests.post(f"{BASE_URL}/products", json=payload)
    if post_res.status_code == 201:
        pid = post_res.json().get("id")
        del_res = requests.delete(f"{BASE_URL}/products/{pid}")
        assert del_res.status_code == 204 or del_res.status_code == 200

# ==========================================
# 2. INVALID INPUTS
# ==========================================

def test_get_non_existent_product():
    response = requests.get(f"{BASE_URL}/products/999999")
    assert response.status_code == 404

def test_get_negative_id():
    response = requests.get(f"{BASE_URL}/products/-5")
    assert response.status_code == 400 or response.status_code == 404

def test_get_invalid_string_id():
    response = requests.get(f"{BASE_URL}/products/invalid_id_abc")
    assert response.status_code == 400 or response.status_code == 404

def test_post_invalid_id_in_body():
    payload = {"id": 999, "name": "Hack", "price": 10.0, "stock": 2}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    # Should probably ignore ID or return 400
    assert response.status_code in [201, 400] 

def test_delete_non_existent_product():
    response = requests.delete(f"{BASE_URL}/products/999999")
    assert response.status_code == 404

def test_delete_already_deleted_product():
    # Delete a product that could theoretically already be gone
    response = requests.delete(f"{BASE_URL}/products/999998")
    assert response.status_code == 404

def test_put_invalid_string_id():
    response = requests.put(f"{BASE_URL}/products/xyz123", json={"name": "A"})
    assert response.status_code in [400, 404]

def test_put_negative_id():
    response = requests.put(f"{BASE_URL}/products/-1", json={"name": "A"})
    assert response.status_code in [400, 404]


# ==========================================
# 3. MISSING FIELDS
# ==========================================

def test_post_missing_name():
    payload = {"price": 10.0, "stock": 5}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_missing_price():
    payload = {"name": "Test", "stock": 5}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_missing_stock():
    payload = {"name": "Test", "price": 10.0}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_empty_body():
    response = requests.post(f"{BASE_URL}/products", json={})
    assert response.status_code == 400

def test_put_missing_all_fields():
    response = requests.put(f"{BASE_URL}/products/1", json={})
    assert response.status_code == 400

def test_put_missing_name_partial_update():
    # If partial updates aren't allowed, this should be 400
    payload = {"price": 150.0, "stock": 100}
    response = requests.put(f"{BASE_URL}/products/1", json=payload)
    assert response.status_code in [200, 400, 404]

def test_post_missing_multiple_fields():
    payload = {"name": "Test"}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_no_json_header():
    # Send form data instead of JSON
    response = requests.post(f"{BASE_URL}/products", data={"name": "Test", "price": 10, "stock": 1})
    assert response.status_code == 400 or response.status_code == 415

# ==========================================
# 4. WRONG DATA TYPES
# ==========================================

def test_post_price_as_string():
    payload = {"name": "String Price", "price": "19.99", "stock": 10}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_stock_as_float():
    payload = {"name": "Float Stock", "price": 19.99, "stock": 10.5}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_name_as_int():
    payload = {"name": 12345, "price": 10.0, "stock": 5}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_stock_as_string():
    payload = {"name": "Str Stock", "price": 10.0, "stock": "five"}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_price_null():
    payload = {"name": "No Price", "price": None, "stock": 10}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_name_null():
    payload = {"name": None, "price": 10.0, "stock": 10}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_put_price_as_boolean():
    payload = {"name": "Bool Price", "price": True, "stock": 10}
    response = requests.put(f"{BASE_URL}/products/1", json=payload)
    assert response.status_code in [400, 404]

def test_put_stock_as_list():
    payload = {"name": "List Stock", "price": 10.0, "stock": [1, 2, 3]}
    response = requests.put(f"{BASE_URL}/products/1", json=payload)
    assert response.status_code in [400, 404]


# ==========================================
# 5. BOUNDARY VALUES
# ==========================================

def test_post_empty_string_name():
    payload = {"name": "", "price": 10.0, "stock": 5}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_zero_price():
    payload = {"name": "Free item", "price": 0.0, "stock": 5}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    # Could be valid depending on business logic, normally ok but often strictly > 0
    assert response.status_code in [201, 400]

def test_post_negative_price():
    payload = {"name": "Debt item", "price": -10.0, "stock": 5}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_negative_stock():
    payload = {"name": "Owed item", "price": 10.0, "stock": -5}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_huge_price():
    payload = {"name": "Luxury", "price": 999999999999999.99, "stock": 1}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    # System should handle or correctly bound
    assert response.status_code in [201, 400]

def test_post_huge_stock():
    payload = {"name": "Grains", "price": 1.0, "stock": 2147483647}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code in [201, 400]

def test_post_very_long_name():
    payload = {"name": "A" * 10000, "price": 10.0, "stock": 5}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    assert response.status_code == 400

def test_post_price_many_decimals():
    payload = {"name": "Crypto", "price": 10.12345678, "stock": 5}
    response = requests.post(f"{BASE_URL}/products", json=payload)
    # Could be rounded or rejected
    assert response.status_code in [201, 400]
