"""Payment model tracking creditor repayments."""

from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime
from datetime import datetime

from .base import Base
from .mixins import TimestampMixin


class Payment(Base, TimestampMixin):
    """Represents a payment from a creditor."""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    creditor_id = Column(Integer, ForeignKey("creditors.id"))
    amount = Column(Numeric(10, 2), nullable=False)
    paid_at = Column(DateTime, default=datetime.utcnow)
