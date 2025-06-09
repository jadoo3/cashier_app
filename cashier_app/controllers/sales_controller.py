"""Controller handling sales logic."""

from sqlalchemy.orm import Session

from cashier_app.models.sale import Sale, SaleItem
from cashier_app.models.product import Product


class SalesController:
    """Facade between SalesView and the database layer."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_sale(self, payment_type: str) -> Sale:
        sale = Sale(payment_type=payment_type)
        self.db.add(sale)
        self.db.commit()
        return sale

    def add_item(self, sale: Sale, product: Product, qty: int, price: float) -> SaleItem:
        item = SaleItem(sale_id=sale.id, product_id=product.id, qty=qty,
                        unit_price=price, subtotal=qty * price)
        self.db.add(item)
        sale.total += item.subtotal
        self.db.commit()
        return item
