# Black Box API Testing Report

## 1. Introduction

This report presents the black-box testing of the QuickCart REST API. The testing approach treats the system as a closed unit, without any knowledge of internal implementation. All test cases are designed based on API behavior, inputs, and outputs.

The objective is to validate:

* Correct HTTP status codes
* Proper JSON response structures
* Logical correctness of API behavior
* Robust handling of invalid and edge-case inputs

Testing was performed using `pytest` and `requests`.

---

## 2. Test Case Design

### 2.1 Product API

#### 1. Fetch all products

* Input: GET `/products`
* Expected Output: HTTP 200 with a list of products
* Justification: Ensures basic product retrieval functionality

#### 2. Fetch product by valid ID

* Input: GET `/products/1`
* Expected Output: HTTP 200 with product details
* Justification: Validates correct lookup behavior

#### 3. Fetch product with invalid ID

* Input: GET `/products/9999`
* Expected Output: HTTP 404
* Justification: Ensures system handles missing resources correctly

---

### 2.2 Cart API

#### 4. Add product to cart (valid)

* Input: POST `/cart/add` with valid product_id and quantity
* Expected Output: HTTP 200
* Justification: Core cart functionality

#### 5. Add product with missing quantity

* Input: POST `/cart/add` without quantity
* Expected Output: HTTP 400
* Justification: Validates required field enforcement

#### 6. Add product with negative quantity

* Input: quantity = -1
* Expected Output: HTTP 400
* Justification: Prevents invalid cart states

#### 7. Add product with large quantity

* Input: quantity = 10000
* Expected Output: Either success or controlled failure
* Justification: Boundary testing

---

### 2.3 Checkout API

#### 8. Valid checkout

* Input: POST `/checkout` with valid payment method
* Expected Output: HTTP 200
* Justification: Validates successful order placement

#### 9. Checkout with invalid method

* Input: payment_method = "INVALID"
* Expected Output: HTTP 400
* Justification: Ensures strict validation

#### 10. Checkout with empty cart

* Expected Output: HTTP 400
* Justification: Prevents invalid transactions

---

### 2.4 Profile API

#### 11. Get profile

* Input: GET `/profile`
* Expected Output: HTTP 200
* Justification: Basic user functionality

#### 12. Update profile (valid)

* Input: valid name and phone
* Expected Output: HTTP 200
* Justification: Ensures update works correctly

#### 13. Update with invalid phone

* Input: phone = "abc123"
* Expected Output: HTTP 400
* Justification: Data validation

---

### 2.5 Wallet API

#### 14. Add money

* Input: POST `/wallet/add`
* Expected Output: HTTP 200
* Justification: Financial correctness

#### 15. Pay from wallet

* Input: POST `/wallet/pay`
* Expected Output: HTTP 200
* Justification: Deduction logic

#### 16. Pay with insufficient balance

* Expected Output: HTTP 400
* Justification: Prevent overdrawing

---

### 2.6 Edge Case Testing

#### 17. Empty string input

* Input: ""
* Expected Output: HTTP 400
* Justification: Boundary validation

#### 18. Null values

* Input: null fields
* Expected Output: HTTP 400
* Justification: Prevent invalid data

#### 19. Wrong data types

* Input: string instead of integer
* Expected Output: HTTP 400
* Justification: Type safety

---

## 3. Bug Report

### Bug 1: Invalid product ID returns 200

* Endpoint: GET `/products/9999`
* Expected: 404
* Actual: 200 with empty object

---

### Bug 2: Cart accepts negative quantity

* Endpoint: POST `/cart/add`
* Expected: 400
* Actual: 200

---

### Bug 3: Missing quantity not validated

* Endpoint: POST `/cart/add`
* Expected: 400
* Actual: 200

---

### Bug 4: Checkout accepts invalid payment method

* Endpoint: POST `/checkout`
* Expected: 400
* Actual: 200

---

### Bug 5: Empty cart checkout succeeds

* Endpoint: POST `/checkout`
* Expected: 400
* Actual: 200

---

### Bug 6: Profile accepts invalid phone format

* Endpoint: PUT `/profile`
* Expected: 400
* Actual: 200

---

### Bug 7: Wallet allows negative add amount

* Endpoint: POST `/wallet/add`
* Expected: 400
* Actual: 200

---

### Bug 8: Wallet deduction incorrect

* Endpoint: POST `/wallet/pay`
* Expected: Correct balance deduction
* Actual: Incorrect final balance

---

### Bug 9: Missing fields do not trigger error

* Endpoint: Multiple endpoints
* Expected: 400
* Actual: 200

---

### Bug 10: Incorrect status codes

* Issue: Some invalid inputs return 200 instead of 400

---

### Bug 11: API accepts wrong data types

* Input: string instead of integer
* Expected: 400
* Actual: 200

---

### Bug 12: Large inputs not handled properly

* Input: extremely large values
* Expected: controlled handling
* Actual: inconsistent behavior

---

### Bug 13: Null values accepted

* Input: null
* Expected: 400
* Actual: 200

---

### Bug 14: Inconsistent JSON structure

* Expected: consistent schema
* Actual: varies across responses

---

### Bug 15: Error messages unclear

* Expected: descriptive error
* Actual: vague or missing

---

## 4. Conclusion

The black-box testing process revealed multiple issues in input validation, error handling, and logical correctness. While basic functionality works, the API lacks robustness against invalid inputs and edge cases.

The designed test suite ensures comprehensive validation across:

* valid scenarios
* invalid inputs
* boundary conditions
* error handling

This testing approach helps improve API reliability, user experience, and system stability.
