"""
Order, order items, payments, and shipments data generators.
"""

import random
from datetime import timedelta
from typing import Dict, List, Tuple

import pandas as pd
from faker import Faker
from tqdm import tqdm

from ..config import (
    BATCH_SIZE, SHIPPING_CARRIERS, WAREHOUSES,
    PAYMENT_METHODS, PAYMENT_METHOD_WEIGHTS, CARD_TYPES
)
from ..writers import DataWriter


def generate_orders_with_items(
    n_orders: int,
    customer_ids: List[int],
    max_address_id: int,
    coupon_ids: List[int],
    product_ids: List[int],
    product_prices: Dict[int, float],
    coupons_df: pd.DataFrame,
    writer: DataWriter,
    fake: Faker
) -> Tuple[List[dict], int, int]:
    """
    Generate and write orders with their items together in batches.
    
    Args:
        n_orders: Number of orders to generate
        customer_ids: List of customer IDs
        max_address_id: Maximum address ID
        coupon_ids: List of coupon IDs
        product_ids: List of product IDs
        product_prices: Dict mapping product ID to price
        coupons_df: DataFrame of coupons
        writer: DataWriter instance
        fake: Faker instance
        
    Returns:
        Tuple of (orders data list, orders count, items count)
    """
    orders_batch = []
    items_batch = []
    
    total_orders_written = 0
    total_items_written = 0
    order_item_id = 1
    
    orders_data = []
    
    # Build coupon lookup
    coupon_lookup = {}
    if coupons_df is not None and len(coupons_df) > 0:
        for _, row in coupons_df.iterrows():
            coupon_lookup[row['coupon_id']] = {
                'discount_type': row['discount_type'],
                'discount_value': row['discount_value']
            }
    
    pbar = tqdm(range(1, n_orders + 1), desc="  Orders + Items", unit="orders", ncols=80)
    for order_id in pbar:
        customer_id = random.choice(customer_ids)
        
        shipping_addr = random.randint(1, max_address_id)
        billing_addr_id = random.randint(1, max_address_id)
        
        coupon_id = None
        if random.random() < 0.2 and coupon_ids:
            coupon_id = random.choice(coupon_ids)
        
        order_date = fake.date_time_between(start_date='-4y', end_date='now')
        status = random.choices(
            ['pending', 'processing', 'shipped', 'delivered', 'cancelled', 'returned'],
            weights=[5, 10, 15, 60, 5, 5]
        )[0]
        
        shipping_cost = round(random.choice([0, 4.99, 7.99, 9.99, 14.99]), 2)
        
        # Generate order items (1-5 items per order)
        num_items = random.choices([1, 2, 3, 4, 5], weights=[30, 30, 20, 12, 8])[0]
        subtotal = 0.0
        
        for _ in range(num_items):
            product_id = random.choice(product_ids)
            quantity = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 15, 7, 3])[0]
            
            unit_price = product_prices.get(product_id, round(random.uniform(10, 500), 2))
            
            item_discount = 0
            if random.random() < 0.15:
                item_discount = round(unit_price * random.choice([0.05, 0.10, 0.15, 0.20]), 2)
            
            item_total = round((unit_price - item_discount) * quantity, 2)
            subtotal += item_total
            
            items_batch.append({
                'order_item_id': order_item_id,
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'discount': item_discount,
                'total_price': item_total
            })
            order_item_id += 1
        
        # Calculate order totals
        discount_amount = 0.0
        if coupon_id is not None and coupon_id in coupon_lookup:
            coupon = coupon_lookup[coupon_id]
            if coupon['discount_type'] == 'percentage':
                discount_amount = round(subtotal * (coupon['discount_value'] / 100), 2)
            else:
                discount_amount = min(coupon['discount_value'], subtotal)
        
        tax_amount = round(subtotal * 0.08, 2)
        total_amount = round(subtotal - discount_amount + tax_amount + shipping_cost, 2)
        
        order_data = {
            'order_id': order_id,
            'customer_id': customer_id,
            'shipping_address_id': shipping_addr,
            'billing_address_id': billing_addr_id,
            'order_date': order_date,
            'status': status,
            'subtotal': round(subtotal, 2),
            'discount_amount': discount_amount,
            'tax_amount': tax_amount,
            'shipping_cost': shipping_cost,
            'total_amount': total_amount,
            'coupon_id': coupon_id,
            'notes': fake.sentence() if random.random() < 0.1 else None
        }
        
        orders_batch.append(order_data)
        orders_data.append(order_data)
        
        # Flush batches
        if len(orders_batch) >= BATCH_SIZE:
            writer.write_batch('orders', orders_batch)
            total_orders_written += len(orders_batch)
            orders_batch = []
            
            writer.write_batch('order_items', items_batch)
            total_items_written += len(items_batch)
            items_batch = []
            
            pbar.set_postfix({
                'orders': f'{total_orders_written:,}',
                'items': f'{total_items_written:,}'
            })
    
    # Write remaining
    if orders_batch:
        writer.write_batch('orders', orders_batch)
        total_orders_written += len(orders_batch)
    
    if items_batch:
        writer.write_batch('order_items', items_batch)
        total_items_written += len(items_batch)
    
    return orders_data, total_orders_written, total_items_written


