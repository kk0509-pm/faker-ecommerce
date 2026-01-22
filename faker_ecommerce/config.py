"""
Configuration constants for the faker_postgres package.
"""

# Default batch size for database inserts
BATCH_SIZE = 10000

# Real-world brand data organized by category
CATEGORY_BRANDS = {
    'Electronics': {
        'brands': ['Apple', 'Samsung', 'Sony', 'LG', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'Microsoft', 'Google', 'OnePlus', 'Xiaomi', 'Bose', 'JBL'],
        'products': [
            ('iPhone {v} Pro', 799, 1299), ('Galaxy S{v}', 699, 1199), ('MacBook Pro {v}"', 1299, 2499),
            ('iPad Air', 599, 899), ('Galaxy Tab S{v}', 449, 849), ('Surface Pro {v}', 899, 1599),
            ('Pixel {v}', 599, 999), ('AirPods Pro', 199, 279), ('Galaxy Buds Pro', 149, 229),
            ('WH-1000XM{v} Headphones', 279, 399), ('QuietComfort Earbuds', 249, 329),
            ('4K Smart TV {v}"', 399, 1999), ('OLED TV {v}"', 999, 3499), ('Soundbar {v}00', 199, 799),
            ('Gaming Monitor {v}"', 249, 899), ('Wireless Mouse', 29, 129), ('Mechanical Keyboard', 79, 199),
            ('External SSD {v}TB', 89, 299), ('Portable Charger', 29, 79), ('Smart Watch Series {v}', 249, 599)
        ]
    },
    'Clothing': {
        'brands': ['Nike', 'Adidas', 'Levi\'s', 'Zara', 'H&M', 'Uniqlo', 'Gap', 'Ralph Lauren', 'Tommy Hilfiger', 'Calvin Klein', 'Under Armour', 'Puma', 'The North Face', 'Patagonia', 'Gucci'],
        'products': [
            ('Classic T-Shirt', 19, 89), ('Slim Fit Jeans', 49, 149), ('Hoodie', 39, 129),
            ('Running Shoes', 79, 189), ('Sneakers', 69, 179), ('Dress Shirt', 45, 145),
            ('Casual Blazer', 99, 349), ('Winter Jacket', 129, 499), ('Yoga Pants', 39, 99),
            ('Polo Shirt', 35, 95), ('Cargo Pants', 49, 129), ('Denim Jacket', 79, 199),
            ('Athletic Shorts', 29, 69), ('Wool Sweater', 59, 199), ('Leather Belt', 29, 129),
            ('Baseball Cap', 19, 49), ('Sunglasses', 89, 299), ('Backpack', 49, 199),
            ('Rain Jacket', 79, 249), ('Flannel Shirt', 39, 99)
        ]
    },
    'Home & Kitchen': {
        'brands': ['Dyson', 'KitchenAid', 'Instant Pot', 'Ninja', 'Cuisinart', 'Keurig', 'Breville', 'iRobot', 'Shark', 'Vitamix', 'Le Creuset', 'OXO', 'Calphalon', 'All-Clad', 'Nespresso'],
        'products': [
            ('Vacuum Cleaner V{v}', 299, 699), ('Stand Mixer', 279, 449), ('Pressure Cooker', 79, 149),
            ('Blender Pro', 99, 349), ('Coffee Maker', 49, 299), ('Robot Vacuum', 249, 799),
            ('Air Fryer', 79, 199), ('Food Processor', 99, 299), ('Espresso Machine', 199, 699),
            ('Dutch Oven', 79, 399), ('Cookware Set', 149, 599), ('Knife Set', 79, 349),
            ('Toaster Oven', 79, 249), ('Electric Kettle', 39, 129), ('Hand Mixer', 29, 89),
            ('Dish Set {v}-Piece', 49, 199), ('Bedding Set', 79, 299), ('Bath Towel Set', 39, 129),
            ('Air Purifier', 149, 549), ('Humidifier', 49, 199)
        ]
    },
    'Beauty': {
        'brands': ['L\'Oréal', 'Estée Lauder', 'Clinique', 'MAC', 'Maybelline', 'NYX', 'Urban Decay', 'Fenty Beauty', 'Charlotte Tilbury', 'NARS', 'Olay', 'Neutrogena', 'CeraVe', 'The Ordinary', 'Drunk Elephant'],
        'products': [
            ('Foundation', 19, 59), ('Mascara', 9, 29), ('Lipstick', 12, 39),
            ('Moisturizer', 15, 89), ('Serum', 19, 129), ('Cleanser', 12, 49),
            ('Eyeshadow Palette', 29, 69), ('Setting Spray', 15, 39), ('Concealer', 12, 35),
            ('Bronzer', 19, 49), ('Highlighter', 19, 49), ('Primer', 19, 49),
            ('Face Mask Set', 15, 49), ('Eye Cream', 25, 89), ('Sunscreen SPF{v}', 12, 39),
            ('Toner', 12, 49), ('Body Lotion', 9, 29), ('Lip Gloss', 9, 25),
            ('Perfume {v}ml', 49, 199), ('Hair Serum', 15, 59)
        ]
    },
    'Sports & Outdoors': {
        'brands': ['Nike', 'Adidas', 'Under Armour', 'The North Face', 'Columbia', 'Patagonia', 'Yeti', 'Coleman', 'REI', 'Garmin', 'Fitbit', 'Hydro Flask', 'Osprey', 'Black Diamond', 'Salomon'],
        'products': [
            ('Running Shoes', 89, 199), ('Yoga Mat', 19, 89), ('Dumbbell Set', 49, 299),
            ('Hiking Boots', 99, 249), ('Tent {v}-Person', 99, 499), ('Sleeping Bag', 49, 249),
            ('Cooler {v}qt', 79, 399), ('Fitness Tracker', 79, 299), ('GPS Watch', 199, 599),
            ('Water Bottle', 19, 49), ('Camping Chair', 29, 129), ('Backpack {v}L', 79, 299),
            ('Resistance Bands', 15, 49), ('Foam Roller', 19, 59), ('Jump Rope', 9, 39),
            ('Bike Helmet', 39, 149), ('Ski Goggles', 49, 199), ('Climbing Harness', 49, 149),
            ('Trekking Poles', 39, 129), ('Kayak Paddle', 79, 249)
        ]
    },
    'Books': {
        'brands': ['Penguin Random House', 'HarperCollins', 'Simon & Schuster', 'Hachette', 'Macmillan', 'Scholastic', 'Wiley', 'McGraw Hill', 'O\'Reilly', 'Pearson', 'Oxford University Press', 'Cambridge University Press', 'Bloomsbury', 'Chronicle Books', 'National Geographic'],
        'products': [
            ('Bestselling Novel', 12, 29), ('Mystery Thriller', 10, 25), ('Science Fiction Epic', 12, 28),
            ('Biography', 15, 35), ('Self-Help Guide', 14, 29), ('Cookbook', 19, 45),
            ('History Book', 18, 39), ('Children\'s Book', 8, 22), ('Young Adult Novel', 12, 25),
            ('Business Book', 16, 35), ('Programming Guide', 29, 69), ('Art Book', 25, 89),
            ('Travel Guide', 15, 35), ('Poetry Collection', 12, 28), ('Graphic Novel', 15, 35),
            ('Philosophy Book', 14, 32), ('Psychology Book', 16, 38), ('Fitness Guide', 14, 29),
            ('DIY Manual', 19, 45), ('Language Learning', 18, 49)
        ]
    },
    'Toys & Games': {
        'brands': ['LEGO', 'Hasbro', 'Mattel', 'Nintendo', 'PlayStation', 'Xbox', 'Fisher-Price', 'Hot Wheels', 'Nerf', 'Barbie', 'Funko', 'Ravensburger', 'Melissa & Doug', 'VTech', 'Playmobil'],
        'products': [
            ('Building Set', 19, 199), ('Board Game', 19, 59), ('Action Figure', 12, 49),
            ('Video Game', 39, 69), ('Gaming Console', 299, 549), ('Remote Control Car', 29, 149),
            ('Puzzle {v} Pieces', 12, 39), ('Doll Set', 19, 79), ('Educational Toy', 19, 69),
            ('Card Game', 9, 29), ('Plush Toy', 12, 49), ('Science Kit', 19, 59),
            ('Art Set', 15, 49), ('Musical Toy', 19, 79), ('Outdoor Play Set', 49, 199),
            ('Collectible Figure', 9, 39), ('Strategy Game', 29, 79), ('Train Set', 39, 199),
            ('Drone', 49, 299), ('VR Headset', 299, 549)
        ]
    },
    'Grocery': {
        'brands': ['Whole Foods', 'Trader Joe\'s', 'Organic Valley', 'Annie\'s', 'Kind', 'Clif Bar', 'Nature\'s Path', 'Bob\'s Red Mill', 'Amy\'s', 'Newman\'s Own', 'Stonyfield', 'Horizon', 'Earth\'s Best', 'Kashi', 'RXBar'],
        'products': [
            ('Organic Coffee Beans', 12, 24), ('Granola Bars Pack', 5, 12), ('Olive Oil', 8, 29),
            ('Pasta Sauce', 4, 9), ('Cereal Box', 4, 8), ('Protein Bars', 15, 35),
            ('Organic Milk', 5, 9), ('Almond Butter', 8, 15), ('Trail Mix', 7, 15),
            ('Organic Tea', 6, 14), ('Honey', 8, 18), ('Maple Syrup', 10, 25),
            ('Quinoa', 6, 12), ('Chia Seeds', 8, 16), ('Coconut Oil', 9, 18),
            ('Dark Chocolate', 4, 12), ('Dried Fruit', 6, 14), ('Oatmeal Pack', 5, 12),
            ('Energy Drink Pack', 18, 36), ('Sparkling Water Case', 12, 24)
        ]
    }
}

