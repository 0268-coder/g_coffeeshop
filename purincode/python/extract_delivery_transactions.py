#!/usr/bin/env python3
"""
Extract delivery transaction data from SQL INSERT statements to CSV.
This script parses delivery_data.sql and converts the delivery_transaction 
INSERT statements to CSV format.
"""

import re
import csv
from pathlib import Path


def extract_delivery_transactions(sql_file_path, output_csv_path):
    """
    Extract delivery transaction data from SQL INSERT file and save to CSV.
    
    Args:
        sql_file_path: Path to the SQL file containing INSERT statements
        output_csv_path: Path where the CSV file will be saved
    """
    
    # Read the SQL file
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all delivery_transaction INSERT blocks
    # Pattern: capture everything between VALUES and either a semicolon or another INSERT statement
    pattern = r"INSERT INTO delivery_transaction \(delivery_id, delivery_time, transaction_id\) VALUES\s*(.*?)(?=INSERT INTO|;|\Z)"
    matches = re.findall(pattern, content, re.DOTALL)
    
    if not matches:
        print("Error: Could not find delivery_transaction INSERT statements")
        return False
    
    # Extract individual tuples from all blocks
    # Pattern: (delivery_id, 'delivery_time', 'transaction_id')
    tuple_pattern = r"\((\d+),\s*'([^']+)',\s*'([^']+)'\)"
    all_tuples = []
    
    for values_block in matches:
        tuples = re.findall(tuple_pattern, values_block)
        all_tuples.extend(tuples)
    
    if not all_tuples:
        print("Error: Could not extract delivery transaction tuples")
        return False
    
    # Write to CSV
    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['delivery_id', 'delivery_time', 'transaction_id'])
            
            # Write data rows
            writer.writerows(all_tuples)
        
        print(f"✓ Successfully extracted {len(all_tuples)} delivery transactions")
        print(f"✓ CSV saved to: {output_csv_path}")
        return True
    
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        return False


if __name__ == "__main__":
    # Define file paths
    script_dir = Path(__file__).parent
    sql_file = script_dir / "../../insert_statements" / "delivery_data.sql"
    output_csv = script_dir / "../info" / "delivery_transactions.csv"
    
    # Extract and convert
    if extract_delivery_transactions(sql_file, output_csv):
        print(f"\nFile location: {output_csv}")
    else:
        print("\nExtraction failed.")
