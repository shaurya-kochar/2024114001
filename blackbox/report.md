# Black Box API Testing Bug Report

This report documents bugs discovered in the QuickCart REST API during black-box testing.

### Bug 1: Product Price Mismatch
* **Endpoint tested:** `/api/v1/products` vs `/api/v1/admin/products`
* **HTTP method:** `GET`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`
* **Request body:** N/A
* **Expected result:** The price shown for products in `/api/v1/products` should match the exact real price stored in `/api/v1/admin/products`.
* **Actual result:** The product price differs between the user products list and the admin products list.

### Bug 2: Cart Accepts Zero Quantity
* **Endpoint tested:** `/api/v1/cart/add`
* **HTTP method:** `POST`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`, `Content-Type: application/json`
* **Request body:** `{"product_id": 1, "quantity": 0}`
* **Expected result:** `400 Bad Request` (Quantity must be at least 1).
* **Actual result:** `200 OK` (The cart accepts a quantity of 0).

### Bug 3: Cart Item Subtotal Overflow
* **Endpoint tested:** `/api/v1/cart`
* **HTTP method:** `GET`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`
* **Request body:** N/A
* **Expected result:** Item subtotal in cart should exactly equal `quantity * unit_price`.
* **Actual result:** Item subtotal overflows instead of correctly multiplying quantity by unit price.

### Bug 4: Cart Total Missing Subtotals
* **Endpoint tested:** `/api/v1/cart`
* **HTTP method:** `GET`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`
* **Request body:** N/A
* **Expected result:** Cart total must be the exact sum of all item subtotals, including the last one.
* **Actual result:** Cart total does not include all subtotals (misses items in its summation).

### Bug 5: Average Rating Rounded Down
* **Endpoint tested:** `/api/v1/products/{product_id}/reviews`
* **HTTP method:** `GET`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`
* **Request body:** N/A
* **Expected result:** The average rating should be a proper decimal calculation (e.g., 4.5).
* **Actual result:** The average rating is rounded down to an integer.

### Bug 6: Profile Accepts Non-digit Phone
* **Endpoint tested:** `/api/v1/profile`
* **HTTP method:** `PUT`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`, `Content-Type: application/json`
* **Request body:** `{"name": "Valid Name", "phone": "abcdefghij"}`
* **Expected result:** `400 Bad Request` (Phone number must be exactly 10 digits).
* **Actual result:** `200 OK` (Profile accepts non-digit characters in the 10-char phone number).

### Bug 7: Profile Accepts Whitespace-only Name
* **Endpoint tested:** `/api/v1/profile`
* **HTTP method:** `PUT`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`, `Content-Type: application/json`
* **Request body:** `{"name": "     ", "phone": "1234567890"}`
* **Expected result:** `400 Bad Request` (Name must be between 2 and 50 valid characters).
* **Actual result:** `200 OK` (Profile accepts a whitespace-only name).

### Bug 8: Address Accepts 5-digit Pincode
* **Endpoint tested:** `/api/v1/addresses`
* **HTTP method:** `POST`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`, `Content-Type: application/json`
* **Request body:** `{"label": "HOME", "street": "123 Test Street", "city": "TestCity", "pincode": "12345"}`
* **Expected result:** `400 Bad Request` (Pincode must be exactly 6 digits).
* **Actual result:** `201 Created` (Accepts 5-digit pincode).

### Bug 9: Wallet Pay Deducts Incorrect Amount
* **Endpoint tested:** `/api/v1/wallet/pay`
* **HTTP method:** `POST`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`, `Content-Type: application/json`
* **Request body:** `{"amount": 10}`
* **Expected result:** The exact amount (10) should be deducted from the user's wallet balance.
* **Actual result:** Wallet pay deducts an incorrect amount from the balance.

### Bug 10: Percent Coupon Discount Computed as Flat Value
* **Endpoint tested:** `/api/v1/coupon/apply`
* **HTTP method:** `POST`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`, `Content-Type: application/json`
* **Request body:** `{"code": "PERCENT10"}`
* **Expected result:** A PERCENT coupon should take a percentage off the cart total.
* **Actual result:** The percent coupon discount is computed and applied as a flat value subtraction.

### Bug 11: Cancelled Order Does Not Restore Stock
* **Endpoint tested:** `/api/v1/orders/{order_id}/cancel`
* **HTTP method:** `POST`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`
* **Request body:** N/A
* **Expected result:** When an order is cancelled, all the items in that order are added back to the product stock.
* **Actual result:** Cancelled order does not restore product stock, leading to lost inventory.

### Bug 12: Delivered Orders Can Be Cancelled
* **Endpoint tested:** `/api/v1/orders/{order_id}/cancel`
* **HTTP method:** `POST`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`
* **Request body:** N/A
* **Expected result:** `400 Bad Request` (A delivered order cannot be cancelled).
* **Actual result:** `200 OK` (Delivered orders can still be successfully cancelled).

### Bug 13: COD Checkout Starts as PAID
* **Endpoint tested:** `/api/v1/checkout`
* **HTTP method:** `POST`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`, `Content-Type: application/json`
* **Request body:** `{"payment_method": "COD"}`
* **Expected result:** Order starts with a payment status of PENDING.
* **Actual result:** COD checkout creates the order with a status of PAID instead of PENDING.

### Bug 14: WALLET Checkout Starts as PAID instead of PENDING
* **Endpoint tested:** `/api/v1/checkout`
* **HTTP method:** `POST`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`, `Content-Type: application/json`
* **Request body:** `{"payment_method": "WALLET"}`
* **Expected result:** Order starts with a payment status of PENDING.
* **Actual result:** WALLET checkout creates the order with a status of PAID instead of PENDING.

### Bug 15: Empty Pincode is Accepted
* **Endpoint tested:** `/api/v1/addresses`
* **HTTP method:** `POST`
* **Headers:** `X-Roll-Number: 2024114001`, `X-User-ID: 1`, `Content-Type: application/json`
* **Request body:** `{"label": "HOME", "street": "123 Main St", "city": "City", "pincode": ""}`
* **Expected result:** `400 Bad Request` (Pincode must be exactly 6 digits).
* **Actual result:** `201 Created` (Empty pincode is accepted into the database).
