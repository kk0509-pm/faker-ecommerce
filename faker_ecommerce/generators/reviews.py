"""
Reviews, wishlists, and coupon usage data generators.
"""

import random
from typing import List

import pandas as pd
from faker import Faker
from tqdm import tqdm

from ..config import BATCH_SIZE, POSITIVE_PHRASES, NEUTRAL_PHRASES, NEGATIVE_PHRASES
from ..writers import DataWriter


def generate_reviews(
    n: int,
    customer_ids: List[int],
    product_ids: List[int],
    writer: DataWriter,
    fake: Faker
) -> int:
    """
    Generate and write reviews in batches.
    
    Args:
        n: Number of reviews to generate
        customer_ids: List of customer IDs
        product_ids: List of product IDs
        writer: DataWriter instance
        fake: Faker instance
        
    Returns:
        Total number of reviews generated
    """
    batch = []
    total_written = 0
    
    pbar = tqdm(range(1, n + 1), desc="  Reviews", unit="rows", ncols=80)
    for i in pbar:
        rating = random.choices([1, 2, 3, 4, 5], weights=[5, 8, 15, 32, 40])[0]
        
        if rating >= 4:
            base_text = random.choice(POSITIVE_PHRASES)
        elif rating == 3:
            base_text = random.choice(NEUTRAL_PHRASES)
        else:
            base_text = random.choice(NEGATIVE_PHRASES)
        
        review_text = f"{base_text} {fake.sentence(nb_words=random.randint(5, 15))}"
        
        batch.append({
            'review_id': i,
            'product_id': random.choice(product_ids),
            'customer_id': random.choice(customer_ids),
            'rating': rating,
            'title': fake.sentence(nb_words=random.randint(3, 8)).rstrip('.'),
            'review_text': review_text,
            'verified_purchase': random.choices([True, False], weights=[80, 20])[0],
            'helpful_votes': random.randint(0, 500),
            'review_date': fake.date_between(start_date='-3y', end_date='today')
        })
        
        if len(batch) >= BATCH_SIZE:
            writer.write_batch('product_reviews', batch)
            total_written += len(batch)
            batch = []
            pbar.set_postfix({'written': f'{total_written:,}'})
    
    if batch:
        writer.write_batch('product_reviews', batch)
        total_written += len(batch)
    
    return total_written


def generate_wishlists(
    n: int,
    customer_ids: List[int],
    product_ids: List[int],
    writer: DataWriter,
    fake: Faker
) -> int:
    """
    Generate and write wishlists in batches.
    
    Args:
        n: Number of wishlist items to generate
        customer_ids: List of customer IDs
        product_ids: List of product IDs
        writer: DataWriter instance
        fake: Faker instance
        
    Returns:
        Total number of wishlist items generated
    """
    batch = []
    total_written = 0
    
    pbar = tqdm(range(1, n + 1), desc="  Wishlists", unit="rows", ncols=80)
    for i in pbar:
        batch.append({
            'wishlist_id': i,
            'customer_id': random.choice(customer_ids),
            'product_id': random.choice(product_ids),
            'added_date': fake.date_between(start_date='-2y', end_date='today'),
            'priority': random.choices(['low', 'medium', 'high'], weights=[40, 40, 20])[0],
            'notes': fake.sentence() if random.random() < 0.2 else None
        })
        
        if len(batch) >= BATCH_SIZE:
            writer.write_batch('wishlists', batch)
            total_written += len(batch)
            batch = []
            pbar.set_postfix({'written': f'{total_written:,}'})
    
    if batch:
        writer.write_batch('wishlists', batch)
        total_written += len(batch)
    
    return total_written


def generate_coupon_usage(orders_data: List[dict], writer: DataWriter) -> int:
    """
    Generate and write coupon usage records.
    
    Args:
        orders_data: List of order dictionaries
        writer: DataWriter instance
        
    Returns:
        Total number of coupon usage records generated
    """
    usage = []
    usage_id = 1
    
    for order in orders_data:
        if order['coupon_id'] is not None:
            usage.append({
                'usage_id': usage_id,
                'coupon_id': order['coupon_id'],
                'order_id': order['order_id'],
                'customer_id': order['customer_id'],
                'discount_applied': order['discount_amount'],
                'used_at': order['order_date']
            })
            usage_id += 1
    
    if usage:
        df = pd.DataFrame(usage)
        writer.write_dataframe('coupon_usage', df)
    
    return len(usage)

