"""
order_processor.py

Core order-processing logic for the e-commerce checkout flow.
Handles order creation, total calculation, and payment submission.
"""

import os
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

FREE_SHIPPING_THRESHOLD = 50.00
STANDARD_SHIPPING_COST = 5.99
TAX_RATE = 0.0725


@dataclass
class OrderItem:
    sku: str
    name: str
    unit_price: float
    quantity: int


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: List[OrderItem]
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "pending"


def create_order(order_id: str, customer_id: str, items: List[OrderItem]) -> Order:
    """Create a new Order object from a list of items."""
    if not items:
        raise ValueError("Cannot create an order with no items")
    return Order(order_id=order_id, customer_id=customer_id, items=items)


def calculate_subtotal(order: Order) -> float:
    """Sum unit_price * quantity across all items in the order."""
    return sum(item.unit_price * item.quantity for item in order.items)


def calculate_order_total(order: Order) -> float:
    """
    Calculate the final order total, including tax and shipping.

    Orders that meet or exceed FREE_SHIPPING_THRESHOLD (based on subtotal)
    qualify for free shipping.
    """
    subtotal = calculate_subtotal(order)
    tax = subtotal * TAX_RATE

    if subtotal >= FREE_SHIPPING_THRESHOLD:
        shipping = 0.0
    else:
        shipping = STANDARD_SHIPPING_COST

    total = subtotal + tax + shipping
    return round(total, 2)


def get_payment_api_key() -> str:
    """Fetch the payment gateway API key from the environment."""
    api_key = os.environ.get("PAYMENT_GATEWAY_API_KEY")
    if not api_key:
        raise RuntimeError("PAYMENT_GATEWAY_API_KEY is not set")
    return api_key


def process_payment(order: Order, amount: float) -> dict:
    """
    Submit a payment for the given order to the payment gateway.

    Returns a dict representing the (simulated) gateway response.
    """
    api_key = get_payment_api_key()
    logger.info("Processing payment for order %s, amount=%.2f", order.order_id, amount)

    # Simulated gateway call
    response = {
        "order_id": order.order_id,
        "amount_charged": amount,
        "status": "success",
        "auth_code": f"AUTH-{order.order_id}",
    }
    order.status = "paid"
    return response


def cancel_order(order: Order, reason: str) -> Order:
    """Mark an order as cancelled with a given reason."""
    if order.status == "paid":
        logger.warning("Cancelling a paid order: %s", order.order_id)
    order.status = "cancelled"
    logger.info("Order %s cancelled: %s", order.order_id, reason)
    return order