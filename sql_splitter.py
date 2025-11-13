import re
import os
import sys

def split_sql_file(input_filepath):
    """
    Reads a single SQL file containing multiple CREATE TABLE and INSERT INTO
    statements and splits them into individual files based on table name.
    
    A new file '{table_name}.sql' is created for each table. The CREATE TABLE
    statement and all subsequent INSERT INTO statements for that table are
    written to the new file.
    
    Args:
        input_filepath (str): The path to the monolithic SQL input file.
    """
    
    # Regex to capture table name (handles optional backticks and schema.table format)
    # We focus on capturing the name immediately following CREATE TABLE or INSERT INTO
    
    # Pattern for CREATE TABLE: captures the table name (group 2)
    CREATE_TABLE_PATTERN = re.compile(
        r"^\s*CREATE\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+(`?[\w\.]+`?)",
        re.IGNORECASE | re.MULTILINE
    )
    
    # Pattern for INSERT INTO: captures the table name (group 1)
    INSERT_INTO_PATTERN = re.compile(
        r"^\s*INSERT\s+INTO\s+(`?[\w\.]+`?)",
        re.IGNORECASE | re.MULTILINE
    )
    
    output_files = {}  # Stores open file handles: {table_name: file_handle}
    current_statement = [] # Stores lines of the current ongoing statement
    current_table = None   # Tracks the table name for the current statement block
    
    print(f"Starting to process: {input_filepath}")
    
    try:
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            for line_number, line in enumerate(infile, 1):
                # 1. Skip comments and empty lines for cleaner processing
                if line.strip().startswith('--') or line.strip().startswith('/*') or not line.strip():
                    continue

                current_statement.append(line)
                
                # Check if the current line ends the statement
                if line.strip().endswith(';'):
                    full_statement = "".join(current_statement).strip()
                    current_statement = [] # Reset for the next statement

                    # --- Statement Processing ---
                    
                    # A. Check for CREATE TABLE statement
                    match_create = CREATE_TABLE_PATTERN.match(full_statement)
                    if match_create:
                        # Use the captured table name (group 1)
                        table_name = match_create.group(1).strip('`').split('.')[-1]
                        current_table = table_name # Set the active table for writing
                        
                        # Close existing file handle for safety (though it shouldn't happen)
                        if table_name in output_files:
                            output_files[table_name].close()
                            
                        output_filepath = f"{table_name}.sql"
                        output_files[table_name] = open(output_filepath, 'w', encoding='utf-8')
                        print(f"--> Created new file: {output_filepath}")
                    
                    # B. Check for INSERT INTO statement
                    match_insert = INSERT_INTO_PATTERN.match(full_statement)
                    if match_insert:
                        # Use the captured table name (group 1)
                        table_name = match_insert.group(1).strip('`').split('.')[-1]
                        current_table = table_name # Update current_table for potential future relevance (less important here)
                        
                        # Ensure the file handle exists for the table
                        if table_name not in output_files:
                            output_filepath = f"{table_name}.sql"
                            # If we encounter an INSERT before a CREATE, we assume the CREATE must have been missed,
                            # so we create the file anyway. This is robust.
                            output_files[table_name] = open(output_filepath, 'a', encoding='utf-8')
                            print(f"--> Opened existing file for INSERT: {output_filepath}")
                            
                    
                    # --- Writing Logic ---
                    
                    # Determine which file to write to
                    table_to_write = None
                    if match_create:
                        table_to_write = table_name
                    elif match_insert:
                        table_to_write = table_name
                    elif current_table:
                        # Write subsequent lines of a multi-line statement (if not matched above)
                        table_to_write = current_table
                        
                    if table_to_write and table_to_write in output_files:
                        output_files[table_to_write].write(full_statement + "\n\n")
                    # If we don't have a table name, it's likely a global command (e.g., SET, USE)
                    # or an unmatched statement, which we will skip.
    
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        sys.exit(1)
    finally:
        # Ensure all file handles are closed
        for table, f_handle in output_files.items():
            f_handle.close()
        print("\nProcessing complete. All output files closed.")


if __name__ == '__main__':
    # Set the default input file name
    default_input_file = "g_coffeeshop_newest.sql"
    
    # Check if a file path was provided as a command-line argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = default_input_file
        
    split_sql_file(input_file)