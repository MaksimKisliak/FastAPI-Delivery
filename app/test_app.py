from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_create_delivery():
    payload = {
        "type": "CREATE_DELIVERY",
        "data": {
            "budget": 1000,
            "notes": "Some delivery notes"
        }
    }
    response = client.post("/deliveries/create", json=payload)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "budget" in response.json()
    assert "notes" in response.json()
    assert "status" in response.json()
    assert response.json()["status"] == "ready"


def test_start_delivery():
    payload = {
        "type": "START_DELIVERY",
        "delivery_id": "some_delivery_id",
        "data": {}
    }
    response = client.post("/event", json=payload)
    assert response.status_code == 200
    assert "budget" in response.json()
    assert "purchase_price" not in response.json()
    assert "quantity" not in response.json()
    assert "sell_price" not in response.json()
    assert response.json()["status"] == "active"


def test_pickup_products():
    payload = {
        "type": "PICKUP_PRODUCTS",
        "delivery_id": "some_delivery_id",
        "data": {
            "purchase_price": 10,
            "quantity": 5
        }
    }
    response = client.post("/event", json=payload)
    assert response.status_code == 200
    assert "budget" in response.json()
    assert "purchase_price" in response.json()
    assert "quantity" in response.json()
    assert "sell_price" not in response.json()
    assert response.json()["status"] == "collected"


def test_deliver_products():
    payload = {
        "type": "DELIVER_PRODUCTS",
        "delivery_id": "some_delivery_id",
        "data": {
            "sell_price": 20,
            "quantity": 3
        }
    }
    response = client.post("/event", json=payload)
    assert response.status_code == 200
    assert "budget" in response.json()
    assert "purchase_price" not in response.json()
    assert "quantity" in response.json()
    assert "sell_price" in response.json()
    assert response.json()["status"] == "completed"


def test_increase_budget():
    payload = {
        "type": "INCREASE_BUDGET",
        "delivery_id": "some_delivery_id",
        "data": {
            "budget": 100
        }
    }
    response = client.post("/event", json=payload)
    assert response.status_code == 200
    assert "budget" in response.json()
    assert "purchase_price" not in response.json()
    assert "quantity" not in response.json()
    assert "sell_price" not in response.json()
    assert response.json()["status"] == "active"


def test_get_state():
    response = client.get("/deliveries/some_delivery_id/status")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "budget" in response.json()
    assert "notes" in response.json()
    assert "status" in response.json()


def test_redis_connection():
    from redis_om import get_redis_connection
    redis = get_redis_connection()
    redis.set("test_key", "test_value")
    assert redis.get("test_key") == b"test_value"
