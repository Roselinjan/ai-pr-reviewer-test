"""
inventory_utils.py

Helper functions for checking and reserving stock levels.
"""

from typing import Dict


def check_stock(sku: str, requested_qty: int, stock_levels: Dict[str, int]) -> bool:
    """Return True if there is enough stock for the requested quantity."""
    available = stock_levels.get(sku, 0)
    return available >= requested_qty


def reserve_stock(sku: str, qty: int, stock_levels: Dict[str, int]) -> Dict[str, int]:
    """Deduct the reserved quantity from the stock levels dict."""
    if not check_stock(sku, qty, stock_levels):
        raise ValueError(f"Not enough stock for SKU {sku}")
    stock_levels[sku] -= qty
    return stock_levels


def restock(sku: str, qty: int, stock_levels: Dict[str, int]) -> Dict[str, int]:
    """Add quantity back into stock, e.g. after a cancellation."""
    stock_levels[sku] = stock_levels.get(sku, 0) + qty
    return stock_levels