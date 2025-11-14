#!/usr/bin/env python3
"""
Generate synthetic gift card transaction data from payment_transaction_extracted.csv

This script:
1. Reads payment transactions with payment_method_id = 1 (gift card)
2. Generates synthetic gift card data with random codes and balances
3. Outputs both CSV and SQL INSERT statements
"""

import csv
import random
import string
import os
from datetime import datetime, timedelta

# ==============================================================
# CONFIGURATION
# ==============================================================
GIFTCARD_PAYMENT_METHOD_ID = 1

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to purincode directory
PURIN_CODE_DIR = os.path.dirname(SCRIPT_DIR)

INPUT_CSV = os.path.join(PURIN_CODE_DIR, "info", "payment_transaction_extracted.csv")
OUTPUT_CSV = os.path.join(PURIN_CODE_DIR, "info", "giftcard_synthetic.csv")
OUTPUT_SQL = os.path.join(PURIN_CODE_DIR, "insert sql", "giftcard_inserts.sql")

# Gift card titles
GIFTCARD_TITLES = [
    "Coffee Lovers",
    "Premium Blend",
    "Daily Rewards",
    "Special Gift",
    "Barista's Choice",
    "Espresso Club",
    "Morning Brew",
    "Weekend Special",
    "VIP Member",
    "Gold Card"
]

