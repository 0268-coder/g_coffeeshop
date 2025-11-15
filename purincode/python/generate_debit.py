#!/usr/bin/env python3
"""
Generate synthetic debit card transaction data from payment_transaction_extracted.csv

This script:
1. Reads payment transactions with payment_method_id = 3 (Debit Card)
2. Generates synthetic debit card details:
   - Last 4 digits (random)
   - First name (random Thai-sounding name)
   - Last name (random Thai-sounding name)
3. Outputs both CSV and SQL INSERT statements
"""

import csv
import random
import os

# ==============================================================
# CONFIGURATION
# ==============================================================
DEBIT_PAYMENT_METHOD_ID = 3

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to purincode directory
PURIN_CODE_DIR = os.path.dirname(SCRIPT_DIR)

INPUT_CSV = os.path.join(PURIN_CODE_DIR, "info", "payment_transaction_extracted.csv")
OUTPUT_CSV = os.path.join(PURIN_CODE_DIR, "info", "debit_synthetic.csv")
OUTPUT_SQL = os.path.join(PURIN_CODE_DIR, "insert sql", "debit_inserts.sql")

# Thai-sounding first names
THAI_FIRST_NAMES = [
  "Pawin",
  "Napat",
  "Nattapong",
  "Kittipong",
  "Anawin",
  "Korn",
  "Phurit",
  "Thanakorn",
  "Chanon",
  "Tanapat",
  "Tawan",
  "Phattharaphon",
  "Niran",
  "Sirichai",
  "Pimchanok",
  "Ornapa",
  "Kanokwan",
  "Ploypailin",
  "Narumon",
  "Suchada",
  "Thanyarat",
  "Kamonchanok",
  "Pimnipa",
  "Ratchada",
  "Sasithorn",
  "Napatsorn",
  "Warit",
  "Teerapat",
  "Natthawat",
  "Supachai",
  "Phumiphat",
  "Weerayut",
  "Chanikan",
  "Pitchaya",
  "Natnicha",
  "Chayaporn",
  "Supaporn",
  "Phakjira",
  "Thanaporn",
  "Jirawat"
]


# Thai-sounding last names
THAI_LAST_NAMES = [
  "Suwannarat",
  "Kanjanakumnerd",
  "Chaiyapat",
  "Pinyosophon",
  "Rattanapong",
  "Worachot",
  "Phumpradit",
  "Thammarat",
  "Siriphan",
  "Nanthasiri",
  "Boonme",
  "Sangthong",
  "Chansawang",
  "Rattanachai",
  "Thongchai",
  "Phromphithak",
  "Somwang",
  "Phiphatphong",
  "Suksan",
  "Charoensuk",
  "Benjamas",
  "Phanthong",
  "Yingsiri",
  "Supawong",
  "Chantarangsi",
  "Rungroj",
  "Kittisak",
  "Phonphinit",
  "Intarachai",
  "Wongthong",
  "Bunyarat",
  "Kosolkitiwong",
  "Jariyawat",
  "Phansiri",
  "Sirilak",
  "Chamnan",
  "Boonlert",
  "Phuttharak",
  "Jirasuk"
]


# ==============================================================
# HELPER FUNCTIONS
# ==============================================================
def generate_last_4_digits():
    """Generate random 4-digit card number"""
    return str(random.randint(1000, 9999))


def generate_name():
    """Generate random Thai-sounding first and last name"""
    fname = random.choice(THAI_FIRST_NAMES)
    lname = random.choice(THAI_LAST_NAMES)
    return fname, lname


# ==============================================================
# STEP 1: Load payment_transaction_extracted.csv
# ==============================================================
print("=" * 60)
print("DEBIT CARD DATA GENERATION")
print("=" * 60)

debit_source = []

with open(INPUT_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if int(row['payment_method_id']) == DEBIT_PAYMENT_METHOD_ID:
            debit_source.append(row['payment_created_at'])

if len(debit_source) == 0:
    raise ValueError(f"No transactions found with payment_method_id = {DEBIT_PAYMENT_METHOD_ID}")

NUM_ROWS = len(debit_source)
print(f"\n✓ Loaded {NUM_ROWS} transactions from '{INPUT_CSV}'")
print(f"  Payment Method ID: {DEBIT_PAYMENT_METHOD_ID}")

# ==============================================================
# STEP 2: Generate synthetic debit card data
# ==============================================================
print("\nGenerating synthetic debit card records...")

rows = []
debit_id = 1

for _ in debit_source:
    # Generate random 4-digit card number
    last4digit = generate_last_4_digits()
    
    # Generate random Thai-sounding name
    fname, lname = generate_name()

    rows.append({
        'payment_method_id': DEBIT_PAYMENT_METHOD_ID,
        'debit_id': debit_id,
        'last4digit': last4digit,
        'fname': fname,
        'lname': lname
    })
    debit_id += 1

# ==============================================================
# STEP 3: Save to CSV
# ==============================================================
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['payment_method_id', 'debit_id', 'last4digit', 'fname', 'lname'])
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Saved to '{OUTPUT_CSV}'")

# ==============================================================
# STEP 4: Generate SQL INSERT statements
# ==============================================================
with open(OUTPUT_SQL, "w", encoding="utf-8") as file:
    file.write("INSERT INTO `debit` (`payment_method_id`, `debit_id`, `last4digit`, `fname`, `lname`) VALUES\n")
    
    for idx, row in enumerate(rows):
        pm_id = row['payment_method_id']
        did = row['debit_id']
        last4 = row['last4digit']
        fname = row['fname']
        lname = row['lname']
        
        values = f"({pm_id}, {did}, '{last4}', '{fname}', '{lname}')"
        
        if idx < len(rows) - 1:
            file.write(values + ",\n")
        else:
            file.write(values + ";\n")

print(f"✓ Saved to '{OUTPUT_SQL}'")

# ==============================================================
# STEP 5: Display Summary
# ==============================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total debit card records generated: {len(rows):,}")
print(f"Payment Method ID: {DEBIT_PAYMENT_METHOD_ID}")
print(f"Card Last 4 Digits: Random (1000-9999)")
print(f"Cardholder Names: Random Thai-sounding names")

print("\nFirst 10 records:")
print("-" * 60)
for i, row in enumerate(rows[:10], 1):
    print(f"{i:2}. ID:{row['debit_id']:5} | Last4: {row['last4digit']} | {row['fname']:15} {row['lname']:15}")

print("\n" + "=" * 60)
print("✓ Generation complete!")
print("=" * 60)
