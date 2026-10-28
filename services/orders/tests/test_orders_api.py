

def test_create_order_returns_201(client):
    """Тест успешного создания заказа (Код 201)"""
    payload = {"client_id": 1, "item_name": "Тестовый товар", "quantity": 5}
    response = client.post("/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["item_name"] == "Тестовый товар"
    assert "id" in data


def test_invalid_payload_returns_422(client):
    """Тест ошибки валидации, если количество меньше 1 (Код 422)"""
    payload = {
        "client_id": 1,
        "item_name": "Тестовый товар",
        "quantity": 0,  # Невалидное количество
    }
    response = client.post("/orders", json=payload)
    assert response.status_code == 422
