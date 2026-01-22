"""
Command-line interface for faker_ecommerce.
"""

import argparse
import getpass

from . import config


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog='faker_ecommerce',
        description="Generate realistic e-commerce test data for PostgreSQL or Parquet files.",
        epilog="Output options: Use --username for PostgreSQL or --parquet-dir for Parquet files."
    )
    
    # Data size options
    size_group = parser.add_argument_group('Data size options')
    size_group.add_argument(
        "--customers", type=int, default=config.PRESETS['default']['customers'],
        help=f"Number of customers (default: {config.PRESETS['default']['customers']:,})"
    )
    size_group.add_argument(
        "--products", type=int, default=config.PRESETS['default']['products'],
        help=f"Number of products (default: {config.PRESETS['default']['products']:,})"
    )
    size_group.add_argument(
        "--orders", type=int, default=config.PRESETS['default']['orders'],
        help=f"Number of orders, each with 1-5 items (default: {config.PRESETS['default']['orders']:,})"
    )
    size_group.add_argument(
        "--reviews", type=int, default=config.PRESETS['default']['reviews'],
        help=f"Number of product reviews (default: {config.PRESETS['default']['reviews']:,})"
    )
    size_group.add_argument(
        "--wishlists", type=int, default=config.PRESETS['default']['wishlists'],
        help=f"Number of wishlist items (default: {config.PRESETS['default']['wishlists']:,})"
    )
    size_group.add_argument(
        "--coupons", type=int, default=config.PRESETS['default']['coupons'],
        help=f"Number of coupons (default: {config.PRESETS['default']['coupons']})"
    )
    size_group.add_argument(
        "--batch-size", type=int, default=config.BATCH_SIZE,
        help=f"Batch size for writes (default: {config.BATCH_SIZE:,})"
    )
    
    # Output options
    output_group = parser.add_argument_group('Output options (choose one)')
    output_group.add_argument(
        "--username", type=str,
        help="PostgreSQL username (enables PostgreSQL output)"
    )
    output_group.add_argument(
        "--host", type=str, default="localhost",
        help="PostgreSQL host (default: localhost)"
    )
    output_group.add_argument(
        "--port", type=int, default=5432,
        help="PostgreSQL port (default: 5432)"
    )
    output_group.add_argument(
        "--database", type=str,
        help="PostgreSQL database name"
    )
    output_group.add_argument(
        "--parquet-dir", type=str,
        help="Directory for Parquet output (enables Parquet output)"
    )
    
    # Presets
    preset_group = parser.add_argument_group('Size presets')
    preset_group.add_argument(
        "--quick", action="store_true",
        help="Generate a small quick sample dataset"
    )
    preset_group.add_argument(
        "--xl", action="store_true",
        help="Generate an extra-large dataset"
    )
    preset_group.add_argument(
        "--xxl", action="store_true",
        help="Generate an extra-extra-large dataset"
    )

    args = parser.parse_args()
    
    # Validate output options
    if args.username and args.parquet_dir:
        parser.error("Please choose either --username (PostgreSQL) or --parquet-dir (Parquet), not both.")
    elif args.username:
        if not args.database:
            parser.error("--database is required when using PostgreSQL output.")
    elif not args.parquet_dir:
        parser.error("Please specify an output: --username for PostgreSQL or --parquet-dir for Parquet files.")
    
    return args


def apply_presets(args):
    """Apply size presets to arguments."""
    if args.quick:
        print("🚀 Quick mode enabled: using small dataset sizes.")
        preset = config.PRESETS['quick']
    elif args.xl:
        print("🔥 XL mode enabled: using large dataset sizes.")
        preset = config.PRESETS['xl']
    elif args.xxl:
        print("🔥🔥 XXL mode enabled: using extra-large dataset sizes.")
        preset = config.PRESETS['xxl']
    else:
        return args
    
    args.customers = preset['customers']
    args.products = preset['products']
    args.orders = preset['orders']
    args.reviews = preset['reviews']
    args.wishlists = preset['wishlists']
    args.coupons = preset['coupons']
    
    return args


def get_password(args):
    """Prompt for password if using PostgreSQL."""
    if args.username:
        return getpass.getpass("Password: ")
    return None

