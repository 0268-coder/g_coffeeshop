import os
import glob
import sys

# Get the directory of this script and construct relative path to insert sql directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILES_DIRECTORY = os.path.join(SCRIPT_DIR, 'insert_statements')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'combined_inserts.sql')

# Whitelist of files to include in combined_inserts.sql (in desired order)
# This prevents duplicate data and ensures proper structure
APPROVED_FILES = [
    'delivery_addresses.sql',
    'delivery_data.sql',
    'employee.sql',
    'handle.sql',
    'inventory.sql',
    'inventory_transaction.sql',
    'menu_item.sql',
    'purin_consolidated_inserts.sql',
    'reduction.sql',
    'restock.sql',
    'supplier.sql',
]

def combine_sql_files(directory=SQL_FILES_DIRECTORY, output_file=None):
    """
    Combines approved .sql files in a specified directory into a single file.
    Uses a whitelist to ensure correct file order and prevent duplicates.
    
    Args:
        directory (str): The directory containing SQL files to merge (default: SQL_FILES_DIRECTORY)
        output_file (str): The name of the output combined SQL file (default: combined_inserts.sql)
    """
    # Set default output file if not provided
    if output_file is None:
        output_file = OUTPUT_FILE
    
    # Validate directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return False
    
    # Get approved SQL files in specified order
    sql_files = []
    missing_files = []
    
    for filename in APPROVED_FILES:
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            sql_files.append(filepath)
        else:
            missing_files.append(filename)
    
    if not sql_files:
        print(f"No approved SQL files found in '{directory}'.")
        return False
    
    if missing_files:
        print(f"Warning: The following approved files were not found:")
        for f in missing_files:
            print(f"  - {f}")
    
    print(f"Found {len(sql_files)} SQL files in '{directory}':")
    for file in sql_files:
        print(f"  - {os.path.basename(file)}")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Combine all SQL files
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Add foreign key check disable at the beginning
        outfile.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
        
        for i, sql_file in enumerate(sql_files):
            print(f"Processing: {os.path.basename(sql_file)}")
            with open(sql_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)
                # Add a separator between files for clarity
                if i < len(sql_files) - 1:
                    outfile.write('\n\n')
        
        # Add foreign key check enable at the end
        outfile.write("\n\nSET FOREIGN_KEY_CHECKS = 1;")
    
    print(f"\nSuccessfully combined {len(sql_files)} files into '{output_file}'")
    return True

if __name__ == '__main__':
    combine_sql_files(SQL_FILES_DIRECTORY)
