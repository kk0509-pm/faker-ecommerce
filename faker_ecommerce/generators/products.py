"""
Product, product images, and inventory data generators.
"""

import random
from typing import Dict, List, Tuple

import pandas as pd
from faker import Faker
from tqdm import tqdm

from ..config import BATCH_SIZE, CATEGORY_BRANDS, WAREHOUSES
from ..writers import DataWriter


def generate_products(
    n: int,
    categories_df: pd.DataFrame,
    brands_df: pd.DataFrame,
    writer: DataWriter,
    fake: Faker
) -> Tuple[List[int], Dict[int, float]]:
    """
    Generate and write products in batches.
    
    Args:
        n: Number of products to generate
        categories_df: DataFrame of categories
        brands_df: DataFrame of brands
        writer: DataWriter instance
        fake: Faker instance
        
    Returns:
        Tuple of (product IDs list, product prices dict)
    """
    batch = []
    total_written = 0
    category_list = list(CATEGORY_BRANDS.keys())
    product_prices = {}
    
    pbar = tqdm(range(1, n + 1), desc="  Products", unit="rows", ncols=80)
    for i in pbar:
        category_name = random.choice(category_list)
        cat_data = CATEGORY_BRANDS[category_name]
        
        cat_id = categories_df[categories_df['category_name'] == category_name]['category_id'].values[0]
        brand_name = random.choice(cat_data['brands'])
        brand_row = brands_df[brands_df['brand_name'] == brand_name]
        brand_id = brand_row['brand_id'].values[0] if len(brand_row) > 0 else 1
        
        product_template, min_price, max_price = random.choice(cat_data['products'])
        version = random.randint(1, 15)
        product_name = product_template.format(v=version)
        price = round(random.uniform(min_price, max_price), 2)
        
        product_prices[i] = price
        
        batch.append({
            'product_id': i,
            'product_name': f"{brand_name} {product_name}",
            'category_id': cat_id,
            'brand_id': brand_id,
            'description': fake.paragraph(nb_sentences=3),
            'price': price,
            'cost_price': round(price * random.uniform(0.3, 0.6), 2),
            'sku': f"SKU-{category_name[:3].upper()}-{i:06d}",
            'weight_kg': round(random.uniform(0.1, 25.0), 2),
            'is_active': random.choices([True, False], weights=[95, 5])[0],
            'created_at': fake.date_between(start_date='-3y', end_date='today'),
            'rating_avg': round(random.uniform(3.0, 5.0), 1)
        })
        
        if len(batch) >= BATCH_SIZE:
            writer.write_batch('products', batch)
            total_written += len(batch)
            batch = []
            pbar.set_postfix({'written': f'{total_written:,}'})
    
    if batch:
        writer.write_batch('products', batch)
        total_written += len(batch)
    
    return list(range(1, n + 1)), product_prices


def generate_product_images(product_ids: List[int], writer: DataWriter, fake: Faker) -> int:
    """
    Generate and write product images in batches.
    
    Args:
        product_ids: List of product IDs
        writer: DataWriter instance
        fake: Faker instance
        
    Returns:
        Total number of images generated
    """
    batch = []
    img_id = 1
    total_written = 0
    
    pbar = tqdm(product_ids, desc="  Product Images", unit="products", ncols=80)
    for prod_id in pbar:
        num_images = random.choices([1, 2, 3, 4, 5], weights=[20, 30, 30, 15, 5])[0]
        for j in range(num_images):
            batch.append({
                'image_id': img_id,
                'product_id': prod_id,
                'image_url': f"https://cdn.example.com/products/{prod_id}/image_{j+1}.jpg",
                'alt_text': f"Product {prod_id} image {j+1}",
                'is_primary': j == 0,
                'display_order': j + 1
            })
            img_id += 1
        
        if len(batch) >= BATCH_SIZE:
            writer.write_batch('product_images', batch)
            total_written += len(batch)
            batch = []
            pbar.set_postfix({'written': f'{total_written:,}'})
    
    if batch:
        writer.write_batch('product_images', batch)
        total_written += len(batch)
    
    return total_written


def generate_inventory(product_ids: List[int], writer: DataWriter, fake: Faker) -> int:
    """
    Generate and write inventory in batches.
    
    Args:
        product_ids: List of product IDs
        writer: DataWriter instance
        fake: Faker instance
        
    Returns:
        Total number of inventory records generated
    """
    batch = []
    inv_id = 1
    total_written = 0
    
    pbar = tqdm(product_ids, desc="  Inventory", unit="products", ncols=80)
    for prod_id in pbar:
        num_warehouses = random.randint(1, min(4, len(WAREHOUSES)))
        warehouses = random.sample(WAREHOUSES, num_warehouses)
        
        for wh_code, city, state, country in warehouses:
            batch.append({
                'inventory_id': inv_id,
                'product_id': prod_id,
                'warehouse_code': wh_code,
                'quantity_available': random.randint(0, 500),
                'quantity_reserved': random.randint(0, 50),
                'reorder_level': random.randint(10, 50),
                'last_restocked': fake.date_between(start_date='-6m', end_date='today')
            })
            inv_id += 1
        
        if len(batch) >= BATCH_SIZE:
            writer.write_batch('inventory', batch)
            total_written += len(batch)
            batch = []
            pbar.set_postfix({'written': f'{total_written:,}'})
    
    if batch:
        writer.write_batch('inventory', batch)
        total_written += len(batch)
    
    return total_written

