import csv
import json
from pathlib import Path

from .exceptions import InsufficientStockError, ProductNotFoundError
from .models import PerishableProduct, Product


class Inventory:
    def __init__(self):
        self._products = {}

    @property
    def products(self):
        return dict(self._products)

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("product must be a Product instance")
        self._products[product.product_id] = product

    def get_product(self, product_id):
        try:
            return self._products[product_id]
        except KeyError:
            raise ProductNotFoundError(f"Product not found: {product_id}")

    def sell(self, product_id, quantity):
        product = self.get_product(product_id)

        if quantity <= 0:
            raise ValueError("Sale quantity must be positive.")

        if product.quantity < quantity:
            raise InsufficientStockError("Insufficient stock.")

        product.quantity -= quantity

    def save_json(self, path):
        data = [product.to_dict() for product in self._products.values()]
        Path(path).write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )

    def save_csv(self, path):
        data = [product.to_dict() for product in self._products.values()]
        fields = [
            "product_id",
            "name",
            "quantity",
            "price",
            "type",
            "expiry_date"
        ]

        with Path(path).open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fields,
                extrasaction="ignore"
            )
            writer.writeheader()

            for item in data:
                writer.writerow(item)

    @classmethod
    def load_json(cls, path):
        inventory = cls()

        data = json.loads(
            Path(path).read_text(encoding="utf-8")
        )

        for item in data:
            if item.get("type") == "PerishableProduct":
                product = PerishableProduct(
                    item["product_id"],
                    item["name"],
                    item["quantity"],
                    item["price"],
                    item["expiry_date"]
                )
            else:
                product = Product(
                    item["product_id"],
                    item["name"],
                    item["quantity"],
                    item["price"]
                )

            inventory.add_product(product)

        return inventory
