import pandas as pd
from database.connection import engine

# 👉 change filename to your uploaded CSV
df = pd.read_csv("Bangkok_final.csv")

# Clean column names (important)
df.columns = [col.lower().strip() for col in df.columns]

# Rename if needed (depends on your CSV)
df.rename(columns={
    "latitude": "lat",
    "longitude": "lon"
}, inplace=True)

# Insert into MySQL
df.to_sql("venues", con=engine, if_exists="append", index=False)

print("✅ Data inserted successfully")