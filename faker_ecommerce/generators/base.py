"""
Base data generators for categories, brands, warehouses, and coupons.
"""

import random
from datetime import timedelta

import pandas as pd
from faker import Faker

from ..config import CATEGORY_BRANDS, WAREHOUSES, COUPON_PREFIXES
from ..writers import DataWriter


def generate_categories(writer: DataWriter) -> pd.DataFrame:
    """Generate and write product categories."""
    categories = []
    cat_id = 1
    
    for main_cat in CATEGORY_BRANDS.keys():
        categories.append({
            'category_id': cat_id,
            'category_name': main_cat,
            'parent_category_id': None,
            'description': f'All {main_cat.lower()} products'
        })
        cat_id += 1
    
    df = pd.DataFrame(categories)
    writer.write_dataframe('categories', df)
    return df


def generate_brands(writer: DataWriter) -> pd.DataFrame:
    """Generate and write brands."""
    brands = []
    brand_id = 1
    seen_brands = set()
    
    for category, data in CATEGORY_BRANDS.items():
        for brand_name in data['brands']:
            if brand_name not in seen_brands:
                clean_name = brand_name.lower().replace(' ', '').replace("'", '')
                brands.append({
                    'brand_id': brand_id,
                    'brand_name': brand_name,
                    'country_of_origin': random.choice(['USA', 'Japan', 'Germany', 'South Korea', 'France', 'Italy', 'UK', 'Sweden', 'China']),
                    'founded_year': random.randint(1850, 2020),
                    'website': f"https://www.{clean_name}.com"
                })
                seen_brands.add(brand_name)
                brand_id += 1
    
    df = pd.DataFrame(brands)
    writer.write_dataframe('brands', df)
    return df


def generate_warehouses(writer: DataWriter) -> pd.DataFrame:
    """Generate and write warehouse records."""
    warehouses = []
    fake = Faker()
    
    for wh_code, city, state, country in WAREHOUSES:
        warehouses.append({
            'warehouse_code': wh_code,
            'warehouse_name': f"{city} Distribution Center",
            'city': city,
            'state': state,
            'country': country,
            'capacity_sqft': random.randint(50000, 500000),
            'manager_name': fake.name()
        })
    
    df = pd.DataFrame(warehouses)
    writer.write_dataframe('warehouses', df)
    return df


def generate_coupons(n: int, writer: DataWriter, fake: Faker) -> pd.DataFrame:
    """Generate and write coupons."""
    coupons = []
    
    for i in range(1, n + 1):
        prefix = random.choice(COUPON_PREFIXES)
        discount_type = random.choice(['percentage', 'fixed_amount'])
        
        if discount_type == 'percentage':
            discount_value = random.choice([5, 10, 15, 20, 25, 30, 40, 50])
            min_order = random.choice([0, 25, 50, 75, 100])
        else:
            discount_value = random.choice([5, 10, 15, 20, 25, 50])
            min_order = discount_value * random.choice([2, 3, 4, 5])
        
        start_date = fake.date_between(start_date='-2y', end_date='+1m')
        
        coupons.append({
            'coupon_id': i,
            'coupon_code': f"{prefix}{discount_value}{random.randint(100, 999)}",
            'description': f"Get {discount_value}{'%' if discount_type == 'percentage' else '$'} off your order",
            'discount_type': discount_type,
            'discount_value': discount_value,
            'min_order_amount': min_order,
            'max_uses': random.choice([None, 100, 500, 1000, 5000]),
            'times_used': 0,
            'start_date': start_date,
            'end_date': start_date + timedelta(days=random.randint(7, 90)),
            'is_active': random.choices([True, False], weights=[70, 30])[0]
        })
    
    df = pd.DataFrame(coupons)
    writer.write_dataframe('coupons', df)
    return df

