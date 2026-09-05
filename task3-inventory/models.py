from dataclasses import dataclass


@dataclass
class Product:
    product_id: str
    name: str
    _quantity: int
    _price: float

    def __post_init__(self):
        if not self.product_id.strip() or not self.name.strip():
            from .exceptions import InvalidProductError
            raise InvalidProductError("Product ID and name are required.")

        self.quantity = self._quantity
        self.price = self._price

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        from .exceptions import InvalidProductError

        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise InvalidProductError(
                "Quantity must be a non-negative integer."
            )

        self._quantity = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        from .exceptions import InvalidProductError

        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            raise InvalidProductError(
                "Price must be a non-negative number."
            )

        self._price = float(value)

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "type": self.__class__.__name__,
        }


class PerishableProduct(Product):
    def __init__(self, product_id, name, quantity, price, expiry_date):
        if not expiry_date.strip():
            from .exceptions import InvalidProductError
            raise InvalidProductError("Expiry date is required.")

        super().__init__(product_id, name, quantity, price)
        self.expiry_date = expiry_date

    def to_dict(self):
        data = super().to_dict()
        data["expiry_date"] = self.expiry_date
        return data
