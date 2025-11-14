#!/usr/bin/env python3
"""
Generate synthetic cash transaction data from payment_transaction_extracted.csv

This script:
1. Reads payment transactions with payment_method_id = 4 (cash)
2. Generates synthetic cash_received amounts (customer pays with cash, may overpay)
3. Calculates cash_change based on the difference
4. Outputs both CSV and SQL INSERT statements
"""

import csv
import random

# ==============================================================
# CONFIGURATION
# ==============================================================
import os
import sys

CASH_PAYMENT_METHOD_ID = 4

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to purincode directory
PURIN_CODE_DIR = os.path.dirname(SCRIPT_DIR)

INPUT_CSV = os.path.join(PURIN_CODE_DIR, "info", "payment_transaction_extracted.csv")
OUTPUT_CSV = os.path.join(PURIN_CODE_DIR, "info", "cash_synthetic.csv")
OUTPUT_SQL = os.path.join(PURIN_CODE_DIR, "insert sql", "cash_inserts.sql")

# Change options (in THB) that customers might pay with
CHANGE_OPTIONS = [0, 1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# ==============================================================
# STEP 1: Load payment_transaction_extracted.csv
# ==============================================================
print("=" * 60)
print("CASH DATA GENERATION")
print("=" * 60)

cash_source = []

with open(INPUT_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if int(row['payment_method_id']) == CASH_PAYMENT_METHOD_ID:
            cash_source.append(float(row['payment_final_amount']))

if len(cash_source) == 0:
    raise ValueError(f"No transactions found with payment_method_id = {CASH_PAYMENT_METHOD_ID}")

NUM_ROWS = len(cash_source)
print(f"\n✓ Loaded {NUM_ROWS} transactions from '{INPUT_CSV}'")
print(f"  Payment Method ID: {CASH_PAYMENT_METHOD_ID}")

# ==============================================================
# STEP 2: Generate synthetic cash data
# ==============================================================
print("\nGenerating synthetic cash records...")

rows = []
cash_id = 1

for final_amount in cash_source:
    # Simulate customer paying cash:
    # Customer pays with bills, so may pay more than the exact amount
    extra_paid = random.choice(CHANGE_OPTIONS)
    cash_received = final_amount + extra_paid
    cash_change = cash_received - final_amount

    rows.append({
        'payment_method_id': CASH_PAYMENT_METHOD_ID,
        'cash_id': cash_id,
        'cash_received': round(cash_received, 2),
        'cash_change': round(cash_change, 2)
    })
    cash_id += 1

# ==============================================================
# STEP 3: Save to CSV
# ==============================================================
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['payment_method_id', 'cash_id', 'cash_received', 'cash_change'])
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Saved to '{OUTPUT_CSV}'")

# ==============================================================
# STEP 4: Generate SQL INSERT statements
# ==============================================================
with open(OUTPUT_SQL, "w", encoding="utf-8") as file:
    file.write("INSERT INTO `cash` (`payment_method_id`, `cash_id`, `cash_received`, `cash_change`) VALUES\n")
    
    for idx, row in enumerate(rows):
        pm_id = row['payment_method_id']
        cid = row['cash_id']
        received = row['cash_received']
        change = row['cash_change']
        
        values = f"({pm_id}, {cid}, {received}, {change})"
        
        if idx < len(rows) - 1:
            file.write(values + ",\n")
        else:
            file.write(values + ";\n")

print(f"✓ Saved to '{OUTPUT_SQL}'")

# ==============================================================
# STEP 5: Display Summary
# ==============================================================
total_received = sum(row['cash_received'] for row in rows)
total_change = sum(row['cash_change'] for row in rows)

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total cash records generated: {len(rows):,}")
print(f"Total cash received: ฿{total_received:,.2f}")
print(f"Total cash change given: ฿{total_change:,.2f}")
print(f"Average cash received per transaction: ฿{total_received/len(rows):,.2f}")
print(f"Average cash change per transaction: ฿{total_change/len(rows):,.2f}")

print("\nFirst 10 records:")
print("-" * 60)
for i, row in enumerate(rows[:10], 1):
    print(f"{i:2}. ID:{row['cash_id']:5} | Received: ฿{row['cash_received']:8.2f} | Change: ฿{row['cash_change']:6.2f}")

print("\n" + "=" * 60)
print("✓ Generation complete!")
print("=" * 60)
