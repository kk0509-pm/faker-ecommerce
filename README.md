# faker-ecommerce

Generate realistic e-commerce test data for PostgreSQL or Parquet files. This tool creates a complete 16-table e-commerce database schema with realistic data including real brand names, product names, and customer information.

## Features

- **16 interconnected tables** with proper relationships
- **Real-world brand names** (Apple, Nike, Sony, etc.) organized by category
- **Realistic data patterns** (sentiment-aware reviews, proper price ranges)
- **Dual output support**: PostgreSQL or Parquet files
- **Batch processing** for memory-efficient generation of large datasets
- **Progress tracking** with detailed progress bars
- **Configurable sizes** from quick tests to XXL datasets

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd faker-postgres

# Install dependencies with uv
uv sync
```

## Quick Start

### Generate to Parquet files (no database required)

```bash
uv run -m faker_ecommerce --parquet-dir ./data --quick
```

### Generate to PostgreSQL

```bash
# First, set up the database (optional helper script)
./setup_db.sh myuser mypassword ecommerce_db

# Generate data
uv run -m faker_ecommerce --username myuser --database ecommerce_db --quick
```

## Usage

```bash
uv run -m faker_ecommerce [OPTIONS]
```

### Output Options (choose one)

| Option | Description |
|--------|-------------|
| `--username USER` | PostgreSQL username (enables PostgreSQL output) |
| `--database DB` | PostgreSQL database name (required with --username) |
| `--host HOST` | PostgreSQL host (default: localhost) |
| `--port PORT` | PostgreSQL port (default: 5432) |
| `--parquet-dir DIR` | Directory for Parquet output (enables Parquet output) |

### Data Size Options

| Option | Description | Default |
|--------|-------------|---------|
| `--customers N` | Number of customers | 100,000 |
| `--products N` | Number of products | 5,000 |
| `--orders N` | Number of orders (1-5 items each) | 500,000 |
| `--reviews N` | Number of product reviews | 200,000 |
| `--wishlists N` | Number of wishlist items | 50,000 |
| `--coupons N` | Number of coupons | 500 |
| `--batch-size N` | Batch size for writes | 10,000 |

### Size Presets

| Preset | Description |
|--------|-------------|
| `--quick` | Small dataset for quick testing (~2K rows) |
| `--xl` | Large dataset (~10M+ rows) |
| `--xxl` | Extra-large dataset (~50M+ rows) |

## Examples

### Quick test with Parquet output

```bash
uv run -m faker_ecommerce --parquet-dir ./test_data --quick
```

### Medium dataset to PostgreSQL

```bash
uv run -m faker_ecommerce \
    --username ecom_user \
    --database ecommerce \
    --customers 10000 \
    --products 1000 \
    --orders 50000
```

### Large dataset with custom batch size

```bash
uv run -m faker_ecommerce \
    --parquet-dir ./large_data \
    --xl \
    --batch-size 50000
```

### Remote PostgreSQL server

```bash
uv run -m faker_ecommerce \
    --username admin \
    --host db.example.com \
    --port 5432 \
    --database ecommerce \
    --quick
