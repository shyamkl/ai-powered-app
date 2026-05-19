from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.venue import Venue
import numpy as np
import json
from openai import OpenAI

router = APIRouter()

client = OpenAI(api_key="YOUR_API_KEY")


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


@router.get("/search")
def search(query: str, db: Session = Depends(get_db)):
    
    # 🔥 Step 1: get query embedding
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    # 🔥 Step 2: fetch venues
    venues = db.query(Venue).all()

    results = []

    # 🔥 Step 3: compare with stored embeddings
    for v in venues:
        if not v.embedding:
            continue

        emb = json.loads(v.embedding)
        score = cosine_similarity(query_embedding, emb)

        results.append({
            "name": v.name,
            "category": v.category,
            "area": v.area,
            "score": float(score)
        })

    # 🔥 Step 4: sort results
    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:10]