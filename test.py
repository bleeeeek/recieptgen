from flask import Flask, render_template
import random
from datetime import datetime, timedelta
from math import ceil

app = Flask(__name__)

# Currency configurations
CURRENCIES = {
    "MYR": {"symbol": "RM", "rate": 1.0, "name": "Malaysian Ringgit"},
    "BHD": {"symbol": "BD", "rate": 0.083, "name": "Bahraini Dinar"},
    "INR": {"symbol": "₹", "rate": 17.25, "name": "Indian Rupee"},
    "USD": {"symbol": "$", "rate": 0.21, "name": "US Dollar"},
    "EUR": {"symbol": "€", "rate": 0.19, "name": "Euro"}
}

# Payment methods
PAYMENT_METHODS = [
    "CASH",
    "VISA ****1234",
    "MASTERCARD ****5678",
    "AMEX ****9012",
    "E-WALLET",
    "MOBILE PAY"
]

# Company and store information
company_info = {
    "BERJAYA COFFEE": {
        "company_name": "BERJAYA STARBUCKS COFFEE COMPANY SDN BHD",
        "legal_name": "BERJAYA FOOD TRADING SDN BHD",
        "tax_id": "GST ID: 001234567890",
        "service_tax_id": "SERVICE TAX ID: WID-1558-31025875",
        "company_number": "Company No. 157251-A",
        "halal_cert": "HALAL CERT: JAKIM-HD28185",
        "business_license": "LICENSE: KL-2024-123456",
        "food_license": "FOOD LICENSE: FL-789012",
        "address": "Level 15, West Wing, Berjaya Times Square\n1, Jalan Imbi, 55100 Kuala Lumpur, Malaysia",
        "phone": "Tel: 1-300-80-8888",
        "fax": "Fax: +603-2141-0555",
        "website": "www.starbucks.com.my",
        "email": "customerservice@starbucks.com.my",
        "currency": "MYR",
        "region": "MY-14",
        "store_type": "FLAGSHIP STORE",
        "tax_rate": 0.06,
        "service_charge": 0.10
    },
    "STARCITY CAFE": {
        "company_name": "STARCITY COFFEE & BEVERAGES PTE LTD",
        "legal_name": "STARCITY HOLDINGS PTE LTD",
        "tax_id": "GST REG: M8-0123456-7",
        "service_tax_id": "SERVICE TAX ID: SCC-2558-41025875",
        "company_number": "UEN: 202312345K",
        "halal_cert": "HALAL CERT: MUIS-HC-N23-2024",
        "business_license": "LICENSE: SG-2024-78901",
        "food_license": "NEA LICENSE: FE2023-12345",
        "address": "123 City Plaza\n#01-23 Singapore 123456",
        "phone": "Tel: +65 6789 0123",
        "fax": "Fax: +65 6789 0124",
        "website": "www.starcity.com.sg",
        "email": "info@starcity.com.sg",
        "currency": "BHD",
        "region": "SG-05",
        "store_type": "PREMIUM OUTLET",
        "tax_rate": 0.08,
        "service_charge": 0.12
    },
    "COFFEE HOUSE": {
        "company_name": "COFFEE HOUSE INTERNATIONAL LLC",
        "legal_name": "GLOBAL BEVERAGES HOLDINGS INC.",
        "tax_id": "TAX ID: 98-7654321",
        "service_tax_id": "FOOD SERVICE LICENSE: FSL-3558-51025875",
        "company_number": "Business Reg: BRN-55512345",
        "halal_cert": "HALAL CERT: HMC-2024-789",
        "business_license": "LICENSE: CA-2024-456789",
        "food_license": "FDA: FD-123-456-789",
        "address": "888 Coffee Street\nSuite 100, Beverly Hills, CA 90210",
        "phone": "Tel: (888) COFFEE-1",
        "fax": "Fax: (888) COFFEE-2",
        "website": "www.coffeehouse.com",
        "email": "support@coffeehouse.com",
        "currency": "USD",
        "region": "US-CA",
        "store_type": "CONCEPT STORE",
        "tax_rate": 0.0925,
        "service_charge": 0.15
    }
}

# Store locations
store_locations = [
    "Downtown Mall #123",
    "Westside Plaza #456",
    "Eastside Market #789",
    "North Station #321",
    "South Center #654",
    "Central Square #987",
    "Harbor View #147",
    "University District #258",
    "Suburban Market #369",
    "Metro Express #741",
    "BERJAYA COFFEE #875",
    "STARCITY CAFE #654",
    "COFFEE HOUSE #432"
]

