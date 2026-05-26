def test_owner_can_view_restaurant_orders(client, owner_headers):
    res = client.get("/orders/restaurant-orders", headers=owner_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) > 0

def test_customer_cannot_view_restaurant_orders(client, customer_headers):
    res = client.get("/orders/restaurant-orders", headers=customer_headers)
    assert res.status_code == 403

def test_valid_status_transition(client, owner_headers):
    orders_res = client.get("/orders/restaurant-orders", headers=owner_headers)
    orders = orders_res.json()
    assert len(orders) > 0
    order_id = orders[0]["id"]

    res = client.put(f"/orders/{order_id}/status", json={
        "status": "confirmed"
    }, headers=owner_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "confirmed"

def test_second_status_transition(client, owner_headers):
    orders_res = client.get("/orders/restaurant-orders", headers=owner_headers)
    order_id = orders_res.json()[0]["id"]

    res = client.put(f"/orders/{order_id}/status", json={
        "status": "preparing"
    }, headers=owner_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "preparing"

def test_invalid_status_transition(client, owner_headers):
    orders_res = client.get("/orders/restaurant-orders", headers=owner_headers)
    order_id = orders_res.json()[0]["id"]

    res = client.put(f"/orders/{order_id}/status", json={
        "status": "pending"
    }, headers=owner_headers)
    assert res.status_code == 400
    assert "Cannot move" in res.json()["detail"]

def test_customer_cannot_update_order_status(client, customer_headers):
    res = client.put("/orders/1/status", json={
        "status": "confirmed"
    }, headers=customer_headers)
    assert res.status_code == 403