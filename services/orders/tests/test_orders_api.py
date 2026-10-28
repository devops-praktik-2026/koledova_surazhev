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

def test_get_order_not_found(client):
    """Тест получения несуществующего заказа (Код 404)"""
    response = client.get("/orders/9999")
    assert response.status_code == 404
    assert "9999" in response.json()["detail"]