# Updated items with halal-compliant options
items = {
    "Cafe & Coffee": {
        "Iced Latte": (4.50, 6.99),
        "Hot Americano": (3.50, 5.99),
        "Caramel Macchiato": (5.50, 7.99),
        "Mocha Frappuccino": (5.99, 8.99),
        "Espresso Shot": (2.50, 3.99),
        "Cold Brew": (4.50, 6.99),
        "Green Tea Latte": (4.99, 6.99),
        "Hot Chocolate": (3.99, 5.99),
        "Chai Tea Latte": (4.50, 6.99),
        "Vanilla Sweet Cream": (4.99, 7.99),
        "Cafe Misto": (3.50, 5.50),
        "Cappuccino": (3.99, 5.99),
        # Halal-certified food items
        "Butter Croissant (Halal)": (2.99, 4.99),
        "Chocolate Muffin (Halal)": (2.99, 4.99),
        "Cheese & Egg Sandwich": (5.99, 8.99),
        "Tuna Sandwich": (5.99, 8.99),
        "Veggie Protein Box": (7.99, 11.99),
        "Date Cookie": (1.99, 3.99),
        "Banana Bread (Halal)": (2.99, 4.99),
        "Fresh Fruit Cup": (3.99, 6.99)
    },
    "Produce": {
        "Apples (lb)": (0.50, 3.99),
        "Bananas (lb)": (0.15, 0.35),
        "Carrots (bag)": (0.99, 2.99),
        "Tomatoes (lb)": (1.99, 4.99),
        "Lettuce (head)": (1.49, 2.99),
        "Potatoes (5lb)": (2.99, 6.99),
        "Onions (3lb)": (2.79, 4.99),
        "Broccoli (bunch)": (1.99, 3.99),
        "Spinach (bag)": (2.49, 4.99),
        "Avocados": (0.99, 2.99),
        "Bell Peppers": (0.79, 2.49),
        "Mushrooms (8oz)": (1.99, 4.99),
        "Dates (12oz)": (4.99, 8.99),
        "Fresh Figs (8oz)": (3.99, 7.99)
    },
    "Dairy & Eggs": {
        "Milk (gallon, Halal)": (2.99, 5.99),
        "Eggs (dozen)": (2.99, 6.99),
        "Cheese (8oz, Halal)": (3.99, 7.99),
        "Yogurt (32oz, Halal)": (3.99, 5.99),
        "Butter (16oz, Halal)": (2.99, 5.99),
        "Cream Cheese (8oz, Halal)": (2.49, 4.99),
        "Heavy Cream (16oz, Halal)": (3.49, 5.99),
        "Sour Cream (16oz, Halal)": (1.99, 3.99),
        "Almond Milk (64oz)": (3.49, 5.99),
        "String Cheese (12pk, Halal)": (3.99, 5.99)
    },
    "Pantry": {
        "Flatbread": (1.99, 4.99),
        "Rice (5lb)": (4.99, 12.99),
        "Dates Syrup": (4.99, 8.99),
        "Cereal (18oz, Halal)": (2.99, 5.99),
        "Coffee (12oz, Halal)": (5.99, 12.99),
        "Tea (20bags)": (3.99, 8.99),
        "Flour (5lb, Halal)": (2.99, 6.99),
        "Sugar (4lb)": (2.49, 5.99),
        "Olive Oil (48oz)": (8.99, 15.99),
        "Hummus (16oz)": (3.99, 6.99),
        "Honey (12oz)": (4.99, 8.99),
        "Lentil Soup": (1.49, 3.99),
        "Tuna (Halal)": (0.99, 2.99),
        "Tahini (12oz)": (4.99, 8.99)
    },
    "Meat & Seafood": {
        "Chicken Breast (lb, Halal)": (4.99, 9.99),
        "Ground Beef (lb, Halal)": (4.99, 8.99),
        "Lamb (lb, Halal)": (8.99, 15.99),
        "Fish Fillet (lb)": (5.99, 9.99),
        "Shrimp (lb)": (9.99, 16.99),
        "Turkey (lb, Halal)": (5.99, 11.99),
        "Halal Beef Sausage": (4.99, 8.99),
        "Halal Chicken Wings": (4.99, 8.99),
        "Halal Deli Turkey (lb)": (7.99, 12.99),
        "Halal Shawarma Meat": (8.99, 14.99)
    },
    "Snacks": {
        "Mixed Nuts (12oz)": (4.99, 9.99),
        "Dried Fruits": (3.99, 7.99),
        "Halal Crackers": (2.49, 4.99),
        "Date Bars": (2.99, 4.99),
        "Trail Mix": (3.99, 6.99),
        "Granola (Halal)": (2.99, 4.99),
        "Rice Cakes": (1.99, 3.99),
        "Fruit Leather": (1.99, 3.99),
        "Sesame Snacks": (2.49, 4.99),
        "Halal Protein Bars": (2.99, 4.99)
    },
    "Beverages": {
        "Soda (2L)": (1.99, 2.99),
        "Water (24pk)": (3.99, 6.99),
        "Orange Juice (64oz)": (3.99, 6.99),
        "Energy Drinks": (1.99, 4.99),
        "Sports Drinks": (1.49, 3.99),
        "Sparkling Water (12pk)": (3.99, 5.99),
        "Coffee Pods (12ct)": (6.99, 12.99),
        "Green Tea (24pk)": (4.99, 8.99),
        "Coconut Water": (2.99, 4.99),
        "Mango Lassi": (3.99, 5.99)
    },
    "Household": {
        "Paper Towels (6pk)": (5.99, 9.99),
        "Toilet Paper (12pk)": (7.99, 14.99),
        "Trash Bags (40ct)": (8.99, 14.99),
        "Laundry Detergent": (9.99, 17.99),
        "Dish Soap": (2.99, 4.99),
        "Sponges (3pk)": (2.49, 4.99),
        "All-Purpose Cleaner": (3.99, 6.99),
        "Air Freshener": (2.99, 5.99),
        "Light Bulbs (4pk)": (4.99, 9.99),
        "Batteries AA (8pk)": (5.99, 11.99),
        "Zip Bags (50ct)": (3.99, 6.99),
        "Glass Cleaner": (3.49, 5.99),
        "Broom": (8.99, 14.99),
        "Mop": (9.99, 16.99),
        "Dustpan": (2.99, 4.99)
    },
    "Personal Care": {
        "Shampoo": (3.99, 8.99),
        "Conditioner": (3.99, 8.99),
        "Body Wash": (3.99, 7.99),
        "Deodorant": (2.99, 5.99),
        "Toothpaste": (2.99, 4.99),
        "Toothbrush": (1.99, 4.99),
        "Hand Soap": (2.49, 4.99),
        "Hand Sanitizer": (1.99, 4.99),
        "Tissues (160ct)": (2.99, 4.99),
        "Band-Aids (30ct)": (3.49, 5.99),
        "Pain Reliever": (4.99, 8.99),
        "Cotton Swabs (500ct)": (2.99, 4.99),
        "Lotion": (4.99, 8.99),
        "Sunscreen": (6.99, 12.99),
        "Face Wash": (5.99, 9.99),
        "Dental Floss": (2.49, 4.99),
        "Mouthwash": (3.99, 7.99)
    },
    "Office & School": {
        "Notebooks": (0.99, 3.99),
        "Printer Paper": (4.99, 8.99),
        "Pens (10pk)": (2.99, 6.99),
        "Pencils (12pk)": (1.99, 4.99),
        "Markers": (3.99, 7.99),
        "Tape": (1.99, 3.99),
        "Scissors": (2.99, 6.99),
        "Glue Stick": (1.49, 3.99),
        "Sticky Notes": (2.49, 4.99),
        "Stapler": (4.99, 8.99),
        "Paper Clips (100ct)": (1.49, 2.99),
        "Binder": (3.99, 7.99),
        "Calculator": (8.99, 14.99),
        "Highlighters (5pk)": (2.99, 5.99),
        "File Folders (12pk)": (3.99, 7.99)
    }
}