# Shipping carriers
SHIPPING_CARRIERS = ['FedEx', 'UPS', 'USPS', 'DHL', 'Amazon Logistics', 'OnTrac']

# Warehouse locations
WAREHOUSES = [
    ('WH001', 'Los Angeles', 'CA', 'USA'),
    ('WH002', 'Chicago', 'IL', 'USA'),
    ('WH003', 'New York', 'NY', 'USA'),
    ('WH004', 'Dallas', 'TX', 'USA'),
    ('WH005', 'Seattle', 'WA', 'USA'),
    ('WH006', 'Atlanta', 'GA', 'USA'),
    ('WH007', 'Phoenix', 'AZ', 'USA'),
    ('WH008', 'Denver', 'CO', 'USA'),
]

# Coupon prefixes
COUPON_PREFIXES = ['SAVE', 'DEAL', 'SALE', 'PROMO', 'SPECIAL', 'WELCOME', 'VIP', 'FLASH', 'HOLIDAY', 'SUMMER', 'WINTER', 'SPRING', 'FALL', 'BLACK', 'CYBER']

# Review phrases for sentiment-aware generation
POSITIVE_PHRASES = [
    "Absolutely love this product!", "Best purchase I've made this year.",
    "Exceeded my expectations.", "Great quality for the price.",
    "Would definitely recommend.", "Perfect for everyday use.",
    "Amazing value!", "Exactly what I was looking for."
]

