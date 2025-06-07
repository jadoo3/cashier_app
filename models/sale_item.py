from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class SaleItem(Base):
    __tablename__ = 'sale_items'

    id         = Column(Integer, primary_key=True)
    sale_id    = Column(Integer, ForeignKey('sales.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    qty        = Column(Float, nullable=False)
    price      = Column(Float, nullable=False)

    sale    = relationship('Sale', back_populates='items')
    product = relationship('Product')

    def __repr__(self):
        return f"<SaleItem(product_id={self.product_id}, qty={self.qty}, price={self.price})>"
