def test_register_customer(client):
    res = client.post("/auth/register", json={
        "email": "newcustomer@test.com",
        "password": "test123",
        "full_name": "New Customer",
        "role": "customer"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "email": "duplicate@test.com",
        "password": "test123",
        "full_name": "Duplicate User",
        "role": "customer"
    })
    res = client.post("/auth/register", json={
        "email": "duplicate@test.com",
        "password": "test123",
        "full_name": "Duplicate User",
        "role": "customer"
    })
    assert res.status_code == 400
    assert res.json()["detail"] == "Email already registered"

def test_login_success(client, customer_token):
    assert customer_token is not None
    assert len(customer_token) > 10

def test_login_wrong_password(client):
    res = client.post("/auth/login", json={
        "email": "testcustomer@test.com",
        "password": "wrongpassword"
    })
    assert res.status_code == 401

def test_login_wrong_email(client):
    res = client.post("/auth/login", json={
        "email": "notexist@test.com",
        "password": "test123"
    })
    assert res.status_code == 401