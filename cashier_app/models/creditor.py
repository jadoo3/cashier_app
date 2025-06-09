"""Creditor model for managing debts."""

from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship

from .base import Base
from .mixins import TimestampMixin


class Creditor(Base, TimestampMixin):
    """Represents a person who owes or is owed money."""

    __tablename__ = "creditors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    balance = Column(Numeric(10, 2), default=0)

    sales = relationship("Sale", back_populates="creditor")
