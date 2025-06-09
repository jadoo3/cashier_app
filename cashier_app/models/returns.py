"""Model for returned items."""

from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from datetime import datetime

from .base import Base
from .mixins import TimestampMixin


class Return(Base, TimestampMixin):
    """Represents a returned product."""

    __tablename__ = "returns"

    id = Column(Integer, primary_key=True)
    sale_item_id = Column(Integer, ForeignKey("sale_items.id"))
    quantity = Column(Integer, nullable=False)
    refund_amount = Column(Numeric(10, 2), nullable=False)
    returned_at = Column(DateTime, default=datetime.utcnow)
