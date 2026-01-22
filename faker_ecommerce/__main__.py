"""
Main entry point for the faker_ecommerce package.

Run with: uv run -m faker_ecommerce [options]
"""

import random

import numpy as np
from faker import Faker
from sqlalchemy import create_engine

from . import config
from .cli import parse_args, apply_presets, get_password
from .writers import DataWriter
from .generators import (
    generate_categories,
    generate_brands,
    generate_warehouses,
    generate_coupons,
    generate_customers,
    generate_addresses,
    generate_products,
    generate_product_images,
    generate_inventory,
    generate_orders_with_items,
    generate_payments,
    generate_shipments,
    generate_reviews,
    generate_wishlists,
    generate_coupon_usage,
)


def main():
    """Main entry point for data generation."""
    # Parse arguments
    args = parse_args()
    args = apply_presets(args)
    
    # Set batch size globally
    config.BATCH_SIZE = args.batch_size
    
    # Get password if needed
    password = get_password(args)
    
    # Initialize random seeds for reproducibility
    fake = Faker()
    Faker.seed(42)
    random.seed(42)
    np.random.seed(42)
    
    # Determine output type
    output_type = 'postgres' if args.username else 'parquet'
    
    print(f"\n🚀 Starting data generation (batch size: {config.BATCH_SIZE:,})...")
    print(f"   Output: {output_type.upper()}")
    print("=" * 60)
    
    # Create writer
    if output_type == 'postgres':
        db_connection_str = f'postgresql+psycopg2://{args.username}:{password}@{args.host}:{args.port}/{args.database}'
        engine = create_engine(db_connection_str)
        writer = DataWriter('postgres', engine=engine)
    else:
        writer = DataWriter('parquet', parquet_dir=args.parquet_dir)
        print(f"   Parquet directory: {args.parquet_dir}")
    
    row_counts = {}
    
    # 1. Categories
    print("  Categories: generating...")
    categories_df = generate_categories(writer)
    row_counts['categories'] = len(categories_df)
    print(f"  ✓ Categories: {len(categories_df)} rows")
    
    # 2. Brands
    print("  Brands: generating...")
    brands_df = generate_brands(writer)
    row_counts['brands'] = len(brands_df)
    print(f"  ✓ Brands: {len(brands_df)} rows")
    
    # 3. Warehouses
    print("  Warehouses: generating...")
    warehouses_df = generate_warehouses(writer)
    row_counts['warehouses'] = len(warehouses_df)
    print(f"  ✓ Warehouses: {len(warehouses_df)} rows")
    
    # 4. Coupons
    print("  Coupons: generating...")
    coupons_df = generate_coupons(args.coupons, writer, fake)
    row_counts['coupons'] = len(coupons_df)
    print(f"  ✓ Coupons: {len(coupons_df)} rows")
    
    # 5. Customers
    customer_ids = generate_customers(args.customers, writer, fake)
    row_counts['customers'] = len(customer_ids)
    
    # 6. Addresses
    max_address_id = generate_addresses(customer_ids, writer, fake)
    row_counts['addresses'] = max_address_id
    
    # 7. Products
    product_ids, product_prices = generate_products(
        args.products, categories_df, brands_df, writer, fake
    )
    row_counts['products'] = len(product_ids)
    
    # 8. Product Images
    img_count = generate_product_images(product_ids, writer, fake)
    row_counts['product_images'] = img_count
    
    # 9. Inventory
    inv_count = generate_inventory(product_ids, writer, fake)
    row_counts['inventory'] = inv_count
    
    # 10 & 11. Orders and Order Items
    coupon_ids = coupons_df['coupon_id'].tolist() if len(coupons_df) > 0 else []
    orders_data, orders_written, items_written = generate_orders_with_items(
        args.orders, customer_ids, max_address_id, coupon_ids,
        product_ids, product_prices, coupons_df, writer, fake
    )
    row_counts['orders'] = orders_written
    row_counts['order_items'] = items_written
    
    # 12. Payments
    pay_count = generate_payments(orders_data, writer, fake)
    row_counts['payments'] = pay_count
    
    # 13. Shipments
    ship_count = generate_shipments(orders_data, writer, fake)
    row_counts['shipments'] = ship_count
    
    # 14. Reviews
    review_count = generate_reviews(args.reviews, customer_ids, product_ids, writer, fake)
    row_counts['product_reviews'] = review_count
    
    # 15. Wishlists
    wish_count = generate_wishlists(args.wishlists, customer_ids, product_ids, writer, fake)
    row_counts['wishlists'] = wish_count
    
    # 16. Coupon Usage
    print("  Coupon Usage: generating...")
    usage_count = generate_coupon_usage(orders_data, writer)
    row_counts['coupon_usage'] = usage_count
    print(f"  ✓ Coupon Usage: {usage_count} rows")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Data generation complete!")
    print(f"   Output type: {output_type.upper()}")
    if output_type == 'parquet':
        print(f"   Output directory: {args.parquet_dir}")
    print(f"   Total tables: {len(row_counts)}")
    total_rows = sum(row_counts.values())
    print(f"   Total rows: {total_rows:,}")
    print("\n   Row counts per table:")
    for table, count in row_counts.items():
        print(f"     {table}: {count:,}")


if __name__ == "__main__":
    main()

