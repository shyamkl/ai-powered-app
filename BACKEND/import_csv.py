import pandas as pd
import os
from database import SessionLocal
from models.venue import Venue

DATA_FOLDER = "data"

def clean_value(val):
    if pd.isna(val):
        return None
    return val

def extract_location(address):
    if not address or not isinstance(address, str):
        return None, None, None

    # If address looks like garbage text, ignore it
    if len(address) > 150:   # 🔥 key fix
        return None, None, None

    parts = [p.strip() for p in address.split(",")]

    if len(parts) < 2:
        return None, None, None

    city = parts[-3] if len(parts) >= 3 else None
    state = parts[-2] if len(parts) >= 2 else None
    country = parts[-1] if len(parts) >= 1 else None

    return city, state, country

def safe_str(val, max_len=100):
    if val is None:
        return None
    val = str(val)
    return val[:max_len]

def import_file(file_path):
    db = SessionLocal()

    print(f"📥 Importing: {file_path}")

    try:
        df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="latin-1", on_bad_lines="skip")
    df = df.where(pd.notna(df), None)

    for _, row in df.iterrows():

        city, state, country = extract_location(row.get("address"))

        venue = Venue(
    name=safe_str(clean_value(row.get("name")), 255),

    address=safe_str(clean_value(row.get("address")), 255),

    city=safe_str(city, 100),
    state=safe_str(state, 100),
    country=safe_str(country, 100),

    category=safe_str(clean_value(row.get("category")), 50),
    area=safe_str(clean_value(row.get("area")), 200),

    website=safe_str(clean_value(row.get("website")), 255),

    lat=clean_value(row.get("lat")),
    lon=clean_value(row.get("lon")),

    deal=clean_value(row.get("deal")),
    timing=clean_value(row.get("timing")),
    image_url=clean_value(row.get("image_url")),
    image_source=clean_value(row.get("image_source")),
    local_image=clean_value(row.get("local_image")),
    wikidata=clean_value(row.get("wikidata")),
    wikipedia=clean_value(row.get("wikipedia")),
    rating=clean_value(row.get("rating")),
    reviews_count=clean_value(row.get("reviews_count")),
    embedding=None
)

        db.add(venue)

    db.commit()
    db.close()

    print(f"✅ Done: {file_path}")


def import_all_csvs():
    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]

    print(f"📂 Found {len(files)} CSV files")

    for file in files:
        file_path = os.path.join(DATA_FOLDER, file)
        import_file(file_path)

    print("🎉 ALL CSV FILES IMPORTED SUCCESSFULLY")


if __name__ == "__main__":
    import_all_csvs()