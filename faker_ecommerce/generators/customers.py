"""
Customer and address data generators.
"""

import random
from typing import List

from faker import Faker
from tqdm import tqdm

from ..config import BATCH_SIZE, EMAIL_DOMAINS
from ..writers import DataWriter


def generate_customers(n: int, writer: DataWriter, fake: Faker) -> List[int]:
    """
    Generate and write customer data in batches.
    
    Args:
        n: Number of customers to generate
        writer: DataWriter instance
        fake: Faker instance
        
    Returns:
        List of customer IDs
    """
    batch = []
    total_written = 0
    
    pbar = tqdm(range(1, n + 1), desc="  Customers", unit="rows", ncols=80)
    for i in pbar:
        first_name = fake.first_name()
        last_name = fake.last_name()
        domain = random.choice(EMAIL_DOMAINS)
        batch.append({
            'customer_id': i,
            'first_name': first_name,
            'last_name': last_name,
            'email': f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{domain}",
            'phone': fake.phone_number(),
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80),
            'gender': random.choices(['Male', 'Female', 'Non-binary', 'Prefer not to say'], weights=[45, 45, 5, 5])[0],
            'signup_date': fake.date_between(start_date='-5y', end_date='today'),
            'is_active': random.choices([True, False], weights=[90, 10])[0],
            'loyalty_points': random.randint(0, 50000),
            'preferred_language': random.choice(['en', 'es', 'fr', 'de', 'zh', 'ja', 'pt'])
        })
        
        if len(batch) >= BATCH_SIZE:
            writer.write_batch('customers', batch)
            total_written += len(batch)
            batch = []
            pbar.set_postfix({'written': f'{total_written:,}'})
    
    if batch:
        writer.write_batch('customers', batch)
        total_written += len(batch)
    
    return list(range(1, n + 1))


def generate_addresses(customer_ids: List[int], writer: DataWriter, fake: Faker) -> int:
    """
    Generate and write customer addresses in batches.
    
    Args:
        customer_ids: List of customer IDs
        writer: DataWriter instance
        fake: Faker instance
        
    Returns:
        Maximum address ID (total count)
    """
    batch = []
    addr_id = 1
    total_written = 0
    
    pbar = tqdm(customer_ids, desc="  Addresses", unit="customers", ncols=80)
    for cust_id in pbar:
        num_addresses = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
        for j in range(num_addresses):
            addr_type = 'billing' if j == 0 else random.choice(['shipping', 'billing'])
            batch.append({
                'address_id': addr_id,
                'customer_id': cust_id,
                'address_type': addr_type,
                'street_address': fake.street_address(),
                'city': fake.city(),
                'state': fake.state_abbr(),
                'postal_code': fake.postcode(),
                'country': random.choices(['USA', 'Canada', 'UK', 'Germany', 'France', 'Australia'], weights=[70, 10, 5, 5, 5, 5])[0],
                'is_default': j == 0
            })
            addr_id += 1
        
        if len(batch) >= BATCH_SIZE:
            writer.write_batch('addresses', batch)
            total_written += len(batch)
            batch = []
            pbar.set_postfix({'written': f'{total_written:,}'})
    
    if batch:
        writer.write_batch('addresses', batch)
        total_written += len(batch)
    
    return addr_id - 1

