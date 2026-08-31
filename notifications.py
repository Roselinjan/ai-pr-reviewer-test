"""
notifications.py

Sends customer-facing notifications related to order lifecycle events.
"""

import logging

logger = logging.getLogger(__name__)


def send_order_confirmation(customer_id: str, order_id: str) -> None:
    """Send an order confirmation notification to the customer."""
    logger.info("Sending order confirmation to customer %s for order %s", customer_id, order_id)


def send_cancellation_notice(customer_id: str, order_id: str, reason: str) -> None:
    """Send a cancellation notice to the customer."""
    logger.info(
        "Sending cancellation notice to customer %s for order %s (reason: %s)",
        customer_id,
        order_id,
        reason,
    )


def send_shipping_update(customer_id: str, order_id: str, tracking_number: str) -> None:
    """Send a shipping update notification with tracking info."""
    logger.info(
        "Sending shipping update to customer %s for order %s (tracking: %s)",
        customer_id,
        order_id,
        tracking_number,
    )