from collections import Counter
import csv

# Read the CSV file and count payment_method_id occurrences
payment_method_counts = Counter()

with open('../info/payment_transaction_extracted.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        payment_method_id = row['payment_method_id']
        payment_method_counts[payment_method_id] += 1

print("Payment Method ID Counts:")
print("=" * 40)

# Sort by payment_method_id (numeric sort)
for method_id in sorted(payment_method_counts.keys(), key=int):
    count = payment_method_counts[method_id]
    print(f"payment_method_id {method_id}: {count} transactions")

print("\n" + "=" * 40)
print(f"Total transactions: {sum(payment_method_counts.values())}")
