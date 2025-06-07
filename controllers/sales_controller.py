from datetime import datetime
from database.db_session import SessionLocal
from models.sale import Sale
from models.sale_item import SaleItem
from models.product import Product
from models.creditor import Creditor
from sqlalchemy import func

class SalesController:
    def __init__(self):
        self.db = SessionLocal()
        self.model = Sale()

    def get_next_invoice_number(self):
        """الحصول على رقم الفاتورة التالي"""
        # البحث عن آخر رقم فاتورة في قاعدة البيانات
        last_sale = self.db.query(Sale).order_by(Sale.invoice_number.desc()).first()
        if last_sale:
            return last_sale.invoice_number + 1
        return 1  # إذا لم تكن هناك فواتير سابقة

    def create(self, invoice_number, items, total_amount, paid_amount):
        """إنشاء فاتورة جديدة"""
        sale = Sale(
            invoice_number=invoice_number,
            total_amount=total_amount,
            paid_amount=paid_amount
        )
        self.db.add(sale)
        self.db.flush()  # للحصول على معرف الفاتورة

        # إضافة عناصر الفاتورة
        for item in items:
            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=item['product_id'],
                qty=item['qty'],
                price=item['price']
            )
            self.db.add(sale_item)

        self.db.commit()
        return sale

    def list(self, start_date=None, end_date=None):
        q = self.db.query(Sale)
        if start_date:
            q = q.filter(Sale.date_time >= start_date)
        if end_date:
            q = q.filter(Sale.date_time <= end_date)
        return q.all()

    def get(self, sale_id):
        return self.db.query(Sale).get(sale_id)

    def list_all(self):
        """قائمة بجميع الفواتير"""
        return self.db.query(Sale).all()

    def get_by_id(self, id):
        """الحصول على فاتورة بواسطة المعرف"""
        return self.db.query(Sale).get(id)

    def get_by_invoice_number(self, invoice_number):
        """الحصول على فاتورة بواسطة رقم الفاتورة"""
        return self.db.query(Sale).filter_by(invoice_number=invoice_number).first()

    def update(self, sale):
        """تحديث بيانات الفاتورة"""
        self.db.commit()
        return sale

    def delete(self, id):
        """حذف فاتورة"""
        sale = self.get_by_id(id)
        if sale:
            self.db.delete(sale)
            self.db.commit()
            return True
        return False
