"""Общая подготовка для тестов сервиса клиентов.

Каждый тест получает свою пустую базу данных в оперативной памяти.
Так тесты не зависят друг от друга и не требуют запущенного PostgreSQL.
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from orders.accounts_client import (
    ensure_account_exists,
)  # Добавили импорт проверки
from orders.db import Base, get_session
from orders.main import app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def override_get_session() -> Iterator[Session]:
        with TestSession() as session:
            yield session

    # По умолчанию для всех старых тестов считаем, что проверка клиента всегда проходит успешно (ничего не делает)
    def mock_ensure_account_exists(account_id: int) -> None:
        return None

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[ensure_account_exists] = (
        mock_ensure_account_exists  # Заглушка сети для старых тестов
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


@pytest.fixture
def order_payload():
    return {"client_id": 1, "item_name": "Тестовый товар", "quantity": 5}
