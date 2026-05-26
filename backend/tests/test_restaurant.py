def test_customer_cannot_create_restaurant(client, customer_headers):
    res = client.post("/restaurants/", json={
        "name": "Fake Restaurant",
        "description": "Test",
        "address": "Test Address"
    }, headers=customer_headers)
    assert res.status_code == 403

def test_owner_restaurant_exists(client, owner_headers, restaurant_and_menu):
    res = client.get("/restaurants/owner/me", headers=owner_headers)
    assert res.status_code == 200
    assert res.json()["name"] == "Test Restaurant"

def test_owner_can_add_menu_item(client, owner_headers):
    res = client.post("/restaurants/owner/menu", json={
        "name": "Extra Item",
        "description": "Extra",
        "price": 5.99,
        "is_available": True
    }, headers=owner_headers)
    assert res.status_code == 200
    assert res.json()["price"] == 5.99

def test_customer_cannot_add_menu_item(client, customer_headers):
    res = client.post("/restaurants/owner/menu", json={
        "name": "Hacked Item",
        "description": "Should not work",
        "price": 1.00,
        "is_available": True
    }, headers=customer_headers)
    assert res.status_code == 403

def test_unauthenticated_cannot_view_restaurants(client):
    res = client.get("/restaurants/")
    assert res.status_code in [401, 403]

def test_customer_can_view_restaurants(client, customer_headers):
    res = client.get("/restaurants/", headers=customer_headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)