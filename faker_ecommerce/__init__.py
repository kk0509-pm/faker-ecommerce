"""
faker_ecommerce - Generate realistic e-commerce test data for PostgreSQL or Parquet files.

This package generates synthetic data for a complete e-commerce database schema
including customers, products, orders, reviews, and more.
"""

__version__ = "0.1.0"
__author__ = "faker-ecommerce"

from .config import BATCH_SIZE
from .writers import DataWriter

__all__ = ["DataWriter", "BATCH_SIZE"]