```

## Database Schema

The generated schema includes 16 tables with the following relationships:

```mermaid
erDiagram
    customers ||--o{ addresses : has
    customers ||--o{ orders : places
    customers ||--o{ product_reviews : writes
    customers ||--o{ wishlists : creates
    customers ||--o{ coupon_usage : uses

    categories ||--o{ products : contains
    brands ||--o{ products : manufactures

    products ||--o{ product_images : has
    products ||--o{ inventory : stocked_in
    products ||--o{ order_items : included_in
    products ||--o{ product_reviews : receives
    products ||--o{ wishlists : added_to

    warehouses ||--o{ inventory : stores
    warehouses ||--o{ shipments : ships_from

    coupons ||--o{ orders : applied_to
    coupons ||--o{ coupon_usage : tracked_in

    orders ||--o{ order_items : contains
    orders ||--o{ payments : paid_by
    orders ||--o{ shipments : shipped_as
    orders ||--o{ coupon_usage : redeems
    orders }o--|| addresses : ships_to
    orders }o--|| addresses : bills_to

    customers {
        int customer_id PK
        string first_name
        string last_name
        string email
        string phone
        date date_of_birth
        string gender
        date signup_date
        boolean is_active
        int loyalty_points
        string preferred_language
    }

    addresses {
        int address_id PK
        int customer_id FK
        string address_type
        string street_address
        string city
        string state
        string postal_code
        string country
        boolean is_default
    }

    categories {
        int category_id PK
        string category_name
        int parent_category_id FK
        string description
    }

    brands {
        int brand_id PK
        string brand_name
        string country_of_origin
        int founded_year
        string website
    }

    products {
        int product_id PK
        string product_name
        int category_id FK
        int brand_id FK
        string description
        decimal price
        decimal cost_price
        string sku
        decimal weight_kg
        boolean is_active
        date created_at
        decimal rating_avg
    }

    product_images {
        int image_id PK
        int product_id FK
        string image_url
        string alt_text
        boolean is_primary
        int display_order
    }

    inventory {
        int inventory_id PK
        int product_id FK
        string warehouse_code FK
        int quantity_available
        int quantity_reserved
        int reorder_level
        date last_restocked
    }

    warehouses {
        string warehouse_code PK
        string warehouse_name
        string city
        string state
        string country
        int capacity_sqft
        string manager_name
    }

    coupons {
        int coupon_id PK
        string coupon_code
        string description
        string discount_type
        decimal discount_value
        decimal min_order_amount
        int max_uses
        int times_used
        date start_date
        date end_date
        boolean is_active
    }

    orders {
        int order_id PK
        int customer_id FK
        int shipping_address_id FK
        int billing_address_id FK
        datetime order_date
        string status
        decimal subtotal
        decimal discount_amount
        decimal tax_amount
        decimal shipping_cost
        decimal total_amount
        int coupon_id FK
        string notes
    }

    order_items {
        int order_item_id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
        decimal discount
        decimal total_price
    }

    payments {
        int payment_id PK
        int order_id FK
        string payment_method
        string card_type
        string card_last_four
        decimal amount
        string currency
        string status
        string transaction_id
        datetime payment_date
    }

    shipments {
        int shipment_id PK
        int order_id FK
        string carrier
        string tracking_number
        date shipped_date
        date estimated_delivery
        date actual_delivery
        string status
        string warehouse_code FK
    }

    product_reviews {
        int review_id PK
        int product_id FK
        int customer_id FK
        int rating
        string title
        string review_text
        boolean verified_purchase
        int helpful_votes
        date review_date
    }

    wishlists {
        int wishlist_id PK
        int customer_id FK
        int product_id FK
        date added_date
        string priority
        string notes
    }

    coupon_usage {
        int usage_id PK
        int coupon_id FK
        int order_id FK
        int customer_id FK
        decimal discount_applied
        datetime used_at
    }
```

### Table Overview

#### Reference Tables
- **categories** - Product categories (Electronics, Clothing, etc.)
- **brands** - Real brand names (Apple, Nike, Sony, etc.)
- **warehouses** - Distribution center locations
- **coupons** - Discount coupons

#### Customer Tables
- **customers** - Customer profiles with demographics
- **addresses** - Billing and shipping addresses

#### Product Tables
- **products** - Products with realistic names and pricing
- **product_images** - Product image records
- **inventory** - Stock levels per warehouse

#### Order Tables
- **orders** - Customer orders with totals
- **order_items** - Individual items in orders
- **payments** - Payment transactions
- **shipments** - Shipping and delivery info

#### Engagement Tables
- **product_reviews** - Customer reviews with sentiment-aware text
- **wishlists** - Customer wishlists
- **coupon_usage** - Coupon redemption tracking

## Output Structure

### PostgreSQL
Tables are created directly in the specified database with appropriate data types.

### Parquet
```
<parquet-dir>/
├── categories.parquet
├── brands.parquet
├── warehouses.parquet
├── customers.parquet
├── addresses.parquet
├── coupons.parquet
├── products.parquet
├── product_images.parquet
├── inventory.parquet
├── orders.parquet
├── order_items.parquet
├── payments.parquet
├── shipments.parquet
├── product_reviews.parquet
├── wishlists.parquet
└── coupon_usage.parquet
```

## Real Brand Names by Category

| Category | Example Brands |
|----------|---------------|
| Electronics | Apple, Samsung, Sony, Dell, HP, Bose |
| Clothing | Nike, Adidas, Levi's, Zara, The North Face |
| Home & Kitchen | Dyson, KitchenAid, Instant Pot, iRobot |
| Beauty | L'Oréal, Estée Lauder, MAC, Fenty Beauty |
| Sports & Outdoors | Nike, Yeti, Garmin, Patagonia, Columbia |
| Books | Penguin Random House, O'Reilly, HarperCollins |
| Toys & Games | LEGO, Nintendo, PlayStation, Hasbro |
| Grocery | Whole Foods, Trader Joe's, Kind, Clif Bar |
