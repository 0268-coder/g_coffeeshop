#!/usr/bin/env python3
"""
Master script to run all synthetic data generation scripts

This script executes all payment method data generators in sequence:
1. generate_cash.py (payment_method_id = 4)
2. generate_promptpay.py (payment_method_id = 5)
3. generate_credit.py (payment_method_id = 2)
4. generate_debit.py (payment_method_id = 3)
5. generate_giftcard.py (payment_method_id = 1)
"""

import subprocess
import sys
import os
from datetime import datetime
import csv
import io

# Set UTF-8 encoding for stdout
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==============================================================
# CONFIGURATION
# ==============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = [
    ("generate_cash.py", "Cash Transactions"),
    ("generate_promptpay.py", "PromptPay Transactions"),
    ("generate_credit.py", "Credit Card Transactions"),
    ("generate_debit.py", "Debit Card Transactions"),
    ("generate_giftcard.py", "Gift Card Transactions"),
]

# ==============================================================
# HELPER FUNCTIONS
# ==============================================================
def count_csv_rows(filepath):
    """Count the number of rows in a CSV file (excluding header)"""
    if not os.path.exists(filepath):
        return 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return sum(1 for _ in reader)
    except:
        return 0


# ==============================================================
# MAIN EXECUTION
# ==============================================================
def main():
    print("=" * 70)
    print("SYNTHETIC DATA GENERATION - MASTER SCRIPT")
    print("=" * 70)
    print(f"\nStart Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Script Directory: {SCRIPT_DIR}\n")
    
    results = []
    failed_scripts = []
    
    for script_name, description in SCRIPTS:
        script_path = os.path.join(SCRIPT_DIR, script_name)
        
        # Check if script exists
        if not os.path.exists(script_path):
            print(f"\n[SKIP] {script_name} - File not found")
            results.append((script_name, "SKIPPED", "File not found"))
            continue
        
        print(f"\n{'=' * 70}")
        print(f"Running: {description}")
        print(f"Script: {script_name}")
        print(f"{'=' * 70}")
        
        try:
            # Run the script
            result = subprocess.run(
                [sys.executable, script_path],
                cwd=SCRIPT_DIR,
                capture_output=False,
                timeout=300  # 5 minute timeout per script
            )
            
            if result.returncode == 0:
                print(f"\n[OK] SUCCESS: {script_name}")
                results.append((script_name, "SUCCESS", ""))
            else:
                print(f"\n[FAIL] FAILED: {script_name} (Exit code: {result.returncode})")
                results.append((script_name, "FAILED", f"Exit code: {result.returncode}"))
                failed_scripts.append(script_name)
        
        except subprocess.TimeoutExpired:
            print(f"\n[TIMEOUT] {script_name} (exceeded 5 minutes)")
            results.append((script_name, "TIMEOUT", "Exceeded 5 minutes"))
            failed_scripts.append(script_name)
        
        except Exception as e:
            print(f"\n[ERROR] {script_name} - {str(e)}")
            results.append((script_name, "ERROR", str(e)))
            failed_scripts.append(script_name)
    
    # ==============================================================
    # SUMMARY
    # ==============================================================
    print("\n" + "=" * 70)
    print("EXECUTION SUMMARY")
    print("=" * 70)
    
    print(f"\nTotal Scripts: {len(SCRIPTS)}")
    print(f"Completed: {len([r for r in results if r[1] == 'SUCCESS'])}")
    print(f"Skipped: {len([r for r in results if r[1] == 'SKIPPED'])}")
    print(f"Failed: {len([r for r in results if r[1] in ['FAILED', 'ERROR', 'TIMEOUT']])}")
    
    print("\n" + "-" * 70)
    print(f"{'Script':<30} {'Status':<15} {'Details':<25}")
    print("-" * 70)
    
    for script_name, status, details in results:
        status_symbol = "✓" if status == "SUCCESS" else "⚠" if status == "SKIPPED" else "✗"
        print(f"{status_symbol} {script_name:<28} {status:<15} {details:<25}")
    
    print("-" * 70)
    
    # ==============================================================
    # OUTPUT PATHS AND ROW COUNTS
    # ==============================================================
    print("\n" + "=" * 70)
    print("GENERATED DATA FILES")
    print("=" * 70)
    
    purin_code_dir = os.path.dirname(SCRIPT_DIR)
    info_dir = os.path.join(purin_code_dir, "info")
    insert_sql_dir = os.path.join(purin_code_dir, "insert sql")
    
    data_files = [
        ("Cash", "cash_synthetic.csv", "cash_inserts.sql"),
        ("PromptPay", "promptpay_synthetic.csv", "promptpay_inserts.sql"),
        ("Credit Card", "credit_synthetic.csv", "credit_inserts.sql"),
        ("Debit Card", "debit_synthetic.csv", "debit_inserts.sql"),
        ("Gift Card", "giftcard_synthetic.csv", "giftcard_inserts.sql"),
    ]
    
    total_rows = 0
    
    print(f"\nCSV Files: {info_dir}")
    print("-" * 70)
    for name, csv_file, _ in data_files:
        csv_path = os.path.join(info_dir, csv_file)
        row_count = count_csv_rows(csv_path)
        total_rows += row_count
        status = "[OK]" if os.path.exists(csv_path) else "[MISSING]"
        print(f"{status} {name:<20} | {row_count:>6,} rows | {csv_path}")
    
    print(f"\nSQL Files: {insert_sql_dir}")
    print("-" * 70)
    for name, _, sql_file in data_files:
        sql_path = os.path.join(insert_sql_dir, sql_file)
        status = "[OK]" if os.path.exists(sql_path) else "[MISSING]"
        file_size = os.path.getsize(sql_path) if os.path.exists(sql_path) else 0
        size_mb = file_size / (1024 * 1024)
        print(f"{status} {name:<20} | {size_mb:>6.2f} MB | {sql_path}")
    
    print("-" * 70)
    print(f"Total Rows Generated: {total_rows:,}")
    print("=" * 70)
    
    print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed_scripts:
        print(f"\n[WARNING] Failed Scripts: {', '.join(failed_scripts)}")
        print("\n" + "=" * 70)
        return 1
    else:
        print("\n[OK] All scripts completed successfully!")
        print("\n" + "=" * 70)
        return 0


if __name__ == "__main__":
    sys.exit(main())
