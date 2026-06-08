import random
import uuid
from datetime import datetime

from faker import Faker

fake = Faker()

# === PRODUCT DATA GENERATION ===
CATALOG = [
    {"name": "Cordless Handheld Vacuum", "brand": "Dyson", "category": "Appliances", "price": 299.99},
    {"name": "Non-Stick Ceramic Frying Pan", "brand": "Tefal", "category": "Cookware", "price": 45.50},
    {"name": "Smart LED Desk Lamp", "brand": "Philips", "category": "Lighting", "price": 62.00},
    {"name": "Electric Kettle 1.7L", "brand": "Bosch", "category": "Appliances", "price": 38.00},
    {"name": "Memory Foam Bed Pillow", "brand": "SleepWell", "category": "Bedding", "price": 55.99},
    {"name": "Automatic Coffee Maker", "brand": "DeLonghi", "category": "Kitchenware", "price": 185.00},
    {"name": "Microfiber Bath Towel Set", "brand": "CottonSoft", "category": "Textiles", "price": 22.75},
    {"name": "Stainless Steel Mixing Bowl", "brand": "KitchenAid", "category": "Cookware", "price": 29.99},
    {"name": "Digital Bathroom Scale", "brand": "Xiaomi", "category": "Electronics", "price": 32.50},
    {"name": "Wall Mounted Mirror", "brand": "IKEA", "category": "Decor", "price": 75.00},
]

product_cache = {}

def product_info_generator():
    product_id = fake.numerify(text="########")

    if product_id not in product_cache:
        item = random.choice(CATALOG)
        product_cache[product_id] = {
            "product_name": item["name"],
            "brand": item["brand"],
            "category_l1": item["category"],
            "color": fake.color_name(),
            "cost_price": item["price"],
        }

    data = product_cache[product_id]

    return {
        "product_id": product_id,
        "product_name": data["product_name"],
        "brand": data["brand"],
        "category_l1": data["category_l1"],
        "color": data["color"],
        "cost_price": data["cost_price"],
    }


# === ORDER DATA GENERATION ===
def order_info_generator(product_id: str, unit_price: float):
    order_id = fake.numerify(text="########")

    return {
        "order_id": order_id,
        "order_item_id": product_id,           
        "order_date": fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d"),
        "order_status": random.choice(["Order Formed", "Processing", "Shipped", "Delivered", "Cancelled"]),
        "payment_method": random.choice(["Credit Card", "PayPal", "Bank Transfer", "Cash on Delivery", "Apple Pay"]),
        "sales_channel": random.choice(["Website", "Mobile App", "Instagram Store", "Marketplace", "Physical Store"]),
        "quantity": random.randint(1, 10),
        "unit_price": unit_price,              
    }


# === CUSTOMER DATA GENERATION ===
geo_data = {
    "Ukraine": {"Lviv": "79000", "Kyiv": "01001", "Odesa": "65000"},
    "Poland": {"Warsaw": "00-001", "Krakow": "31-001", "Gdansk": "80-001"},
    "Germany": {"Berlin": "10115", "Munich": "80331", "Hamburg": "20095"},
    "France": {"Paris": "75001", "Lyon": "69001", "Nice": "06000"},
    "Italy": {"Rome": "00144", "Milan": "20121", "Florence": "50121"},
    "Spain": {"Madrid": "28001", "Barcelona": "08001", "Valencia": "46001"},
    "USA": {"New York": "10001", "Los Angeles": "90001", "Chicago": "60601"},
    "Canada": {"Toronto": "M5H 2N2", "Vancouver": "V6B 1A1", "Montreal": "H2Z 1A1"},
    "UK": {"London": "SW1A 1AA", "Manchester": "M1 1AD", "Birmingham": "B1 1BB"},
    "Japan": {"Tokyo": "100-0001", "Osaka": "530-0001", "Kyoto": "600-8000"},
}

def customer_info_generator():
    gender = random.choice(["male", "female"])
    first_name = fake.first_name_male() if gender == "male" else fake.first_name_female()
    last_name = fake.last_name_male() if gender == "male" else fake.last_name_female()

    country = random.choice(list(geo_data.keys()))
    city = random.choice(list(geo_data[country].keys()))

    return {
        "customer_id": fake.numerify(text="########"),  
        "first_name": first_name,
        "last_name": last_name,
        "email": f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}",
        "phone": fake.phone_number(),
        "date_of_birth": str(fake.date_of_birth(minimum_age=18, maximum_age=80)),
        "gender": gender,
        "registration_date": str(fake.date_between(start_date="-2y", end_date="today")),
        "loyalty_tier": random.choice(["free", "silver", "gold"]),
        "country": country,
        "city": city,
        "postal_code": geo_data[country][city],
    }


# === MAIN GENERATOR ===
def create_json_record() -> dict:
    product = product_info_generator()
    customer = customer_info_generator()

    order = order_info_generator(
        product_id=product["product_id"],
        unit_price=product["cost_price"],
    )

    return {
        "event_id": f"evt_{uuid.uuid4()}",
        "event_timestamp": datetime.now().isoformat(),
        "order": order,
        "customer": customer,
        "product": product,
    }

def generate_data(n: int):
    data = []
    
    for i in range(n):
        record = create_json_record()
        data.append(record)
    return data


if __name__ == "__main__":
    generate_data()
