import pytest

from .exceptions import (
    InsufficientStockError,
    InvalidProductError,
    ProductNotFoundError,
)
from .models import PerishableProduct, Product
from .engine import Inventory


def test_product():
    product = Product("P1", "Pen", 10, 5)
    assert product.quantity == 10

    product.quantity = 8
    product.price = 6

    assert product.price == 6.0

    with pytest.raises(InvalidProductError):
        product.quantity = -1


def test_inheritance():
    product = PerishableProduct(
        "P2", "Milk", 5, 30, "2026-12-31"
    )

    assert isinstance(product, Product)
    assert product.expiry_date == "2026-12-31"


def test_inventory_sell():
    inventory = Inventory()
    inventory.add_product(Product("P1", "Pen", 3, 5))

    inventory.sell("P1", 2)

    assert inventory.get_product("P1").quantity == 1


def test_insufficient_stock():
    inventory = Inventory()
    inventory.add_product(Product("P1", "Pen", 3, 5))

    with pytest.raises(InsufficientStockError):
        inventory.sell("P1", 5)


def test_product_not_found():
    inventory = Inventory()

    with pytest.raises(ProductNotFoundError):
        inventory.get_product("BAD")


def test_json_persistence(tmp_path):
    inventory = Inventory()
    inventory.add_product(Product("P1", "Pen", 3, 5))

    path = tmp_path / "inventory.json"
    inventory.save_json(path)

    loaded = Inventory.load_json(path)

    assert loaded.get_product("P1").quantity == 3


def test_csv_persistence(tmp_path):
    inventory = Inventory()
    inventory.add_product(Product("P1", "Pen", 3, 5))

    path = tmp_path / "inventory.csv"
    inventory.save_csv(path)

    text = path.read_text(encoding="utf-8")

    assert "product_id" in text
    assert "P1" in text


def test_invalid_product_type():
    inventory = Inventory()

    with pytest.raises(TypeError):
        inventory.add_product("not a product")


def test_invalid_perishable_product():
    with pytest.raises(InvalidProductError):
        PerishableProduct("P2", "Milk", 2, 30, "")
