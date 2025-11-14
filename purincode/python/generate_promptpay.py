#!/usr/bin/env python3
"""
Generate synthetic PromptPay transaction data from payment_transaction_extracted.csv

This script:
1. Reads payment transactions with payment_method_id = 5 (PromptPay)
2. Generates synthetic transaction references (random 60-character strings)
3. Assigns random Thai bank names
4. Outputs both CSV and SQL INSERT statements
"""

import csv
import random
import string
import os

# ==============================================================
# CONFIGURATION
# ==============================================================
PROMPTPAY_PAYMENT_METHOD_ID = 5

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to purincode directory
PURIN_CODE_DIR = os.path.dirname(SCRIPT_DIR)

INPUT_CSV = os.path.join(PURIN_CODE_DIR, "info", "payment_transaction_extracted.csv")
OUTPUT_CSV = os.path.join(PURIN_CODE_DIR, "info", "promptpay_synthetic.csv")
OUTPUT_SQL = os.path.join(PURIN_CODE_DIR, "insert sql", "promptpay_inserts.sql")

# List of major Thai banks
THAI_BANKS = [
    "Bangkok Bank",
    "Kasikornbank",
    "Krungthai Bank",
    "Siam Commercial Bank",
    "Krungsri",
    "TTB Bank"
]

# ==============================================================
# HELPER FUNCTIONS
# ==============================================================
def generate_transaction_ref(date_str, length=17):
    """
    Generate a transaction reference with format: yyyymmdd + 17 random alphanumeric characters
    
    Args:
        date_str: Date string in format 'YYYY-MM-DD HH:MM:SS'
        length: Number of random characters to append (default: 17)
    
    Returns:
        Transaction reference string (e.g., '20250601aB2cD3eF4gH5i')
    """
    # Extract date part (YYYY-MM-DD) and remove hyphens
    date_part = date_str.split(' ')[0].replace('-', '')
    
    # Generate random alphanumeric characters (both upper and lower case)
    characters = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(characters) for _ in range(length))
    
    return date_part + random_part


# ==============================================================
# STEP 1: Load payment_transaction_extracted.csv
# ==============================================================
print("=" * 60)
print("PROMPTPAY DATA GENERATION")
print("=" * 60)

promptpay_source = []

with open(INPUT_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if int(row['payment_method_id']) == PROMPTPAY_PAYMENT_METHOD_ID:
            promptpay_source.append({
                'payment_final_amount': float(row['payment_final_amount']),
                'payment_created_at': row['payment_created_at']
            })

if len(promptpay_source) == 0:
    raise ValueError(f"No transactions found with payment_method_id = {PROMPTPAY_PAYMENT_METHOD_ID}")

NUM_ROWS = len(promptpay_source)
print(f"\n✓ Loaded {NUM_ROWS} transactions from '{INPUT_CSV}'")
print(f"  Payment Method ID: {PROMPTPAY_PAYMENT_METHOD_ID}")
print(f"  Transaction Reference Format: YYYYMMDD + 17 random characters")

# ==============================================================
# STEP 2: Generate synthetic PromptPay data
# ==============================================================
print("\nGenerating synthetic PromptPay records...")

rows = []
promptpay_id = 1

for transaction in promptpay_source:
    # Generate transaction reference with date from payment_created_at
    transaction_ref = generate_transaction_ref(transaction['payment_created_at'])
    
    # Assign random Thai bank
    bank_name = random.choice(THAI_BANKS)

    rows.append({
        'payment_method_id': PROMPTPAY_PAYMENT_METHOD_ID,
        'promptpay_id': promptpay_id,
        'transaction_ref': transaction_ref,
        'bank_name': bank_name
    })
    promptpay_id += 1

# ==============================================================
# STEP 3: Save to CSV
# ==============================================================
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['payment_method_id', 'promptpay_id', 'transaction_ref', 'bank_name'])
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Saved to '{OUTPUT_CSV}'")

# ==============================================================
# STEP 4: Generate SQL INSERT statements
# ==============================================================
with open(OUTPUT_SQL, "w", encoding="utf-8") as file:
    file.write("INSERT INTO `promptpay` (`payment_method_id`, `promptpay_id`, `transaction_ref`, `bank_name`) VALUES\n")
    
    for idx, row in enumerate(rows):
        pm_id = row['payment_method_id']
        pid = row['promptpay_id']
        trans_ref = row['transaction_ref']
        bank = row['bank_name']
        
        # Escape quotes in bank name
        bank_escaped = bank.replace("'", "\\'")
        
        values = f"({pm_id}, {pid}, '{trans_ref}', '{bank_escaped}')"
        
        if idx < len(rows) - 1:
            file.write(values + ",\n")
        else:
            file.write(values + ";\n")

print(f"✓ Saved to '{OUTPUT_SQL}'")

# ==============================================================
# STEP 5: Display Summary
# ==============================================================
# Count bank usage
bank_counts = {}
for row in rows:
    bank = row['bank_name']
    bank_counts[bank] = bank_counts.get(bank, 0) + 1

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total PromptPay records generated: {len(rows):,}")
print(f"Payment Method ID: {PROMPTPAY_PAYMENT_METHOD_ID}")
print(f"Transaction Reference Format: YYYYMMDD + 17 random alphanumeric characters (total 25 chars)")
print(f"\nBank Distribution:")
print("-" * 60)

# Sort banks by count (descending)
sorted_banks = sorted(bank_counts.items(), key=lambda x: x[1], reverse=True)
for bank, count in sorted_banks:
    percentage = (count / len(rows)) * 100
    print(f"  {bank:30} | {count:5,} transactions ({percentage:5.2f}%)")

print("\nFirst 10 records:")
print("-" * 60)
for i, row in enumerate(rows[:10], 1):
    print(f"{i:2}. ID:{row['promptpay_id']:5} | Bank: {row['bank_name']:20} | Ref: {row['transaction_ref'][:20]}...")

print("\n" + "=" * 60)
print("✓ Generation complete!")
print("=" * 60)
