from openai import OpenAI
from database import SessionLocal
from models import Venue
import json

client = OpenAI(api_key="YOUR_API_KEY")
db = SessionLocal()

venues = db.query(Venue).all()

for v in venues:
    text = f"{v.name}, {v.category}, {v.area}, {v.address}"

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    v.embedding = json.dumps(response.data[0].embedding)

db.commit()
db.close()

print("✅ Embeddings generated")