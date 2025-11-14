# PurinCode Data Generation Guide

## Overview

The `purincode` folder contains Python scripts that generate synthetic payment transaction data for the G CoffeeShop database. These scripts create realistic data for different payment methods and export them in both CSV and SQL formats.

## Folder Structure

```
purincode/
├── python/                          # Python scripts for data generation
│   ├── run_all_generators.py       # Master script - runs all generators
│   ├── generate_cash.py            # Cash payment data (payment_method_id = 4)
│   ├── generate_promptpay.py       # PromptPay data (payment_method_id = 5)
│   ├── generate_credit.py          # Credit card data (payment_method_id = 2)
│   ├── generate_debit.py           # Debit card data (payment_method_id = 3)
│   ├── generate_giftcard.py        # Gift card data (payment_method_id = 1)
│   ├── extractTransactions.py      # Extract transactions from SQL file
│   └── count_payment_methods.py    # Count payment methods in extracted data
│
├── info/                            # Input/output data files
│   ├── payment_transaction_extracted.csv   # Source data for all generators
│   ├── cash_synthetic.csv                  # Generated cash data
│   ├── promptpay_synthetic.csv             # Generated PromptPay data
│   ├── credit_synthetic.csv                # Generated credit card data
│   ├── debit_synthetic.csv                 # Generated debit card data
│   └── giftcard_synthetic.csv              # Generated gift card data
│
├── insert sql/                      # SQL INSERT statements
│   ├── cash_inserts.sql
│   ├── promptpay_inserts.sql
│   ├── credit_inserts.sql
│   ├── debit_inserts.sql
│   ├── giftcard_inserts.sql
│   └── consolidated_inserts.sql    # All INSERT statements combined
│
└── sql/                             # SQL table definition files
    ├── cash.sql
    ├── promptpay.sql
    ├── credit.sql
    ├── debit.sql
    ├── gift_card.sql
    └── payment_method.sql
```

## Quick Start

### Option 1: Run All Generators at Once (Recommended)

This is the easiest way to generate all payment method data.

```bash
cd e:\g_coffeeshop\purincode\python
$env:PYTHONIOENCODING='utf-8'
python run_all_generators.py
```



### Option 2: Run Individual Generators

You can also run specific payment method generators individually.

#### Generate Cash Data

```bash
cd e:\g_coffeeshop\purincode\python
python generate_cash.py
```



#### Generate PromptPay Data

```bash
cd e:\g_coffeeshop\purincode\python
python generate_promptpay.py
```



#### Generate Credit Card Data

```bash
cd e:\g_coffeeshop\purincode\python
python generate_credit.py
```



#### Generate Debit Card Data

```bash
cd e:\g_coffeeshop\purincode\python
python generate_debit.py
```

**Output Example:** (Similar to credit card data)

#### Generate Gift Card Data

```bash
cd e:\g_coffeeshop\purincode\python
python generate_giftcard.py
```



## Recommended Workflow

### Step 1: Extract Payment Transactions (if needed)

If you have a new `payment_transaction.sql` file and need to extract transaction data:

```bash
cd e:\g_coffeeshop\purincode\python
python extractTransactions.py
```

This creates `payment_transaction_extracted.csv` in the `info/` folder.

### Step 2: Count Payment Methods (optional)

To see the distribution of payment methods in your data:

```bash
cd e:\g_coffeeshop\purincode\python
python count_payment_methods.py
```



### Step 3: Generate All Payment Data

Run the master script to generate all payment method data:

```bash
cd e:\g_coffeeshop\purincode\python
$env:PYTHONIOENCODING='utf-8'
python run_all_generators.py
```

### Step 4: Import to Database

Use the generated SQL files to populate your database:

```bash
# For individual tables:
mysql -u [username] -p [database_name] < e:\g_coffeeshop\purincode\insert sql\cash_inserts.sql
mysql -u [username] -p [database_name] < e:\g_coffeeshop\purincode\insert sql\promptpay_inserts.sql
mysql -u [username] -p [database_name] < e:\g_coffeeshop\purincode\insert sql\credit_inserts.sql
mysql -u [username] -p [database_name] < e:\g_coffeeshop\purincode\insert sql\debit_inserts.sql
mysql -u [username] -p [database_name] < e:\g_coffeeshop\purincode\insert sql\giftcard_inserts.sql

# Or use consolidated file (if available):
mysql -u [username] -p [database_name] < e:\g_coffeeshop\purincode\insert sql\consolidated_inserts.sql
```

## Generated Data Specifications

### Payment Method ID Mapping

| Payment Method | ID | Script | Rows |
|---|---|---|---|
| Gift Card | 1 | `generate_giftcard.py` | 4,097 |
| Credit Card | 2 | `generate_credit.py` | 4,008 |
| Debit Card | 3 | `generate_debit.py` | 3,988 |
| Cash | 4 | `generate_cash.py` | 3,962 |
| PromptPay | 5 | `generate_promptpay.py` | 3,982 |

### Cash Data
- **cash_id**: Auto-incremented ID (1-3962)
- **cash_received**: Payment amount + change (0-100 THB)
- **cash_change**: Difference between received and payment amount

### PromptPay Data
- **promptpay_id**: Auto-incremented ID (1-3982)
- **transaction_ref**: Date-based (YYYYMMDD) + 17 random alphanumeric characters
- **bank_name**: Random Thai bank names

### Credit/Debit Card Data
- **credit_id/debit_id**: Auto-incremented ID
- **Last 4 digits**: Random (1000-9999)
- **fname**: Thai first name (randomly generated)
- **lname**: Thai last name (randomly generated)

### Gift Card Data
- **giftcard_id**: Auto-incremented ID (1-4097)
- **initial_value**: Payment amount rounded to nearest 100
- **current_balance**: 0-100% of initial value (simulating usage)
- **status**: Active, Used, or Expired
- **code**: Random 20-character alphanumeric code
- **issued_date**: Random (up to 2 years before base date)
- **expiry_date**: Random (6 months to 3 years after issued date)

## Output Files

All generated files are placed in two locations:

### CSV Format
- Location: `e:\g_coffeeshop\purincode\info\`
- Use for: Data analysis, import to other systems, backups
- Files: `*_synthetic.csv`

### SQL Format
- Location: `e:\g_coffeeshop\purincode\insert sql\`
- Use for: Direct database import with `mysql` command
- Files: `*_inserts.sql`

## Troubleshooting

### Unicode/Encoding Issues

If you see encoding errors, set the Python encoding environment variable:

```bash
$env:PYTHONIOENCODING='utf-8'
python run_all_generators.py
```

### Missing Input File

If you get "File not found" error, make sure `payment_transaction_extracted.csv` exists in `info/` folder. If not, run:

```bash
python extractTransactions.py
```

### Script Execution Errors

Check that all required files exist in the `info/` directory before running generators.

## Notes

- All scripts use absolute paths, so they can be run from any directory
- Random data is generated fresh each time, so values will differ between runs
- SQL files are formatted for MySQL databases
- Thai language support is included for cardholder names
- All monetary values are in Thai Baht (฿)

