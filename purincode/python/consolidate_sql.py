#!/usr/bin/env python3
"""
Consolidate all SQL INSERT files into a single master SQL file

This script:
1. Reads all .sql files from the 'insert sql' directory
2. Combines them in a logical order (payment methods 1-5)
3. Creates a single consolidated SQL file with all INSERT statements
"""

import os
import glob
from datetime import datetime

# ==============================================================
# CONFIGURATION
# ==============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PURIN_CODE_DIR = os.path.dirname(SCRIPT_DIR)
MAIN_DIR = os.path.dirname(PURIN_CODE_DIR)

INSERT_SQL_DIR = os.path.join(MAIN_DIR, "insert_statements")
OUTPUT_FILE = os.path.join(INSERT_SQL_DIR, "purin_consolidated_inserts.sql")

# Order of payment methods for logical organization
PAYMENT_METHODS = [
    ("giftcard_inserts.sql", "1", "Gift Card"),
    ("credit_inserts.sql", "2", "Credit Card"),
    ("debit_inserts.sql", "3", "Debit Card"),
    ("cash_inserts.sql", "4", "Cash"),
    ("promptpay_inserts.sql", "5", "PromptPay"),
]

# ==============================================================
# MAIN EXECUTION
# ==============================================================
print("=" * 70)
print("SQL FILE CONSOLIDATION")
print("=" * 70)

print(f"\nSource Directory: {INSERT_SQL_DIR}")
print(f"Output File: {OUTPUT_FILE}\n")

consolidated_content = []
total_inserts = 0
file_count = 0

print("Processing SQL files:")
print("-" * 70)

for filename, method_id, description in PAYMENT_METHODS:
    filepath = os.path.join(INSERT_SQL_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"[SKIP] {description:<20} - File not found: {filename}")
        continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count INSERT statements
        insert_count = content.count("INSERT INTO")
        total_inserts += insert_count
        file_count += 1
        
        consolidated_content.append(content)
        
        # Add separator between sections (except for last section)
        if filename != PAYMENT_METHODS[-1][0]:
            consolidated_content.append("\n")
        
        print(f"[OK] {description:<20} | {insert_count:>6,} inserts | {filename}")
    
    except Exception as e:
        print(f"[ERROR] {description:<20} - {str(e)}")

print("-" * 70)

# Write consolidated file
try:
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.writelines(consolidated_content)
    
    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    
    print(f"\n[OK] Successfully consolidated {file_count} SQL files")
    print(f"\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Output File: {OUTPUT_FILE}")
    print(f"File Size: {file_size_mb:.2f} MB")
    print(f"Total INSERT Statements: {total_inserts:,}")
    print(f"Files Consolidated: {file_count}")
    print("=" * 70)
    print("\n[OK] Consolidation complete!")

except Exception as e:
    print(f"\n[ERROR] Failed to write consolidated file: {str(e)}")
