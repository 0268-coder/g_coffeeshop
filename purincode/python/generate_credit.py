#!/usr/bin/env python3
"""
Generate synthetic credit card transaction data from payment_transaction_extracted.csv

This script:
1. Reads payment transactions with payment_method_id = 2 (Credit Card)
2. Generates synthetic credit card details:
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
CREDIT_PAYMENT_METHOD_ID = 2

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to purincode directory
PURIN_CODE_DIR = os.path.dirname(SCRIPT_DIR)

INPUT_CSV = os.path.join(PURIN_CODE_DIR, "info", "payment_transaction_extracted.csv")
OUTPUT_CSV = os.path.join(PURIN_CODE_DIR, "info", "credit_synthetic.csv")
OUTPUT_SQL = os.path.join(PURIN_CODE_DIR, "insert sql", "credit_inserts.sql")

# Thai-sounding first names
THAI_FIRST_NAMES = [
     "ปวิน",
    "นภัทร",
    "ณัฐพงศ์",
    "กิตติพงษ์",
    "อนาวิน",
    "กร",
    "ภูริทัต",
    "ธนากร",
    "ชานน",
    "ธนภัทร",
    "ตะวัน",
    "ภัทรพล",
    "นีรนารา",
    "ศิริชัย",
    "พิมพ์ชนก",
    "อรพา",
    "กนกวรรณ",
    "พลอยไพลิน",
    "นฤมล",
    "สุชาดา",
    "ธัญรัตน์",
    "กมลชนก",
    "พิมพ์นิภา",
    "รัชฎา",
    "ศศิธร",
    "นภัสสร",
    "วริศ",
    "จิรายุ",
    "สรสิทธิ์",
    "พงษ์เทพ",
    "บดินทร์",
    "ณัฐพล",
    "พงศกร",
    "ธีรภัทร",
    "จิรภัทร",
    "วรวัฒน์",
    "ปกรณ์",
    "อัครกฤษ",
    "กัญญารัตน์",
    "พัชราพร",
    "เบญจมาศ",
    "สุภาภรณ์",
    "กัญญาภัค",
    "วรกมล",
    "ประภาพร",
    "สุพรรณิดา",
    "ชนิกา",
    "วิภาภรณ์"
]

# Thai-sounding last names
THAI_LAST_NAMES = [
 "สวัสดิ์รักษา",
    "จันทร์โสภา",
    "ทองมาก",
    "บุญช่วย",
    "ศรีสวัสดิ์",
    "สุขสันต์",
    "ใจดี",
    "วัฒนกูล",
    "ตั้งตรงจิตร",
    "วงศ์วัฒนา",
    "อินทรศิลป์",
    "พัฒนพงศ์",
    "มณีวรรณ",
    "คชเสนี",
    "โชคดี",
    "ปัญญาเร็ว",
    "สมหมาย",
    "ศรีสุวรรณ",
    "ทองคำ",
    "บุญศรี",
    "สุทธิเวช",
    "เทียนทอง",
    "มนตรี",
    "บุญญาภิรมย์",
    "เกียรติสุวรรณ",
    "พงษ์พิทักษ์",
    "ศรีเจริญ",
    "สุขเกษม",
    "เรืองฤทธิ์",
    "คงคา",
    "วรประเสริฐ",
    "รุ่งเรืองกิจ",
    "ไพศาล",
    "ชนะชัย",
    "อินทร์สวัสดิ์",
    "แซ่ตัน",
    "แซ่ลิ้ม",
    "แซ่โง้ว",
    "แซ่ตั้ง",
    "เกษมศานต์",
    "จิตติวัฒน์",
    "สุริยวงศ์",
    "ศักดิกุล",
    "จารุวัฒน์",
    "พูนทรัพย์",
    "อุดมเดช",
    "ชำนาญกิจ",
    "บุญยงค์",
    "ไชยยศ"
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
print("CREDIT CARD DATA GENERATION")
print("=" * 60)

credit_source = []

with open(INPUT_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if int(row['payment_method_id']) == CREDIT_PAYMENT_METHOD_ID:
            credit_source.append(row['payment_created_at'])

if len(credit_source) == 0:
    raise ValueError(f"No transactions found with payment_method_id = {CREDIT_PAYMENT_METHOD_ID}")

NUM_ROWS = len(credit_source)
print(f"\n✓ Loaded {NUM_ROWS} transactions from '{INPUT_CSV}'")
print(f"  Payment Method ID: {CREDIT_PAYMENT_METHOD_ID}")

# ==============================================================
# STEP 2: Generate synthetic credit card data
# ==============================================================
print("\nGenerating synthetic credit card records...")

rows = []
credit_id = 1

for _ in credit_source:
    # Generate random 4-digit card number
    last4digit = generate_last_4_digits()
    
    # Generate random Thai-sounding name
    fname, lname = generate_name()

    rows.append({
        'payment_method_id': CREDIT_PAYMENT_METHOD_ID,
        'credit_id': credit_id,
        'last4digit': last4digit,
        'fname': fname,
        'lname': lname
    })
    credit_id += 1

# ==============================================================
# STEP 3: Save to CSV
# ==============================================================
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=['payment_method_id', 'credit_id', 'last4digit', 'fname', 'lname'])
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Saved to '{OUTPUT_CSV}'")

# ==============================================================
# STEP 4: Generate SQL INSERT statements
# ==============================================================
with open(OUTPUT_SQL, "w", encoding="utf-8") as file:
    file.write("INSERT INTO `credit` (`payment_method_id`, `credit_id`, `last4digit`, `fname`, `lname`) VALUES\n")
    
    for idx, row in enumerate(rows):
        pm_id = row['payment_method_id']
        cid = row['credit_id']
        last4 = row['last4digit']
        fname = row['fname']
        lname = row['lname']
        
        values = f"({pm_id}, {cid}, '{last4}', '{fname}', '{lname}')"
        
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
print(f"Total credit card records generated: {len(rows):,}")
print(f"Payment Method ID: {CREDIT_PAYMENT_METHOD_ID}")
print(f"Card Last 4 Digits: Random (1000-9999)")
print(f"Cardholder Names: Random Thai-sounding names")

print("\nFirst 10 records:")
print("-" * 60)
for i, row in enumerate(rows[:10], 1):
    print(f"{i:2}. ID:{row['credit_id']:5} | Last4: {row['last4digit']} | {row['fname']:15} {row['lname']:15}")

print("\n" + "=" * 60)
print("✓ Generation complete!")
print("=" * 60)
