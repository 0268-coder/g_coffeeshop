import os
import glob
import sys

# Get the directory of this script and construct relative path to insert sql directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILES_DIRECTORY = os.path.join(SCRIPT_DIR, 'insert_statements')

# Define the default order of SQL files to combine
# Leave empty to use alphabetical order
DEFAULT_FILE_ORDER = [
    'giftcard_inserts.sql',
    'credit_inserts.sql',
    'debit_inserts.sql',
    'cash_inserts.sql',
    'promptpay_inserts.sql',
]

def combine_sql_files(directory=SQL_FILES_DIRECTORY, output_file='combined.sql', file_order=None):
    """
    Combines all .sql files in a specified directory into a single file.
    
    Args:
        directory (str): The directory containing SQL files to merge (default: SQL_FILES_DIRECTORY)
        output_file (str): The name of the output combined SQL file
        file_order (list): Optional list of filenames to specify the order of combination
    """
    # Use provided order or fall back to default
    if file_order is None:
        file_order = DEFAULT_FILE_ORDER
    
    # Validate directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return False
    
    # Get all .sql files in the specified directory
    pattern = os.path.join(directory, '*.sql')
    available_files = sorted(glob.glob(pattern))
    
    # Order files according to file_order list
    sql_files = []
    unordered_files = []
    
    # First, add files in the specified order
    for filename in file_order:
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            sql_files.append(filepath)
    
    # Then, add any remaining files not in the order list (in alphabetical order)
    for filepath in available_files:
        if filepath not in sql_files:
            unordered_files.append(filepath)
    
    sql_files.extend(unordered_files)
    
    if not sql_files:
        print(f"No .sql files found in '{directory}'.")
        return False
    
    print(f"Found {len(sql_files)} SQL files in '{directory}':")
    for file in sql_files:
        print(f"  - {os.path.basename(file)}")
    
    # Combine all SQL files
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, sql_file in enumerate(sql_files):
            print(f"Processing: {os.path.basename(sql_file)}")
            with open(sql_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)
                # Add a separator between files for clarity
                if i < len(sql_files) - 1:
                    outfile.write('\n\n')
    
    print(f"\nSuccessfully combined {len(sql_files)} files into '{output_file}'")
    return True

if __name__ == '__main__':
    # Check if directory argument provided
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'output/combined.sql'
        
        # Check if custom file order is provided (comma-separated)
        file_order = None
        if len(sys.argv) > 3:
            file_order = [f.strip() for f in sys.argv[3].split(',')]
        
        combine_sql_files(directory, output_file, file_order)
    else:
        print("Usage: python combine.py <directory> [output_file] [file_order]")
        print("  <directory>: Path to directory containing SQL files")
        print("  [output_file]: Optional output filename (default: combined.sql)")
        print("  [file_order]: Optional comma-separated list of filenames in desired order")
        print("\nExamples:")
        print("  python combine.py './purincode/insert sql'")
        print("  python combine.py './purincode/insert sql' './output/merged.sql'")
        print("  python combine.py './purincode/insert sql' './output/merged.sql' 'cash_inserts.sql,credit_inserts.sql,debit_inserts.sql'")
