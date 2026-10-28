def test_get_order_success(client):
    """Тест успешного получения существующего заказа (Код 200)"""
    # Сначала создаём заказ
    payload = {"client_id": 1, "item_name": "Книга", "quantity": 1}
    create_resp = client.post("/orders", json=payload)
    order_id = create_resp.json()["id"]

    # Теперь запрашиваем его по ID
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["item_name"] == "Книга"

def test_invalid_payload_returns_422(client):
    """Тест ошибки валидации, если количество меньше 1 (Код 422)"""
    payload = {
        "client_id": 1,
        "item_name": "Тестовый товар",
        "quantity": 0,  # Невалидное количество
    }
    response = client.post("/orders", json=payload)
    assert response.status_code == 422


def test_get_client_orders_success(client):
    """Тест получения списка заказов конкретного клиента (Код 200)"""
    # Создаём два заказа для клиента с ID 5
    client.post(
        "/orders",
        json={"client_id": 5, "item_name": "Ручка", "quantity": 2},
    )
    client.post(
        "/orders",
        json={"client_id": 5, "item_name": "Карандаш", "quantity": 3},
    )

    # Проверяем работу фильтра и limit=1
    response = client.get("/orders/client/5?limit=1")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_client_orders_empty(client):
    """Тест: у клиента без заказов возвращается пустой список (Код 200)"""
    response = client.get("/orders/client/99")
    assert response.status_code == 200
    assert response.json() == []

def test_get_order_not_found(client):
    """Тест получения несуществующего заказа (Код 404)"""
    response = client.get("/orders/9999")
    assert response.status_code == 404
    assert "9999" in response.json()["detail"]
