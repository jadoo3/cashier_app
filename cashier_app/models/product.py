"""ORM model for products."""

from sqlalchemy import Column, Integer, String, Numeric
from .base import Base


class Product(Base):
    """Represents a product in inventory."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    barcode = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    buy_price = Column(Numeric(10, 2), nullable=False)
    sell_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=0)