def get_company_type(store_location):
    if "BERJAYA" in store_location:
        return "BERJAYA COFFEE"
    elif "STARCITY" in store_location:
        return "STARCITY CAFE"
    elif "COFFEE HOUSE" in store_location:
        return "COFFEE HOUSE"
    return None

def format_currency(amount, currency_info):
    """Format amount in the specified currency"""
    converted = amount * currency_info["rate"]
    return f"{currency_info['symbol']}{converted:.2f}"

def generate_receipt():
    # Randomly select a store location
    global store_location
    store_location = random.choice(store_locations)
    
    receipt_items = []
    total = 0
    
    # Get company info and currency
    company_type = get_company_type(store_location)
    store_info = company_info.get(company_type, {})
    
    # Randomly select a currency if not a cafe
    if not company_type:
        currency_code = random.choice(list(CURRENCIES.keys()))
        currency_info = CURRENCIES[currency_code]
    else:
        currency_info = CURRENCIES[store_info["currency"]]
    
    # Check if it's a cafe location
    is_cafe = "COFFEE" in store_location or "CAFE" in store_location or "BERJAYA" in store_location
    
    if is_cafe:
        num_items = random.randint(1, 4)
        all_items = [(category, item, price_range) 
                    for category, items_dict in items.items() 
                    if category == "Cafe & Coffee"
                    for item, price_range in items_dict.items()]
    else:
        num_items = random.randint(20, 35)
        all_items = [(category, item, price_range) 
                    for category, items_dict in items.items() 
                    for item, price_range in items_dict.items()]
    
    # Generate receipt items
    selected_items = random.sample(all_items, min(num_items, len(all_items)))
    for category, item, (min_price, max_price) in selected_items:
        quantity = random.randint(1, 3 if is_cafe else 5)
        price = round(random.uniform(min_price, max_price), 2)
        item_total = round(quantity * price, 2)
        total += item_total
        
        receipt_items.append({
            "category": category,
            "name": item,
            "quantity": quantity,
            "price": format_currency(price, currency_info),
            "total": format_currency(item_total, currency_info)
        })
    
    # Sort items by category
    receipt_items.sort(key=lambda x: (x["category"], x["name"]))
    
    # Calculate various charges
    if is_cafe:
        tax_rate = store_info["tax_rate"]
        service_charge_rate = store_info["service_charge"]
        service_charge = round(total * service_charge_rate, 2)
        tax = round((total + service_charge) * tax_rate, 2)
    else:
        tax_rate = 0.06  # Default tax rate
        service_charge = 0
        tax = round(total * tax_rate, 2)
    
    final_total = total + service_charge + tax
    
    # Generate additional receipt details
    payment_method = random.choice(PAYMENT_METHODS)
    terminal_id = f"TERM{random.randint(100,999)}"
    merchant_id = f"MID{random.randint(10000,99999)}"
    batch_no = random.randint(1,999)
    trace_no = random.randint(100000,999999)
    
    return {
        "items": receipt_items,
        "subtotal": format_currency(total, currency_info),
        "service_charge": format_currency(service_charge, currency_info),
        "tax": format_currency(tax, currency_info),
        "total": format_currency(final_total, currency_info),
        "currency_info": currency_info,
        "payment_method": payment_method,
        "terminal_id": terminal_id,
        "merchant_id": merchant_id,
        "batch_no": batch_no,
        "trace_no": trace_no
    }

