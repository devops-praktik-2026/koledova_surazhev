"""Точка входа сервиса заказов.

Запуск вручную:
    uvicorn orders.main:app --reload --port 8002
"""

from fastapi import FastAPI
from pydantic import BaseModel

from orders.api import router  # Добавили импорт нашего API
from orders.config import settings

app = FastAPI(
    title="Сервис заказов",
    description="Реализация лабораторной работы.",
    version="0.1.0",
)

# Подключаем роутер с запросами заказов (из файла api.py)
app.include_router(router)


class HealthRead(BaseModel):
    status: str
    service: str


@app.get("/health", response_model=HealthRead, tags=["Служебное"], summary="Жив ли сервис")
def health() -> HealthRead:
    return HealthRead(status="ok", service=settings.service_name)