# ==============================================================
# HELPER FUNCTIONS
# ==============================================================
def generate_giftcard_code(length=20):
    """Generate a random gift card code"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_dates(base_date_str):
    """
    Generate issued_date and expiry_date with randomization
    
    Args:
        base_date_str: Base date string from payment_created_at
    
    Returns:
        Tuple of (issued_date, expiry_date) as YYYY-MM-DD strings
    """
    # Parse the base date
    base_date = datetime.strptime(base_date_str.split(' ')[0], '%Y-%m-%d')
    
    # Issued date can be anywhere from 2 years before to the base date
    days_before = random.randint(1, 730)  # 0 to 2 years before
    issued_date = (base_date - timedelta(days=days_before)).strftime('%Y-%m-%d')
    
    # Expiry date is random: 6 months to 3 years after issued date
    issued_datetime = datetime.strptime(issued_date, '%Y-%m-%d')
    expiry_days = random.randint(180, 1095)  # 6 months to 3 years
    expiry_date = (issued_datetime + timedelta(days=expiry_days)).strftime('%Y-%m-%d')
    
    return issued_date, expiry_date


# ==============================================================
# STEP 1: Load payment_transaction_extracted.csv
# ==============================================================
print("=" * 60)
print("GIFT CARD DATA GENERATION")
print("=" * 60)

giftcard_source = []

with open(INPUT_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if int(row['payment_method_id']) == GIFTCARD_PAYMENT_METHOD_ID:
            giftcard_source.append({
                'payment_final_amount': float(row['payment_final_amount']),
                'payment_created_at': row['payment_created_at']
            })

if len(giftcard_source) == 0:
    raise ValueError(f"No transactions found with payment_method_id = {GIFTCARD_PAYMENT_METHOD_ID}")

NUM_ROWS = len(giftcard_source)
print(f"\n✓ Loaded {NUM_ROWS} transactions from '{INPUT_CSV}'")
print(f"  Payment Method ID: {GIFTCARD_PAYMENT_METHOD_ID}")

# ==============================================================
# STEP 2: Generate synthetic gift card data
# ==============================================================
print("\nGenerating synthetic gift card records...")

rows = []
giftcard_id = 1

for transaction in giftcard_source:
    # Gift card initial value is the payment amount, rounded to nearest 100
    initial_value = round(transaction['payment_final_amount'] / 100) * 100
    
    # Generate code and dates first
    code = generate_giftcard_code(20)
    issued_date, expiry_date = generate_dates(transaction['payment_created_at'])
    
    # Check if expired (today is after expiry date)
    today = datetime.now().date()
    expiry_datetime = datetime.strptime(expiry_date, '%Y-%m-%d').date()
    is_expired = today > expiry_datetime
    
    # Determine status based on expiry and usage
    # 40% chance fully used, 20% unused, 40% partially used
    rand = random.random()
    
    if is_expired:
        status = "Expired"
        # Expired cards can have any balance, but are no longer usable
        if rand < 0.5:
            current_balance = 0.00  # Fully used before expiry
        else:
            current_balance = round(initial_value * random.uniform(0.1, 0.9), 2)  # Partially used
    else:
        # Not expired, determine by usage
        if rand < 0.4:
            current_balance = 0.00
            status = "Used"
        elif rand < 0.6:
            current_balance = initial_value
            status = "Active"
        else:
            current_balance = round(initial_value * random.uniform(0.1, 0.9), 2)
            status = "Active"
    
    # Random title
    title = random.choice(GIFTCARD_TITLES)
    
    # Purchased by member: 70% have a member ID, 30% NULL (gift from non-member)
    purchased_by_member_id = random.randint(1, 50000) if random.random() < 0.7 else None
    
    # Last used date (only if status is Used or if partially used)
    if status == "Used" or (status == "Active" and current_balance < initial_value):
        # Last used sometime after issued date
        issued_datetime = datetime.strptime(issued_date, '%Y-%m-%d')
        days_since_issued = random.randint(1, 180)
        last_used_date = (issued_datetime + timedelta(days=days_since_issued)).strftime('%Y-%m-%d')
    else:
        last_used_date = None

    rows.append({
        'payment_method_id': GIFTCARD_PAYMENT_METHOD_ID,
        'giftcard_id': giftcard_id,
        'initial_value': round(initial_value, 2),
        'current_balance': current_balance,
        'title': title,
        'issued_date': issued_date,
        'expiry_date': expiry_date,
        'status': status,
        'code': code,
        'purchased_by_member_id': purchased_by_member_id,
        'last_used_date': last_used_date
    })
    giftcard_id += 1

# ==============================================================
# STEP 3: Save to CSV
# ==============================================================
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['payment_method_id', 'giftcard_id', 'initial_value', 'current_balance', 'title', 'issued_date', 'expiry_date', 'status', 'code', 'purchased_by_member_id', 'last_used_date'])
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Saved to '{OUTPUT_CSV}'")

# ==============================================================
# STEP 4: Generate SQL INSERT statements
# ==============================================================
with open(OUTPUT_SQL, "w", encoding="utf-8") as file:
    file.write("INSERT INTO `gift_card` (`payment_method_id`, `giftcard_id`, `initial_value`, `current_balance`, `title`, `issued_date`, `expiry_date`, `status`, `code`, `purchased_by_member_id`, `last_used_date`) VALUES\n")
    
    for idx, row in enumerate(rows):
        pm_id = row['payment_method_id']
        gc_id = row['giftcard_id']
        init_val = row['initial_value']
        curr_bal = row['current_balance']
        title = row['title'].replace("'", "\\'")
        issued = row['issued_date']
        expiry = row['expiry_date']
        status = row['status']
        code = row['code']
        member_id = row['purchased_by_member_id']
        last_used = row['last_used_date']
        
        # Handle NULL values
        member_id_str = f"{member_id}" if member_id is not None else "NULL"
        last_used_str = f"'{last_used}'" if last_used is not None else "NULL"
        
        values = f"({pm_id}, {gc_id}, {init_val}, {curr_bal}, '{title}', '{issued}', '{expiry}', '{status}', '{code}', {member_id_str}, {last_used_str})"
        
        if idx < len(rows) - 1:
            file.write(values + ",\n")
        else:
            file.write(values + ";\n")

print(f"✓ Saved to '{OUTPUT_SQL}'")

# ==============================================================
# STEP 5: Display Summary
# ==============================================================
status_counts = {}
total_initial = 0
total_balance = 0

for row in rows:
    status = row['status']
    status_counts[status] = status_counts.get(status, 0) + 1
    total_initial += row['initial_value']
    total_balance += row['current_balance']

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total gift card records generated: {len(rows):,}")
print(f"Payment Method ID: {GIFTCARD_PAYMENT_METHOD_ID}")
print(f"Total initial value: ฿{total_initial:,.2f}")
print(f"Total current balance: ฿{total_balance:,.2f}")
print(f"Average initial value per card: ฿{total_initial/len(rows):,.2f}")
print(f"Average current balance per card: ฿{total_balance/len(rows):,.2f}")

print(f"\nStatus Distribution:")
print("-" * 60)
for status in ["Active", "Used", "Expired"]:
    if status in status_counts:
        count = status_counts[status]
        percentage = (count / len(rows)) * 100
        print(f"  {status:10} | {count:5,} cards ({percentage:5.2f}%)")

print("\nFirst 10 records:")
print("-" * 60)
for i, row in enumerate(rows[:10], 1):
    print(f"{i:2}. ID:{row['giftcard_id']:5} | Balance: ฿{row['current_balance']:8.2f} | Status: {row['status']:8} | Code: {row['code'][:15]}...")

print("\n" + "=" * 60)
print("✓ Generation complete!")
print("=" * 60)
