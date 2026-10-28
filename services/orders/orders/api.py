from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from orders.db import get_session  # Поменяли на get_session
from orders.models import Order
from orders.schemas import OrderCreate, OrderResponse

router = APIRouter()


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate, db: Session = Depends(get_session)
):  # Поменяли на get_session
    db_order = Order(
        client_id=payload.client_id, item_name=payload.item_name, quantity=payload.quantity
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
