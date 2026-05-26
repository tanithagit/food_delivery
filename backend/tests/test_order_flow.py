def test_owner_cannot_add_to_cart(client, owner_headers, restaurant_and_menu):
    res = client.post("/cart/", json={
        "menu_item_id": restaurant_and_menu["menu_item_id"],
        "quantity": 1
    }, headers=owner_headers)
    assert res.status_code == 403

def test_customer_can_view_empty_cart(client, customer_headers):
    res = client.get("/cart/", headers=customer_headers)
    assert res.status_code == 200
    assert res.json()["items"] == []

def test_customer_can_add_to_cart(client, customer_headers, restaurant_and_menu):
    res = client.post("/cart/", json={
        "menu_item_id": restaurant_and_menu["menu_item_id"],
        "quantity": 2
    }, headers=customer_headers)
    assert res.status_code == 200
    assert len(res.json()["items"]) == 1
    assert res.json()["items"][0]["quantity"] == 2

def test_cannot_add_zero_quantity(client, customer_headers, restaurant_and_menu):
    res = client.post("/cart/", json={
        "menu_item_id": restaurant_and_menu["menu_item_id"],
        "quantity": 0
    }, headers=customer_headers)
    assert res.status_code == 400

def test_customer_can_checkout(client, customer_headers):
    res = client.post("/orders/checkout", headers=customer_headers)
    assert res.status_code == 200
    assert "payment_intent_id" in res.json()
    assert "client_secret" in res.json()
    assert res.json()["amount"] > 0

def test_empty_cart_cannot_checkout(client, customer_headers):
    cart_res = client.get("/cart/", headers=customer_headers)
    for item in cart_res.json()["items"]:
        client.delete(f"/cart/{item['id']}", headers=customer_headers)
    res = client.post("/orders/checkout", headers=customer_headers)
    assert res.status_code == 400
    assert res.json()["detail"] == "Your cart is empty"