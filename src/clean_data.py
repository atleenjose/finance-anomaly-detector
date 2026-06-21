import pandas as pd

df = pd.read_csv("data/transactions_messy.csv")
df = df.drop_duplicates(subset="transaction_id", keep="first").reset_index(drop=True)

df["merchant"] = df["merchant"].fillna("Unknown Merchant")
df["category"] = df["category"].fillna(df["category"].mode()[0])

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month
df["day_of_week"] = df["date"].dt.dayofweek
print(df[["date", "month", "day_of_week"]].head())

df = df.sort_values(["customer_id", "date"]).reset_index(drop=True)
df["rolling_avg_7d"] = (
    df.groupby("customer_id")["amount"]
    .transform(lambda x: x.rolling(7, min_periods=1).mean())
    .round(2)
)
df[["customer_id", "date", "amount", "rolling_avg_7d"]].head(10)

df.to_csv("data/transactions_clean.csv", index=False)
print("After:", df.shape)
print(df.isnull().sum())