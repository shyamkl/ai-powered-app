import pandas as pd
import csv
import math

from sqlalchemy.orm import Session

from database import SessionLocal
from models.venue import Venue

db: Session = SessionLocal()

print("CONNECTED DATABASE:", db.bind.url)

csv_path = r"data\mumbai_final.csv"

print("LOADING CSV...")

df = pd.read_csv(
    csv_path,
    sep="\t",
    encoding="latin1",
    engine="python",
    quoting=csv.QUOTE_NONE,
    on_bad_lines="skip"
)

print("CSV LOADED")

# CLEAN COLUMN NAMES
df.columns = (
    df.columns
    .str.strip()
    .str.replace('"', '', regex=False)
    .str.lower()
)

print(df.columns)

print("TOTAL CSV ROWS:", len(df))

# DELETE OLD MUMBAI DATA
deleted = db.query(Venue).filter(
    Venue.city == "Mumbai"
).delete()

db.commit()

print("OLD MUMBAI ROWS DELETED:", deleted)

inserted = 0

for _, row in df.iterrows():

    try:

        # SAFE LAT
        lat = row.get("lat", 0)

        if pd.isna(lat):
            lat = 0

        # SAFE LON
        lon = row.get("lon", 0)

        if pd.isna(lon):
            lon = 0

        venue = Venue(

            name=str(row.get("name", ""))[:255],

            category=str(
                row.get("category", "restaurant")
            )[:100],

            area=str(
                row.get("area", "Mumbai")
            )[:100],

            address=str(
                row.get("address", "")
            ),

            lat=float(lat),

            lon=float(lon),

            city="Mumbai",

            state="Maharashtra",

            country="India",

            website=str(
                row.get("website", "")
            ),

            deal=str(
                row.get("happy_hour_details", "")
            ),

            timing=str(
                row.get("happy_hour_timings", "")
            ),

            image_url=None
        )

        db.add(venue)

        inserted += 1

    except Exception as e:
        print("ROW FAILED:", e)

db.commit()

print("MUMBAI IMPORT COMPLETED")
print("TOTAL ROWS IMPORTED:", inserted)

db.close() 