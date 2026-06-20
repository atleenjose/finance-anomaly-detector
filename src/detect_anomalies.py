import pandas as pd
from sklearn.ensemble import IsolationForest

df = pd.read_csv("data/transactions_clean.csv")
print(df.shape)
print(df.dtypes)

features = ["amount", "month", "day_of_week", "rolling_avg_7d"]
X = df[features]

model = IsolationForest(contamination=0.05, random_state=42)
df["anomaly"] = model.fit_predict(X)

print(df["anomaly"].value_counts())

df["anomaly_flag"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

flagged = df[df["anomaly_flag"] == 1]
print(flagged[["customer_id", "date", "amount", "rolling_avg_7d", "category"]].head(10))

df.to_csv("data/transactions_anomalies.csv", index=False)