import pandas as pd

df = pd.read_csv("data/transactions_clean.csv")
print(df["transaction_id"].duplicated().sum())
print(df[df["transaction_id"].duplicated(keep=False)].sort_values("transaction_id").head(10))