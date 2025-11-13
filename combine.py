import os
import glob

def combine_sql_files(output_file='combined.sql'):
    """
    Combines all .sql files in the current directory into a single file.
    
    Args:
        output_file (str): The name of the output combined SQL file
    """
    # Get all .sql files in the current directory
    sql_files = sorted(glob.glob('*.sql'))
    
    if not sql_files:
        print("No .sql files found in the current directory.")
        return
    
    print(f"Found {len(sql_files)} SQL files:")
    for file in sql_files:
        print(f"  - {file}")
    
    # Combine all SQL files
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, sql_file in enumerate(sql_files):
            print(f"Processing: {sql_file}")
            with open(sql_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)
                # Add a separator between files for clarity
                if i < len(sql_files) - 1:
                    outfile.write('\n\n')
    
    print(f"\nSuccessfully combined {len(sql_files)} files into '{output_file}'")

if __name__ == '__main__':
    combine_sql_files()
