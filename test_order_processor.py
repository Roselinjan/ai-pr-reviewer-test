"""
test_order_processor.py

Existing test coverage for order_processor.py.
"""

import pytest

from order_processor import (
    OrderItem,
    Order,
    create_order,
    calculate_subtotal,
    calculate_order_total,
    process_payment,
    cancel_order,
    FREE_SHIPPING_THRESHOLD,
)


@pytest.fixture
def sample_items():
    return [
        OrderItem(sku="SKU-1", name="Widget", unit_price=15.00, quantity=2),
    ]


@pytest.fixture
def sample_order(sample_items):
    return create_order("ORD-1001", "CUST-1", sample_items)


def test_create_order_success(sample_items):
    order = create_order("ORD-1001", "CUST-1", sample_items)
    assert order.order_id == "ORD-1001"
    assert order.customer_id == "CUST-1"
    assert order.status == "pending"
    assert len(order.items) == 1


def test_create_order_with_no_items_raises():
    with pytest.raises(ValueError):
        create_order("ORD-1002", "CUST-1", [])


def test_calculate_subtotal(sample_order):
    # 2 * 15.00 = 30.00
    assert calculate_subtotal(sample_order) == 30.00


def test_calculate_order_total_below_free_shipping_threshold(sample_order):
    # subtotal = 30.00, below the $50 threshold -> shipping should apply
    total = calculate_order_total(sample_order)
    subtotal = 30.00
    expected_tax = round(subtotal * 0.0725, 2)
    expected_total = round(subtotal + expected_tax + 5.99, 2)
    assert total == expected_total


def test_calculate_order_total_above_free_shipping_threshold():
    items = [OrderItem(sku="SKU-2", name="Gadget", unit_price=25.00, quantity=3)]
    order = create_order("ORD-1003", "CUST-2", items)
    # subtotal = 75.00, above the $50 threshold -> free shipping
    total = calculate_order_total(order)
    subtotal = 75.00
    expected_tax = round(subtotal * 0.0725, 2)
    expected_total = round(subtotal + expected_tax, 2)
    assert total == expected_total


def test_process_payment_success(monkeypatch, sample_order):
    monkeypatch.setenv("PAYMENT_GATEWAY_API_KEY", "test-key-123")
    response = process_payment(sample_order, 45.50)
    assert response["status"] == "success"
    assert response["order_id"] == sample_order.order_id
    assert sample_order.status == "paid"


def test_process_payment_missing_api_key_raises(monkeypatch, sample_order):
    monkeypatch.delenv("PAYMENT_GATEWAY_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        process_payment(sample_order, 45.50)


def test_cancel_order_sets_status(sample_order):
    cancelled = cancel_order(sample_order, "customer requested")
    assert cancelled.status == "cancelled"