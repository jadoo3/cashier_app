class OutOfStockError(Exception):
    """يرفع عندما تكون الكمية المطلوبة أكبر من المخزون."""
    pass

from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from models.base import Base, TimestampMixin
from utils.validators import ValidationError

class Product(TimestampMixin, Base):
    __tablename__ = 'products'

    id         = Column(Integer, primary_key=True, index=True)
    code       = Column(String, unique=True, nullable=False)
    name       = Column(String, unique=True, nullable=False)
    unit       = Column(String, nullable=False)
    stock_qty  = Column(Float, default=0.0, nullable=False)
    price_buy  = Column(Float, nullable=False)
    price_sell = Column(Float, nullable=False)
    is_active  = Column(Boolean, default=True, nullable=False)

    sale_items = relationship("SaleItem", back_populates="product")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate()

    def validate(self):
        """التحقق من صحة بيانات المنتج"""
        if not self.name or not self.name.strip():
            raise ValidationError("اسم المنتج مطلوب")
        if not self.code or not self.code.strip():
            raise ValidationError("رمز المنتج مطلوب")
        if not self.unit or not self.unit.strip():
            raise ValidationError("وحدة القياس مطلوبة")
        if self.stock_qty < 0:
            raise ValidationError("الكمية يجب أن تكون موجبة")
        if self.price_buy < 0:
            raise ValidationError("سعر الشراء يجب أن يكون موجباً")
        if self.price_sell < 0:
            raise ValidationError("سعر البيع يجب أن يكون موجباً")
        if self.price_sell < self.price_buy:
            raise ValidationError("سعر البيع يجب أن يكون أكبر من أو يساوي سعر الشراء")

    def withdraw(self, qty: float) -> None:
        """سحب كمية من المخزون"""
        if qty <= 0:
            raise ValidationError("الكمية المطلوبة يجب أن تكون موجبة")
        if qty > self.stock_qty:
            raise OutOfStockError(
                f"الكمية المطلوبة ({qty}) أكبر من المخزون ({self.stock_qty})"
            )
        self.stock_qty -= qty

    def add_stock(self, qty: float) -> None:
        """إضافة كمية للمخزون"""
        if qty <= 0:
            raise ValidationError("الكمية يجب أن تكون موجبة")
        self.stock_qty += qty

    def update_prices(self, new_buy: float, new_sell: float) -> None:
        """تحديث أسعار الشراء والبيع"""
        if new_buy < 0:
            raise ValidationError("سعر الشراء يجب أن يكون موجباً")
        if new_sell < 0:
            raise ValidationError("سعر البيع يجب أن يكون موجباً")
        if new_sell < new_buy:
            raise ValidationError("سعر البيع يجب أن يكون أكبر من أو يساوي سعر الشراء")
        self.price_buy = new_buy
        self.price_sell = new_sell

