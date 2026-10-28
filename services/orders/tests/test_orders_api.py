from unittest.mock import patch

from fastapi import HTTPException, status

from orders.accounts_client import ensure_account_exists


def test_create_order_client_not_found(client):
    """Тест: заказ не создается, если сервис клиентов вернул 404"""

    # Создаем временную функцию-заглушку, которая имитирует ошибку 404 от соседа
    def mock_ensure_account_exists(account_id: int) -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"account {account_id} not found",
        )

    # Подменяем реальную проверку нашей заглушкой
    from orders.main import app

    app.dependency_overrides[ensure_account_exists] = mock_ensure_account_exists

    payload = {"client_id": 999, "item_name": "Телефон", "quantity": 1}
    response = client.post("/orders", json=payload)

    assert response.status_code == 404

    # Очищаем подмену после завершения теста
    app.dependency_overrides.clear()


def test_create_order_client_service_unavailable(client):
    """Тест: если сервис клиентов не отвечает, возвращается код 503"""

    from fastapi import HTTPException

    # Имитируем падение сетевого клиента httpx, выбрасывая ошибку 503
    with patch(
        "orders.api.ensure_account_exists",
        side_effect=HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Сервис клиентов не отвечает",
        ),
    ):
        payload = {"client_id": 1, "item_name": "Телевизор", "quantity": 1}
        response = client.post("/orders", json=payload)

        # Проверяем, что вернулся код 503
        assert response.status_code == 503
        assert "Сервис клиентов не отвечает" in response.json()["detail"]
