from collections.abc import Sequence  # Для типизации ответа списка

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from orders.db import get_session
from orders.models import Order
from orders.schemas import OrderCreate, OrderResponse

router = APIRouter()


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_session)):
    db_order = Order(
        client_id=payload.client_id,
        item_name=payload.item_name,
        quantity=payload.quantity,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


# --- Карточка 1.3: Получение заказа по номеру ---
@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_session)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заказ с номером {order_id} не найден",
        )
    return db_order


# --- Карточка 1.4: Список заказов клиента ---
@router.get("/orders/client/{client_id}", response_model=list[OrderResponse])
def get_client_orders(
    client_id: int,
    limit: int = Query(default=100, ge=1),
    db: Session = Depends(get_session),
) -> Sequence[Order]:
    orders = db.query(Order).filter(Order.client_id == client_id).limit(limit).all()
    return orders
