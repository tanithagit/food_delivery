def test_full_payment_flow(client, customer_headers, owner_headers, restaurant_and_menu):
    # Add item to cart
    client.post("/cart/", json={
        "menu_item_id": restaurant_and_menu["menu_item_id"],
        "quantity": 1
    }, headers=customer_headers)

    # Checkout - get payment intent
    checkout_res = client.post("/orders/checkout", headers=customer_headers)
    assert checkout_res.status_code == 200
    payment_intent_id = checkout_res.json()["payment_intent_id"]
    assert payment_intent_id.startswith("pi_")

    # Confirm order
    confirm_res = client.post("/orders/confirm", json={
        "payment_intent_id": payment_intent_id
    }, headers=customer_headers)
    assert confirm_res.status_code == 200
    assert confirm_res.json()["payment_status"] == "paid"
    assert confirm_res.json()["status"] == "pending"

def test_cart_cleared_after_order(client, customer_headers):
    cart_res = client.get("/cart/", headers=customer_headers)
    assert cart_res.status_code == 200
    assert cart_res.json()["items"] == []

def test_customer_can_view_their_orders(client, customer_headers):
    res = client.get("/orders/my-orders", headers=customer_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) > 0

def test_owner_cannot_view_customer_orders(client, owner_headers):
    res = client.get("/orders/my-orders", headers=owner_headers)
    assert res.status_code == 403