import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from models.product import Product, OutOfStockError


def test_product_creation():
    p = Product(code="001", name="apple", unit="kg", stock_qty=5, price_buy=1.0, price_sell=1.5)
    assert p.name == "apple"
    assert p.price_sell >= p.price_buy


def test_out_of_stock_error():
    p = Product(code="002", name="banana", unit="kg", stock_qty=2, price_buy=0.5, price_sell=1.0)
    with pytest.raises(OutOfStockError):
        p.withdraw(3)
