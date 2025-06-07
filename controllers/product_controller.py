from contextlib import contextmanager
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import IntegrityError
from database.db_session import SessionLocal, session_scope
from models.product import Product, OutOfStockError
from models.price_history import PriceHistory
from models.audit_log import AuditLog
from sqlalchemy import or_, and_
from utils.validators import validate_product_data, ValidationError
import logging

logger = logging.getLogger(__name__)

class ProductController:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, code, name, unit, stock_qty, price_buy, price_sell):
        """إنشاء منتج جديد أو زيادة الكمية إذا كان موجوداً"""
        try:
            # البحث عن منتج بنفس الاسم
            existing_product = self.db.query(Product).filter(Product.name == name).first()
            
            if existing_product:
                # إذا وجد المنتج، نزيد الكمية
                existing_product.stock_qty += stock_qty
                # تحديث الأسعار إذا كانت مختلفة
                if existing_product.price_buy != price_buy or existing_product.price_sell != price_sell:
                    existing_product.price_buy = price_buy
                    existing_product.price_sell = price_sell
                    # تسجيل تغيير السعر
                    ph = PriceHistory(
                        product_id=existing_product.id,
                        old_price=existing_product.price_sell,
                        new_price=price_sell
                    )
                    self.db.add(ph)
                
                self.db.commit()
                self.db.refresh(existing_product)
                return existing_product
            else:
                # إنشاء منتج جديد
                p = Product(
                    code=code,
                    name=name,
                    unit=unit,
                    stock_qty=stock_qty,
                    price_buy=price_buy,
                    price_sell=price_sell
                )
                self.db.add(p)
                self.db.commit()
                self.db.refresh(p)
                return p
                
        except IntegrityError as e:
            self.db.rollback()
            if 'UNIQUE constraint failed: products.code' in str(e):
                raise ValidationError("رمز المنتج مستخدم مسبقاً")
            raise ValidationError("حدث خطأ في قاعدة البيانات")

    def list_all(self, active_only=True):
        q = self.db.query(Product)
        if active_only:
            q = q.filter(Product.is_active == True)
        return q.all()

    def get(self, product_id):
        return self.db.query(Product).get(product_id)

    def update_stock(self, product_id, delta):
        p = self.get(product_id)
        if p:
            p.stock_qty += delta
            self.db.commit()
            self.db.refresh(p)
        return p

    def update_price(self, product_id, new_buy, new_sell):
        p = self.get(product_id)
        if p:
            ph = PriceHistory(
                product_id=p.id,
                old_price=p.price_sell,
                new_price=new_sell
            )
            self.db.add(ph)
            p.price_buy  = new_buy
            p.price_sell = new_sell
            self.db.commit()
            self.db.refresh(p)
            return p
        return None

    def deactivate(self, product_id):
        p = self.get(product_id)
        if p:
            p.is_active = False
            self.db.commit()
            self.db.refresh(p)
        return p

    def search_by_name(self, text):
        """
        البحث في الاسم أو الرمز (case-insensitive) باستخدام LIKE.
        """
        if not text or text.strip() in ["NO_BARCODE", "بدون باركود", "NONE", ""]:
            # إذا كان البحث فارغاً، نعيد قائمة بآخر 10 منتجات تم إضافتها
            return (
                self.db.query(Product)
                .filter(Product.is_active == True)
                .order_by(Product.id.desc())
                .limit(10)
                .all()
            )

        pattern = f"%{text}%"
        return (
            self.db.query(Product)
            .filter(
                or_(
                    Product.name.ilike(pattern),
                    Product.code.ilike(pattern),
                    # إضافة شرط للبحث عن المنتجات بدون باركود
                    and_(
                        Product.code.in_(["NO_BARCODE", "بدون باركود", "NONE", ""]),
                        Product.name.ilike(pattern)
                    )
                )
            )
            .filter(Product.is_active == True)
            .limit(10)
            .all()
        )

    def get_by_barcode(self, code: str) -> Optional[Product]:
        """البحث عن منتج بالباركود"""
        if not code or code.strip() in ["NO_BARCODE", "بدون باركود", "NONE", ""]:
            return None
        return (
            self.db.query(Product)
            .filter(Product.code == code)
            .filter(Product.is_active == True)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[Product]:
        """البحث عن منتج بالاسم"""
        return (
            self.db.query(Product)
            .filter(Product.name == name)
            .filter(Product.is_active == True)
            .first()
        )

    def get_by_code(self, code: str) -> Optional[Product]:
        """البحث عن منتج بالرمز"""
        return (
            self.db.query(Product)
            .filter(Product.code == code)
            .filter(Product.is_active == True)
            .first()
        )

    @staticmethod
    def create_product(code: str, name: str, unit: str, stock_qty: float, 
                      price_buy: float, price_sell: float) -> Product:
        """إنشاء منتج جديد"""
        try:
            with session_scope() as session:
                product = Product(
                    code=code,
                    name=name,
                    unit=unit,
                    stock_qty=stock_qty,
                    price_buy=price_buy,
                    price_sell=price_sell
                )
                session.add(product)
                
                # تسجيل العملية
                AuditLog.log(
                    session=session,
                    entity='Product',
                    entity_id=product.id,
                    action='create',
                    details=f'تم إنشاء منتج جديد: {name}'
                )
                
                return product
        except IntegrityError as e:
            if 'UNIQUE constraint failed: products.code' in str(e):
                raise ValidationError("رمز المنتج مستخدم مسبقاً")
            elif 'UNIQUE constraint failed: products.name' in str(e):
                raise ValidationError("اسم المنتج مستخدم مسبقاً")
            raise ValidationError("حدث خطأ في قاعدة البيانات")

    @staticmethod
    def get_product_by_code(code: str) -> Product:
        """البحث عن منتج برمزه"""
        with session_scope() as session:
            return session.query(Product).filter(Product.code == code).first()

    @staticmethod
    def get_product_by_name(name: str) -> Product:
        """البحث عن منتج باسمه"""
        with session_scope() as session:
            return session.query(Product).filter(Product.name == name).first()

    @staticmethod
    def search_products(query: str) -> list:
        """البحث عن منتجات"""
        with session_scope() as session:
            return session.query(Product).filter(
                (Product.name.ilike(f'%{query}%')) |
                (Product.code.ilike(f'%{query}%'))
            ).all()

    @staticmethod
    def update_product(product_id: int, **kwargs) -> Product:
        """تحديث بيانات منتج"""
        try:
            with session_scope() as session:
                product = session.query(Product).get(product_id)
                if not product:
                    raise ValidationError("المنتج غير موجود")
                
                # حفظ القيم القديمة للتسجيل
                old_values = {
                    'name': product.name,
                    'code': product.code,
                    'unit': product.unit,
                    'stock_qty': product.stock_qty,
                    'price_buy': product.price_buy,
                    'price_sell': product.price_sell
                }
                
                # تحديث القيم
                for key, value in kwargs.items():
                    setattr(product, key, value)
                
                # تسجيل التغييرات
                changes = {
                    k: {'old': old_values[k], 'new': kwargs.get(k, old_values[k])}
                    for k in kwargs.keys()
                }
                
                AuditLog.log(
                    session=session,
                    entity='Product',
                    entity_id=product.id,
                    action='update',
                    details=f'تم تحديث بيانات المنتج: {product.name}',
                    changes=changes
                )
                
                return product
        except IntegrityError as e:
            if 'UNIQUE constraint failed: products.code' in str(e):
                raise ValidationError("رمز المنتج مستخدم مسبقاً")
            elif 'UNIQUE constraint failed: products.name' in str(e):
                raise ValidationError("اسم المنتج مستخدم مسبقاً")
            raise ValidationError("حدث خطأ في قاعدة البيانات")

    @staticmethod
    def delete_product(product_id: int) -> None:
        """حذف منتج"""
        with session_scope() as session:
            product = session.query(Product).get(product_id)
            if not product:
                raise ValidationError("المنتج غير موجود")
            
            # تسجيل الحذف
            AuditLog.log(
                session=session,
                entity='Product',
                entity_id=product.id,
                action='delete',
                details=f'تم حذف المنتج: {product.name}'
            )
            
            session.delete(product)
