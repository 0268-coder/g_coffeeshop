import re
import csv

INPUT_FILE = "../../payment_transaction.sql"
OUTPUT_FILE = "../info/payment_transaction_extracted.csv"

# --------------------------------------------------
# STEP 1 — Load SQL file
# --------------------------------------------------
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    sql_text = f.read()

# --------------------------------------------------
# STEP 2 — Extract tuples (...)
# --------------------------------------------------
pattern = r"\(([^;]+?)\)"
matches = re.findall(pattern, sql_text, re.DOTALL)

rows = []

for row in matches:
    parts = [p.strip() for p in row.split(",")]

    if len(parts) < 6:
        continue

    # Extract values
    final_amount = parts[3].strip().strip("'").strip("`")
    created_at = parts[4].strip().strip("'").strip("`")
    method_id = parts[5].strip().strip("`")

    # --------------------------------------------------
    # IGNORE ANY "header-like" rows
    # --------------------------------------------------
    if final_amount.lower() in ["payment_final_amount"]:
        continue
    if method_id.lower() in ["payment_method_id"]:
        continue
    if created_at.lower() in ["payment_created_at"]:
        continue

    # Keep clean row
    rows.append([final_amount, method_id, created_at])

# --------------------------------------------------
# STEP 3 — Write to CSV (header once)
# --------------------------------------------------
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["payment_final_amount", "payment_method_id", "payment_created_at"])
    writer.writerows(rows)

print(f"Done! Clean rows written: {len(rows)}")
