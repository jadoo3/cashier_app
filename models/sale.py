from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    invoice_number = Column(Integer, unique=True, nullable=False)
    date_time = Column(DateTime, default=datetime.now)
    total_amount = Column(Float, default=0.0)
    paid_amount = Column(Float, default=0.0)
    notes = Column(String(500))
    creditor_id = Column(Integer, ForeignKey('creditors.id'), nullable=True)

    # العلاقات
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    creditor = relationship('Creditor', back_populates='sales')

    def __repr__(self):
        return f"<Sale(invoice_number={self.invoice_number}, total={self.total_amount})>"
