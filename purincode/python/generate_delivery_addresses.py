#!/usr/bin/env python3
"""
Generate synthetic delivery address data for Bangkok.
Creates SQL INSERT statements for the delivery_address table with randomly selected Bangkok areas.
"""

import random
from pathlib import Path


# Bangkok sub-districts and their corresponding district, province, and postal code
BANGKOK_AREAS = [
    # Khlong Toei District
    {'sub_district': 'Khlong Toei', 'district': 'Khlong Toei', 'province': 'Bangkok', 'postal_code': '10110'},
    {'sub_district': 'Bangrak', 'district': 'Khlong Toei', 'province': 'Bangkok', 'postal_code': '10500'},
    
    # Pathum Wan District
    {'sub_district': 'Lumphini', 'district': 'Pathum Wan', 'province': 'Bangkok', 'postal_code': '10330'},
    {'sub_district': 'Pathumwan', 'district': 'Pathum Wan', 'province': 'Bangkok', 'postal_code': '10330'},
    {'sub_district': 'Silom', 'district': 'Pathum Wan', 'province': 'Bangkok', 'postal_code': '10110'},
    
    # Phaya Thai District
    {'sub_district': 'Samsen Nai', 'district': 'Phaya Thai', 'province': 'Bangkok', 'postal_code': '10400'},
    {'sub_district': 'Win', 'district': 'Phaya Thai', 'province': 'Bangkok', 'postal_code': '10400'},
    {'sub_district': 'Thanon Phetchaburi', 'district': 'Phaya Thai', 'province': 'Bangkok', 'postal_code': '10400'},
    
    # Din Daeng District
    {'sub_district': 'Din Daeng', 'district': 'Din Daeng', 'province': 'Bangkok', 'postal_code': '10400'},
    {'sub_district': 'Huai Khwang', 'district': 'Din Daeng', 'province': 'Bangkok', 'postal_code': '10310'},
    
    # Chatuchak District
    {'sub_district': 'Chom Phon', 'district': 'Chatuchak', 'province': 'Bangkok', 'postal_code': '10900'},
    {'sub_district': 'Saphan Song', 'district': 'Chatuchak', 'province': 'Bangkok', 'postal_code': '10900'},
    {'sub_district': 'Chatuchak', 'district': 'Chatuchak', 'province': 'Bangkok', 'postal_code': '10900'},
    
    # Prawet District
    {'sub_district': 'Nong Bon', 'district': 'Prawet', 'province': 'Bangkok', 'postal_code': '10250'},
    {'sub_district': 'Sai Mai', 'district': 'Prawet', 'province': 'Bangkok', 'postal_code': '10250'},
    
    # Lat Phrao District
    {'sub_district': 'Lat Phrao', 'district': 'Lat Phrao', 'province': 'Bangkok', 'postal_code': '10230'},
    {'sub_district': 'Sena Nikhom', 'district': 'Lat Phrao', 'province': 'Bangkok', 'postal_code': '10230'},
    
    # Bang Na District
    {'sub_district': 'Bang Na Nuea', 'district': 'Bang Na', 'province': 'Bangkok', 'postal_code': '10260'},
    {'sub_district': 'Bang Na Tai', 'district': 'Bang Na', 'province': 'Bangkok', 'postal_code': '10260'},
    
    # Khlong San District
    {'sub_district': 'Khlong San', 'district': 'Khlong San', 'province': 'Bangkok', 'postal_code': '10600'},
    {'sub_district': 'Khlong Toei', 'district': 'Khlong San', 'province': 'Bangkok', 'postal_code': '10600'},
    
    # Phasi Charoen District
    {'sub_district': 'Bang Duan', 'district': 'Phasi Charoen', 'province': 'Bangkok', 'postal_code': '10160'},
    {'sub_district': 'Phasi Charoen', 'district': 'Phasi Charoen', 'province': 'Bangkok', 'postal_code': '10160'},
    
    # Taling Chan District
    {'sub_district': 'Taling Chan', 'district': 'Taling Chan', 'province': 'Bangkok', 'postal_code': '10170'},
    {'sub_district': 'Bang Phlat', 'district': 'Taling Chan', 'province': 'Bangkok', 'postal_code': '10170'},
    
    # Ratchathewi District
    {'sub_district': 'Makkasan', 'district': 'Ratchathewi', 'province': 'Bangkok', 'postal_code': '10320'},
    {'sub_district': 'Ratchathewi', 'district': 'Ratchathewi', 'province': 'Bangkok', 'postal_code': '10400'},
    
    # Wattana District
    {'sub_district': 'Nana', 'district': 'Wattana', 'province': 'Bangkok', 'postal_code': '10110'},
    {'sub_district': 'Phloen Chit', 'district': 'Wattana', 'province': 'Bangkok', 'postal_code': '10330'},
    
    # Sathon District
    {'sub_district': 'Sathon', 'district': 'Sathon', 'province': 'Bangkok', 'postal_code': '10120'},
    {'sub_district': 'Bang Rak', 'district': 'Sathon', 'province': 'Bangkok', 'postal_code': '10500'},
]

# Street name patterns for generating realistic addresses
STREET_PREFIXES = [
    'Soi', 'Thanon', 'Sukhumvit', 'Rama', 'Ari', 'Ratchada', 'Ladprao',
    'Srinakarin', 'Pradit Manutham', 'Bangna-Trad', 'Latya', 'Phetkasem',
    'Silom', 'Wireless', 'Phetchaburi', 'Kaset', 'Chula', 'Rattanakosin'
]

STREET_NUMBERS = list(range(1, 500))


def generate_street_address():
    """Generate a realistic Bangkok street address."""
    prefix = random.choice(STREET_PREFIXES)
    number = random.choice(STREET_NUMBERS)
    sub_number = random.randint(1, 20)
    return f"{number}/{sub_number} {prefix}"


def generate_delivery_addresses(output_sql_path, num_records=10019):
    """
    Generate synthetic delivery address data as SQL INSERT statements.
    
    Args:
        output_sql_path: Path where the SQL file will be saved
        num_records: Number of delivery addresses to generate
    """
    
    try:
        with open(output_sql_path, 'w', encoding='utf-8') as sqlfile:
            # Write the INSERT statement header
            sqlfile.write("INSERT INTO delivery_address (delivery_address_id, delivery_id, street, sub_district, district, province, postal_code) VALUES\n")
            
            # Generate records
            for idx, delivery_id in enumerate(range(1, num_records + 1)):
                area = random.choice(BANGKOK_AREAS)
                street = generate_street_address()
                
                # Escape single quotes in the data
                street = street.replace("'", "''")
                sub_district = area['sub_district'].replace("'", "''")
                district = area['district'].replace("'", "''")
                province = area['province'].replace("'", "''")
                
                # Format the value tuple
                value = f"({delivery_id}, {delivery_id}, '{street}', '{sub_district}', '{district}', '{province}', '{area['postal_code']}')"
                
                # Add comma except for the last record
                if idx < num_records - 1:
                    sqlfile.write(value + ",\n")
                else:
                    sqlfile.write(value + ";\n")
        
        print(f"✓ Successfully generated {num_records} delivery addresses")
        print(f"✓ SQL file saved to: {output_sql_path}")
        return True
    
    except Exception as e:
        print(f"Error writing SQL file: {e}")
        return False


if __name__ == "__main__":
    # Define file paths
    script_dir = Path(__file__).parent
    output_sql = script_dir / "../insert sql" / "delivery_addresses.sql"
    
    # Generate synthetic data
    if generate_delivery_addresses(output_sql):
        print(f"\nFile location: {output_sql}")
    else:
        print("\nGeneration failed.")