NEUTRAL_PHRASES = [
    "It's okay, nothing special.", "Decent product for the price.",
    "Does what it's supposed to do.", "Average quality.",
    "Met my basic expectations.", "Good but could be better."
]

NEGATIVE_PHRASES = [
    "Not worth the money.", "Disappointed with the quality.",
    "Would not recommend.", "Did not meet expectations.",
    "Had issues from the start.", "Returning this product."
]

# Payment methods and card types
PAYMENT_METHODS = ['credit_card', 'debit_card', 'paypal', 'apple_pay', 'google_pay', 'bank_transfer', 'gift_card']
PAYMENT_METHOD_WEIGHTS = [35, 20, 20, 10, 8, 5, 2]
CARD_TYPES = ['Visa', 'Mastercard', 'American Express', 'Discover']

# Email domains
EMAIL_DOMAINS = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com', 'protonmail.com']

# Dataset size presets
PRESETS = {
    'quick': {
        'customers': 100,
        'products': 50,
        'orders': 300,
        'reviews': 200,
        'wishlists': 100,
        'coupons': 20
    },
    'default': {
        'customers': 100000,
        'products': 5000,
        'orders': 500000,
        'reviews': 200000,
        'wishlists': 50000,
        'coupons': 500
    },
    'xl': {
        'customers': 1000000,
        'products': 50000,
        'orders': 5000000,
        'reviews': 2000000,
        'wishlists': 500000,
        'coupons': 2000
    },
    'xxl': {
        'customers': 1000000,
        'products': 100000,
        'orders': 40000000,
        'reviews': 8000000,
        'wishlists': 500000,
        'coupons': 2000
    }
}

