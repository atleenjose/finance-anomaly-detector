import pandas as pd
import random
import numpy as np

df = pd.read_csv("data/transactions.csv")
print("Before:", df.shape)

dupes = df.sample(100, random_state=42)
df = pd.concat([df, dupes]).reset_index(drop=True)

null_indices_merchant = random.sample(range(len(df)), 30)
null_indices_category = random.sample(range(len(df)), 20)
df.loc[null_indices_merchant, "merchant"] = None
df.loc[null_indices_category, "category"] = None

outlier_indices = random.sample(range(len(df)), 30)
df.loc[outlier_indices, "amount"] = df.loc[outlier_indices, "amount"].apply(
    lambda x: round(x * random.uniform(10, 20), 2)
)

df.to_csv("data/transactions_messy.csv", index=False)
print("After:", df.shape)
print(df.isnull().sum())