def generate_payments(orders_data: List[dict], writer: DataWriter, fake: Faker) -> int:
    """
    Generate and write payments in batches.
    
    Args:
        orders_data: List of order dictionaries
        writer: DataWriter instance
        fake: Faker instance
        
    Returns:
        Total number of payments generated
    """
    batch = []
    payment_id = 1
    total_written = 0
    
    pbar = tqdm(orders_data, desc="  Payments", unit="orders", ncols=80)
    for order in pbar:
        if order['status'] not in ['pending']:
            status = 'completed' if order['status'] in ['shipped', 'delivered'] else 'pending'
            if order['status'] == 'cancelled':
                status = random.choice(['refunded', 'cancelled'])
            
            method = random.choices(PAYMENT_METHODS, weights=PAYMENT_METHOD_WEIGHTS)[0]
            
            batch.append({
                'payment_id': payment_id,
                'order_id': order['order_id'],
                'payment_method': method,
                'card_type': random.choice(CARD_TYPES) if method in ['credit_card', 'debit_card'] else None,
                'card_last_four': f"{random.randint(1000, 9999)}" if method in ['credit_card', 'debit_card'] else None,
                'amount': order['total_amount'],
                'currency': 'USD',
                'status': status,
                'transaction_id': fake.uuid4(),
                'payment_date': order['order_date'] + timedelta(minutes=random.randint(1, 60))
            })
            payment_id += 1
        
        if len(batch) >= BATCH_SIZE:
            writer.write_batch('payments', batch)
            total_written += len(batch)
            batch = []
            pbar.set_postfix({'written': f'{total_written:,}'})
    
    if batch:
        writer.write_batch('payments', batch)
        total_written += len(batch)
    
    return total_written


def generate_shipments(orders_data: List[dict], writer: DataWriter, fake: Faker) -> int:
    """
    Generate and write shipments in batches.
    
    Args:
        orders_data: List of order dictionaries
        writer: DataWriter instance
        fake: Faker instance
        
    Returns:
        Total number of shipments generated
    """
    batch = []
    shipment_id = 1
    total_written = 0
    
    pbar = tqdm(orders_data, desc="  Shipments", unit="orders", ncols=80)
    for order in pbar:
        if order['status'] in ['shipped', 'delivered']:
            order_date = order['order_date']
            ship_date = order_date + timedelta(days=random.randint(1, 3))
            
            carrier = random.choice(SHIPPING_CARRIERS)
            
            if order['status'] == 'delivered':
                delivery_date = ship_date + timedelta(days=random.randint(2, 7))
                status = 'delivered'
            else:
                delivery_date = None
                status = random.choice(['in_transit', 'out_for_delivery'])
            
            batch.append({
                'shipment_id': shipment_id,
                'order_id': order['order_id'],
                'carrier': carrier,
                'tracking_number': f"{carrier[:3].upper()}{random.randint(100000000000, 999999999999)}",
                'shipped_date': ship_date,
                'estimated_delivery': ship_date + timedelta(days=random.randint(3, 7)),
                'actual_delivery': delivery_date,
                'status': status,
                'warehouse_code': random.choice(WAREHOUSES)[0]
            })
            shipment_id += 1
        
        if len(batch) >= BATCH_SIZE:
            writer.write_batch('shipments', batch)
            total_written += len(batch)
            batch = []
            pbar.set_postfix({'written': f'{total_written:,}'})
    
    if batch:
        writer.write_batch('shipments', batch)
        total_written += len(batch)
    
    return total_written

