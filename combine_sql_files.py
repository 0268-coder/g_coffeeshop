#!/usr/bin/env python3
"""
Script to combine three SQL files sequentially:
1. create_tables.sql
2. combined_inserts.sql
3. encryption.sql
"""

import os

def combine_sql_files(output_filename="g_coffeeshop_final.sql"):
    """
    Combine three SQL files in order into a single output file.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_path, "output")
    
    files_to_combine = [
        os.path.join(output_dir, "create_tables.sql"),
        os.path.join(output_dir, "combined_inserts.sql"),
        os.path.join(output_dir, "encryption.sql"),
    ]
    
    output_file = os.path.join(output_dir, output_filename)
    
    # Verify all input files exist
    for file_path in files_to_combine:
        if not os.path.exists(file_path):
            print(f"Error: File not found - {file_path}")
            return False
    
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Add initial setup to prevent duplicate key errors
            outfile.write("-- ============================================================================\n")
            outfile.write("-- G_COFFEESHOP DATABASE SETUP SCRIPT\n")
            outfile.write("-- ============================================================================\n")
            outfile.write("-- This script drops existing tables and recreates the database from scratch\n")
            outfile.write("-- ============================================================================\n\n")
            outfile.write("-- Drop existing database (optional - comment out if you want to keep old data)\n")
            outfile.write("-- DROP DATABASE IF EXISTS g_coffeeshop;\n\n")
            outfile.write("-- Disable foreign key checks to avoid constraint violations during setup\n")
            outfile.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
            for i, file_path in enumerate(files_to_combine):
                print(f"Processing: {os.path.basename(file_path)}")
                
                # Add separator comment between files
                if i > 0:
                    outfile.write("\n\n")
                    outfile.write("-- " + "=" * 78 + "\n")
                    outfile.write(f"-- {os.path.basename(file_path)}\n")
                    outfile.write("-- " + "=" * 78 + "\n\n")
                
                # Read and write the file content
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
                    
                    # Ensure newline at end if missing
                    if content and not content.endswith('\n'):
                        outfile.write('\n')
            
            # Add cleanup at the end
            outfile.write("\n\n")
            outfile.write("-- ============================================================================\n")
            outfile.write("-- Re-enable foreign key checks\n")
            outfile.write("-- ============================================================================\n")
            outfile.write("SET FOREIGN_KEY_CHECKS = 1;\n")
        
        print(f"\nSuccess! Combined file created: {output_file}")
        
        # Print file size info
        file_size = os.path.getsize(output_file)
        print(f"Output file size: {file_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    combine_sql_files()
