"""Basic sanity tests for models."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from cashier_app.models import Product


def test_product_fields() -> None:
    product = Product(name="test", barcode="123", buy_price=1, sell_price=2)
    assert product.name == "test"
    assert product.barcode == "123"
