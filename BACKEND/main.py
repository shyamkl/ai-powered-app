from fastapi import FastAPI, Depends, Form, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from pydantic import BaseModel

from database import Base, engine, SessionLocal
from models import Review
from models.venue import Venue
from models.review import Review
from models.favorite import Favorite
from fastapi import UploadFile, File

from routes.venues import router as venues_router

import uuid
import os

# ======================================================
# APP
# ======================================================

app = FastAPI()

# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# DATABASE
# ======================================================

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ======================================================
# UPLOADS
# ======================================================

os.makedirs("uploads", exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# ======================================================
# ROUTERS
# ======================================================

app.include_router(venues_router)

# ======================================================
# REQUEST MODELS
# ======================================================

class ChatRequest(BaseModel):
    message: str

class FavoriteRequest(BaseModel):
    venue_id: int

# ======================================================
# HOME
# ======================================================

@app.get("/")
def home():
    return {
        "message": "Backend is running"
    }

# ======================================================
# REVIEWS
# ======================================================

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

    return reviews

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

# ======================================================
# FAVORITES
# ======================================================

@app.post("/favorites")
def toggle_favorite(
    data: FavoriteRequest,
    db: Session = Depends(get_db)
):

    existing = db.query(Favorite).filter(
        Favorite.venue_id == data.venue_id
    ).first()

    # REMOVE FAVORITE
    if existing:

        db.delete(existing)
        db.commit()

        return {
            "message": "Favorite removed",
            "favorited": False
        }

    # ADD FAVORITE
    favorite = Favorite(
        venue_id=data.venue_id
    )

    db.add(favorite)
    db.commit()

    return {
        "message": "Favorite added",
        "favorited": True
    }

@app.get("/favorites")
def get_favorites(
    db: Session = Depends(get_db)
):

    favorites = db.query(Favorite).all()

    return [
        fav.venue_id
        for fav in favorites
    ]

# =========================
# CHATBOT
# =========================

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def ai_chat(
    payload: ChatRequest,
    db: Session = Depends(get_db)
):

    message = payload.message.lower().strip()

    query = db.query(Venue)

    # =========================
    # TOKENIZE USER MESSAGE
    # =========================

    words = message.split()

    # =========================
    # CATEGORY DETECTION
    # =========================

    if any(word in words for word in ["bar", "bars"]):

        query = query.filter(
            Venue.category.ilike("%bar%")
        )

    elif any(word in words for word in ["pub", "pubs"]):

        query = query.filter(
            Venue.category.ilike("%pub%")
        )

    elif any(word in words for word in ["restaurant", "restaurants", "hotel", "hotels"]):

        query = query.filter(
            Venue.category.ilike("%restaurant%")
        )

    elif any(word in words for word in ["cafe", "cafes", "coffee"]):

        query = query.filter(
            Venue.category.ilike("%cafe%")
        )

    # =========================
    # VEG FILTER
    # =========================

    if any(word in message for word in [
        "veg",
        "vegetarian",
        "pure veg"
    ]):

        query = query.filter(
            Venue.food_type.ilike("%veg%")
        )

        query = query.filter(
            ~Venue.food_type.ilike("%non%")
        )

    # =========================
    # NON VEG FILTER
    # =========================

    elif any(word in message for word in [
        "non veg",
        "nonveg",
        "chicken",
        "bbq",
        "grill",
        "biryani"
    ]):

        query = query.filter(
            or_(
                Venue.food_type.ilike("%non%"),
                Venue.food_type.ilike("%chicken%"),
                Venue.food_type.ilike("%bbq%"),
                Venue.food_type.ilike("%grill%"),
                Venue.food_type.ilike("%biryani%")
            )
        )

    # =========================
    # COCKTAIL FILTER
    # =========================

    if "cocktail" in message:

        query = query.filter(
            or_(
                Venue.drink_type.ilike("%cocktail%"),
                Venue.deal.ilike("%cocktail%")
            )
        )

    # =========================
    # PREMIUM FILTER
    # =========================

    if "premium" in message:

        query = query.filter(
            Venue.is_premium == True
        )

    # =========================
    # DYNAMIC LOCATION SEARCH
    # =========================

    ignored_words = [
        "list",
        "show",
        "find",
        "give",
        "me",
        "hotels",
        "hotel",
        "bars",
        "bar",
        "restaurants",
        "restaurant",
        "cafes",
        "cafe",
        "pubs",
        "pub",
        "in",
        "near",
        "best",
        "top",
        "vegetarian",
        "veg",
        "nonveg",
        "non",
        "premium",
        "cocktail"
    ]

    location_words = [
        word for word in words
        if word not in ignored_words
    ]

    # SEARCH EACH WORD DYNAMICALLY
    for word in location_words:

        query = query.filter(
            or_(
                Venue.city.ilike(f"%{word}%"),
                Venue.area.ilike(f"%{word}%"),
                Venue.address.ilike(f"%{word}%")
            )
        )

    # =========================
    # SORTING
    # =========================

    if "best" in message or "top" in message:

        query = query.order_by(
            Venue.rating.desc()
        )

    else:

        query = query.order_by(
            Venue.id.desc()
        )

    # =========================
    # FETCH RESULTS
    # =========================

    venues = query.limit(10).all()

    # =========================
    # NO RESULTS
    # =========================

    if not venues:

        return {
            "reply": "No matching venues found."
        }

    # =========================
    # FORMAT RESPONSE
    # =========================

    response = "🍽️ Matching venues:\n\n"

    for idx, venue in enumerate(venues, start=1):

        response += f"{idx}. {venue.name}\n"

        if venue.category:
            response += f"🍴 {venue.category}\n"

        location_parts = []

        if venue.area and str(venue.area).lower() != "nan":
            location_parts.append(venue.area)

        if venue.city and str(venue.city).lower() != "nan":
            location_parts.append(venue.city)

        if location_parts:
            response += f"📍 {', '.join(location_parts)}\n"

        elif venue.address:
            response += f"📍 {venue.address}\n"

        if venue.food_type:
            response += f"🥗 {venue.food_type}\n"

        if venue.drink_type:
            response += f"🍹 {venue.drink_type}\n"

        if venue.rating:
            response += f"⭐ {venue.rating}\n"

        if venue.deal:
            response += f"🔥 {venue.deal}\n"

        response += "\n"

    return {
        "reply": response
    }
# =========================
# UPDATE VENUE IMAGE
# =========================

@app.post("/venues/{venue_id}/upload-image")
async def upload_venue_image(
    venue_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:

        # FIND VENUE
        venue = db.query(Venue).filter(
            Venue.id == venue_id
        ).first()

        if not venue:
            return {
                "success": False,
                "message": "Venue not found"
            }

        # CREATE UPLOADS FOLDER
        os.makedirs("uploads", exist_ok=True)

        # UNIQUE FILE NAME
        filename = f"{uuid.uuid4()}_{image.filename}"

        filepath = os.path.join("uploads", filename)

        # SAVE IMAGE
        with open(filepath, "wb") as buffer:
            buffer.write(await image.read())

        # SAVE PATH TO DATABASE
        venue.local_image = f"/uploads/{filename}"

        # IMPORTANT
        db.add(venue)

        db.commit()

        db.refresh(venue)

        print("IMAGE SAVED:", venue.local_image)

        return {
            "success": True,
            "message": "Image uploaded successfully",
            "local_image": venue.local_image
        }

    except Exception as e:

        print("UPLOAD ERROR:", str(e))

        return {
            "success": False,
            "message": str(e)
        }