@app.route('/')
def index():
    # Generate receipt data
    receipt_data = generate_receipt()
    
    # Get company info if it's a cafe
    company_type = get_company_type(store_location)
    store_info = company_info.get(company_type, {})
    
    # Generate receipt identifiers
    timestamp = datetime.now()
    receipt_number = f"{timestamp.strftime('%Y%m%d')}-{random.randint(1000,9999)}"
    employee_id = f"EMP{random.randint(1000,9999)}"
    service_id = f"WID-{random.randint(1000,9999)}-{random.randint(10000000,99999999)}"
    
    # Generate shift information
    shift_id = f"SHIFT-{random.randint(1,3)}"
    pos_id = f"POS-{random.randint(1,99):02d}"
    
    # Unpack receipt_data to avoid the items() method conflict
    return render_template('receipt.html',
                         items=receipt_data["items"],
                         subtotal=receipt_data["subtotal"],
                         service_charge=receipt_data["service_charge"],
                         tax=receipt_data["tax"],
                         total=receipt_data["total"],
                         currency_info=receipt_data["currency_info"],
                         payment_method=receipt_data["payment_method"],
                         terminal_id=receipt_data["terminal_id"],
                         merchant_id=receipt_data["merchant_id"],
                         batch_no=receipt_data["batch_no"],
                         trace_no=receipt_data["trace_no"],
                         timestamp=timestamp.strftime("%m-%d-%Y %I:%M:%p"),
                         store_id=store_location,
                         service_id=service_id,
                         company_info=store_info,
                         receipt_number=receipt_number,
                         employee_id=employee_id,
                         shift_id=shift_id,
                         pos_id=pos_id)

if __name__ == '__main__':
    app.run(debug=True)
