from sqlalchemy import Column, Integer, String

from orders.db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, index=True, nullable=False)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="created")
