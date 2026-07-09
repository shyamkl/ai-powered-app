import sqlite3

conn = sqlite3.connect(
    "venues.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS venues(

id INTEGER PRIMARY KEY,

name TEXT,

lat REAL,

lon REAL,

category TEXT,

address TEXT,

city TEXT
)

""")

conn.commit()