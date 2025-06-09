"""Product controller handling CRUD operations."""

from sqlalchemy.orm import Session

from cashier_app.models.product import Product


class OutOfStockError(Exception):
    """Raised when product quantity is insufficient."""


class ProductController:
    """Controller for interacting with Product model."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def add_product(self, name: str, barcode: str, buy_price: float, sell_price: float, quantity: int = 0) -> Product:
        product = Product(name=name, barcode=barcode, buy_price=buy_price, sell_price=sell_price, quantity=quantity)
        self.db.add(product)
        self.db.commit()
        return product

    def get_by_barcode(self, barcode: str) -> Product | None:
        return self.db.query(Product).filter_by(barcode=barcode).first()
