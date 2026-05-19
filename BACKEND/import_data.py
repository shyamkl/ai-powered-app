import os
import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
from models.venue import Venue


CSV_FILES = [
    "data/chennai_final.csv",
    "data/Bangkok_final.csv",
    "data/krabi_final.csv",
    "data/mumbai_final.csv"
]


def safe_read_csv(file):
    try:
        return pd.read_csv(file, encoding="utf-8", on_bad_lines="skip")
    except UnicodeDecodeError:
        return pd.read_csv(file, encoding="latin1", on_bad_lines="skip")


# 🔥 Clean NaN
def clean(value):
    if pd.isna(value):
        return None
    return value


# 🔥 Prevent DB overflow
def limit(value, max_len=100):
    if value and isinstance(value, str):
        return value[:max_len]
    return value


def normalize_row(row):
    address = clean(row.get("address"))

    parts = address.split(",") if isinstance(address, str) else []

    # safer extraction
    city = clean(row.get("city")) or (parts[-3].strip() if len(parts) >= 3 else None)
    state = clean(row.get("state")) or (parts[-2].strip() if len(parts) >= 2 else None)
    country = clean(row.get("country")) or (parts[-1].strip() if len(parts) >= 1 else None)

    # 🔥 FIX: avoid garbage long strings
    country = limit(country, 50)
    city = limit(city, 50)
    state = limit(state, 50)

    return Venue(
        name=limit(clean(row.get("name")), 200),
        source=limit(clean(row.get("source")), 50),

        lat=float(row["lat"]) if pd.notna(row.get("lat")) else None,
        lon=float(row["lon"]) if pd.notna(row.get("lon")) else None,

        address=limit(address, 300),

        city=city,
        state=state,
        country=country,

        category=limit(clean(row.get("category")), 50),
        area=limit(clean(row.get("area")), 100),

        deal=limit(clean(row.get("deal")), 200),
        timing=limit(clean(row.get("timing")), 100),

        image_url=limit(clean(row.get("image_url")), 300),
        image_source=limit(clean(row.get("image_source")), 50),
        local_image=limit(clean(row.get("local_image")), 200),

        website=limit(clean(row.get("website")), 200),
        wikidata=limit(clean(row.get("wikidata")), 100),
        wikipedia=limit(clean(row.get("wikipedia")), 200),

        rating=float(row["rating"]) if pd.notna(row.get("rating")) else None,
        reviews_count=int(row["reviews_count"]) if pd.notna(row.get("reviews_count")) else None,

        embedding=None  # safer to ignore for now
    )


def load_all_data():
    all_data = []

    for file in CSV_FILES:
        if not os.path.exists(file):
            print(f"⚠️ File not found: {file}")
            continue

        df = safe_read_csv(file)
        print(f"✅ Loaded: {file} ({len(df)} rows)")
        all_data.append(df)

    return pd.concat(all_data, ignore_index=True)


def insert_data():
    db: Session = SessionLocal()

    df = load_all_data()
    inserted = 0

    for _, row in df.iterrows():
        try:
            venue = normalize_row(row)
            db.add(venue)
            inserted += 1
        except Exception as e:
            print(f"❌ Skipped row: {e}")

    db.commit()
    db.close()

    print(f"\n✅ Inserted {inserted} records successfully!")


if __name__ == "__main__":
    insert_data()