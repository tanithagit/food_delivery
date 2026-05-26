import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/food_delivery_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def client(setup_database):
    return TestClient(app)

@pytest.fixture(scope="session")
def owner_token(client):
    client.post("/auth/register", json={
        "email": "testowner@test.com",
        "password": "test123",
        "full_name": "Test Owner",
        "role": "restaurant_owner"
    })
    res = client.post("/auth/login", json={
        "email": "testowner@test.com",
        "password": "test123"
    })
    return res.json()["access_token"]

@pytest.fixture(scope="session")
def owner_headers(owner_token):
    return {"Authorization": f"Bearer {owner_token}"}

@pytest.fixture(scope="session")
def restaurant_and_menu(client, owner_headers):
    # Create restaurant
    r = client.post("/restaurants/", json={
        "name": "Test Restaurant",
        "description": "Best food",
        "address": "123 Test Street"
    }, headers=owner_headers)
    restaurant_id = r.json()["id"]

    # Add menu item
    m = client.post("/restaurants/owner/menu", json={
        "name": "Test Burger",
        "description": "Tasty burger",
        "price": 9.99,
        "is_available": True
    }, headers=owner_headers)
    menu_item_id = m.json()["id"]

    return {"restaurant_id": restaurant_id, "menu_item_id": menu_item_id}

@pytest.fixture(scope="session")
def customer_token(client, restaurant_and_menu):
    client.post("/auth/register", json={
        "email": "testcustomer@test.com",
        "password": "test123",
        "full_name": "Test Customer",
        "role": "customer"
    })
    res = client.post("/auth/login", json={
        "email": "testcustomer@test.com",
        "password": "test123"
    })
    return res.json()["access_token"]

@pytest.fixture(scope="session")
def customer_headers(customer_token):
    return {"Authorization": f"Bearer {customer_token}"}