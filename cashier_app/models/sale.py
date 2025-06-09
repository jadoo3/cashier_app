"""Sale invoice model."""

from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base
from .mixins import TimestampMixin


class Sale(Base, TimestampMixin):
    """Represents a sales invoice."""

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    invoice_no = Column(String, unique=True, nullable=False)
    datetime = Column(DateTime, default=datetime.utcnow)
    payment_type = Column(String, nullable=False)
    creditor_id = Column(Integer, ForeignKey("creditors.id"), nullable=True)
    total = Column(Numeric(10, 2), nullable=False, default=0)
    paid = Column(Numeric(10, 2), nullable=False, default=0)
    remaining = Column(Numeric(10, 2), nullable=False, default=0)

    items = relationship("SaleItem", back_populates="sale")
    creditor = relationship("Creditor", back_populates="sales")
