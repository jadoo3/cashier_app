"""Controller generating simple reports."""

from sqlalchemy.orm import Session
from pandas import DataFrame

from cashier_app.models.sale import Sale, SaleItem


class ReportController:
    """Return pandas DataFrames for basic reports."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def sales_between(self, start, end) -> DataFrame:
        query = (
            self.db.query(Sale)
            .filter(Sale.datetime >= start, Sale.datetime <= end)
        )
        data = [s.__dict__ for s in query]
        return DataFrame(data)
