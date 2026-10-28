from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    client_id: int
    item_name: str
    quantity: int = Field(..., ge=1)  # ge=1 гарантирует ошибку 422, если quantity < 1


class OrderResponse(BaseModel):
    id: int
    client_id: int
    item_name: str
    quantity: int
    status: str = "created"

    class Config:
        from_attributes = True
