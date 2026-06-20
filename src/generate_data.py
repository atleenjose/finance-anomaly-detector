from faker import Faker
import pandas as pd
import random

fake = Faker()

categories = ["groceries", "travel", "dining", "shopping", "utilities", "entertainment"]
payment_modes = ["credit card", "debit card", "UPI", "net banking"]
customer_ids = [f"CUST{str(i).zfill(3)}" for i in range(1, 51)]

transactions = []

for i in range(2000):
    transactions.append({
        "transaction_id": f"TXN{str(i).zfill(5)}",
        "date": fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d"),
        "customer_id": random.choice(customer_ids),
        "merchant": fake.company(),
        "category": random.choice(categories),
        "amount": round(random.uniform(10, 1000), 2),
        "payment_mode": random.choice(payment_modes),
    })

df = pd.DataFrame(transactions)
df.to_csv("data/transactions.csv", index=False)
print(df.head())