class InventoryError(Exception):
    """Base exception for inventory operations."""


class InvalidProductError(InventoryError):
    """Raised when product data is invalid."""


class ProductNotFoundError(InventoryError):
    """Raised when a product ID does not exist."""


class InsufficientStockError(InventoryError):
    """Raised when requested stock is unavailable."""
