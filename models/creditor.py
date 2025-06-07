from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from models.base import Base, TimestampMixin

class Creditor(TimestampMixin, Base):
    __tablename__ = 'creditors'

    id      = Column(Integer, primary_key=True, index=True)
    name    = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    notes   = Column(String, nullable=True)

    # علاقة بعرض المبيعات المؤجلة (إذا وجدت)
    sales = relationship('Sale', back_populates='creditor')
