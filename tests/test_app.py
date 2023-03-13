from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

delivery_id = None


def test_redis_connection():
    from redis_om import get_redis_connection
    from dotenv import load_dotenv
    import os
    load_dotenv()
    redis = get_redis_connection(
        host=os.environ.get('REDIS_HOST'),
        port=os.environ.get('REDIS_PORT'),
        password=os.environ.get('REDIS_PASSWORD'),
    )
    redis.set("test_key", "test_value")
    assert redis.get("test_key") == "test_value"


def test_create_delivery():
    global delivery_id
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
    delivery_id = response.json()["id"]


def test_start_delivery():
    global delivery_id
    payload = {
        "type": "START_DELIVERY",
        "delivery_id": delivery_id,
        "data": {}
    }
    response = client.post("/event", json=payload)
    assert response.status_code == 200
    assert "budget" in response.json()
    assert "purchase_price" not in response.json()
    assert "quantity" not in response.json()
    assert "sell_price" not in response.json()
    assert response.json()["status"] == "active"


def test_increase_budget():
    global delivery_id
    payload = {
        "type": "INCREASE_BUDGET",
        "delivery_id": delivery_id,
        "data": {
            "budget": 100
        }
    }
    response = client.post("/event", json=payload)
    assert response.status_code == 200
    print(response.json())
    assert "budget" in response.json()
    assert "purchase_price" not in response.json()
    assert "quantity" not in response.json()
    assert "sell_price" not in response.json()
    assert response.json()["status"] == "active"


def test_pickup_products():
    global delivery_id
    payload = {
        "type": "PICKUP_PRODUCTS",
        "delivery_id": delivery_id,
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
    global delivery_id
    payload = {
        "type": "DELIVER_PRODUCTS",
        "delivery_id": delivery_id,
        "data": {
            "sell_price": 70,
            "quantity": 5
        }
    }
    response = client.post("/event", json=payload)
    assert response.status_code == 200
    assert "budget" in response.json()
    assert "quantity" in response.json()
    assert "sell_price" in response.json()
    assert response.json()["status"] == "completed"


def test_get_state():
    global delivery_id
    response = client.get(f"/deliveries/{delivery_id}/status")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "budget" in response.json()
    assert "notes" in response.json()
    assert response.json()["status"] == "completed"
