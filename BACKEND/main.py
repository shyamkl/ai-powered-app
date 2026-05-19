from fastapi import FastAPI, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from routes import venues, search
from routes.venues import router as venues_router
from database import Base, engine
import models
from models.venue import Venue
from fastapi.staticfiles import StaticFiles
import os
import uuid
from database import SessionLocal, get_db
from models import Review
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

from fastapi import (
    FastAPI,
    Depends,
    Form,
    File,
    UploadFile
)

# ✅ FIRST create app
app = FastAPI()
os.makedirs("uploads", exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)
# app.include_router(search.router)
app.include_router(venues_router)

# ✅ THEN add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# ✅ THEN include routes
app.include_router(venues_router)
# Optional test route

@app.get("/reviews/{venue_id}")
def get_reviews(
    venue_id: int,
    db: Session = Depends(get_db)
):

    reviews = (
        db.query(Review)
        .filter(Review.venue_id == venue_id)
        .order_by(Review.created_at.desc())
        .all()
    )

    return [
        {
            "id": r.id,
            "venue_id": r.venue_id,
            "user_name": r.user_name,
            "rating": r.rating,
            "comment": r.comment,
            "image_url": r.image_url,
            "created_at": r.created_at
        }
        for r in reviews
    ]
 
@app.post("/reviews")
async def create_review(
    venue_id: int = Form(...),
    user_name: str = Form(...),
    rating: int = Form(...),
    comment: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    image_path = None

    if image:

        filename = f"{uuid.uuid4()}_{image.filename}"

        filepath = f"uploads/{filename}"

        with open(filepath, "wb") as f:
            f.write(await image.read())

        image_path = f"/uploads/{filename}"

    review = Review(
        venue_id=venue_id,
        user_name=user_name,
        rating=rating,
        comment=comment,
        image_url=image_path
    )

    db.add(review)

    db.commit()

    db.refresh(review)

    return {
        "message": "Review added successfully"
    }

@app.get("/")
def home():
    return {"message": "Backend is running"}