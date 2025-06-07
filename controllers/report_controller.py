import pandas as pd
from database.db_session import SessionLocal
from models.sale import Sale
from models.product import Product
from models.creditor import Creditor

class ReportController:
    def __init__(self):
        self.db = SessionLocal()

    def sales_report(self, start_date=None, end_date=None):
        stmt = self.db.query(
            Sale.id,
            Sale.date_time,
            Creditor.name.label('creditor'),
            Sale.total,
            Sale.paid
        ).outerjoin(Creditor)
        if start_date:
            stmt = stmt.filter(Sale.date_time >= start_date)
        if end_date:
            stmt = stmt.filter(Sale.date_time <= end_date)
        return pd.read_sql(stmt.statement, self.db.bind)

    def low_stock(self, threshold=10.0):
        stmt = self.db.query(
            Product.id,
            Product.code,
            Product.name,
            Product.stock_qty
        ).filter(Product.stock_qty <= threshold)
        return pd.read_sql(stmt.statement, self.db.bind)
