"""History of product price changes."""

from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime
from datetime import datetime

from .base import Base


class PriceHistory(Base):
    """Stores price change history for products."""

    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    old_buy = Column(Numeric(10, 2))
    new_buy = Column(Numeric(10, 2))
    old_sell = Column(Numeric(10, 2))
    new_sell = Column(Numeric(10, 2))
    changed_at = Column(DateTime, default=datetime.utcnow)
