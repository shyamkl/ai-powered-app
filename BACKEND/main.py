from fastapi import FastAPI, Depends, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from sqlalchemy import or_

from pydantic import BaseModel

from database import Base, engine, get_db
from models import Review

from routes.venues import router as venues_router
from models.venue import Venue


import uuid
import os

# =========================
# APP SETUP
# =========================

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATABASE
# =========================

Base.metadata.create_all(bind=engine)

# =========================
# UPLOADS
# =========================

os.makedirs("uploads", exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# =========================
# ROUTERS
# =========================

app.include_router(venues_router)

# =========================
# OPENAI
# =========================



# =========================
# CHAT MODEL
# =========================

class ChatRequest(BaseModel):
    message: str

# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {
        "message": "Backend is running"
    }

# =========================
# CHAT ENDPOINT
# =========================


   

# =========================
# GET REVIEWS
# =========================

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

# =========================
# CREATE REVIEW
# =========================

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

@app.post("/chat")
async def ai_chat(
    payload: dict,
    db: Session = Depends(get_db)
):

    message = payload.get("message", "").lower().strip()

    # -------------------------
    # GREETING HANDLING
    # -------------------------

    greetings = [
        "hi",
        "hello",
        "hey",
        "hii",
        "good morning",
        "good evening"
    ]

    if message in greetings:

        return {
            "reply": (
                "👋 Hi! I'm your AI venue assistant.\n\n"
                "You can ask me things like:\n"
                "• Vegetarian restaurants in Chennai\n"
                "• Bars in Mumbai\n"
                "• Rooftop cafes in Bangalore\n"
                "• Premium restaurants near Bandra"
            )
        }

    query = db.query(Venue)

    # -------------------------
    # CITY DETECTION
    # -------------------------

    cities = [
        "chennai",
        "mumbai",
        "bangalore",
        "kochi",
        "delhi",
        "hyderabad",
        "pune"
    ]

    detected_city = None

    for city in cities:
        if city in message:
            detected_city = city
            break

    if detected_city:
        query = query.filter(
            Venue.city.ilike(f"%{detected_city}%")
        )

    # -------------------------
    # AREA DETECTION
    # -------------------------

    areas = [
        "royapuram",
        "bandra",
        "juhu",
        "andheri",
        "adyar",
        "koramangala",
        "fort kochi"
    ]

    detected_area = None

    for area in areas:
        if area in message:
            detected_area = area
            break

    if detected_area:
        query = query.filter(
            Venue.area.ilike(f"%{detected_area}%")
        )

    # -------------------------
    # VEG FILTER
    # -------------------------

    if "vegetarian" in message or "veg" in message:

        query = query.filter(
            (
                Venue.category.ilike("%veg%")
            ) |
            (
                Venue.food_type.ilike("%veg%")
            ) |
            (
                Venue.name.ilike("%veg%")
            )
        )
        # -------------------------
        # NON VEG FILTER
        # -------------------------

    elif (
        "non veg" in message
        or "nonveg" in message
        or "chicken" in message
        or "biryani" in message
        or "grill" in message
        or "bbq" in message
    ):

        query = query.filter(
            (
                Venue.food_type.ilike("%non%")
            ) |
            (
                Venue.food_type.ilike("%chicken%")
            ) |
            (
                Venue.food_type.ilike("%biryani%")
            ) |
            (
                Venue.food_type.ilike("%bbq%")
            ) |
            (
                Venue.food_type.ilike("%grill%")
            ) |
            (
                Venue.category.ilike("%non%")
            )
        )

    # -------------------------
    # PUB / BAR FILTER
    # -------------------------

    if (
        "pub" in message
        or "bar" in message
        or "nightclub" in message
        or "club" in message
    ):

        query = query.filter(
            or_(
                Venue.category.ilike("%pub%"),
                Venue.category.ilike("%bar%"),
                Venue.category.ilike("%club%"),
                Venue.name.ilike("%pub%"),
                Venue.name.ilike("%bar%")
            )
        )
    # -------------------------
    # HOTEL / RESTAURANT FILTER
    # -------------------------

    elif (
        "restaurant" in message
        or "hotel" in message
        or "cafe" in message
    ):

        query = query.filter(
            (
                Venue.category.ilike("%restaurant%")
            ) |
            (
                Venue.category.ilike("%hotel%")
            ) |
            (
                Venue.category.ilike("%cafe%")
            )
        )

    # -------------------------
    # GET RESULTS
    # -------------------------

    venues = query.limit(5).all()

    if not venues:

        return {
            "reply": (
                "😔 Sorry, I couldn't find matching venues.\n\n"
                "Try searching like:\n"
                "• Veg restaurants in Chennai\n"
                "• Bars in Mumbai\n"
                "• Cafes in Bangalore"
            )
        }

    # -------------------------
    # FORMAT RESPONSE
    # -------------------------

    response_text = "🍽️ Here are some places I found:\n\n"

    for idx, venue in enumerate(venues, start=1):

        response_text += (
            f"{idx}. {venue.name}\n"
            f"📍 {venue.area or 'Area not available'}, "
            f"{venue.city or 'City not available'}\n"
        )

        if venue.category:
            response_text += f"🍴 {venue.category}\n"

        if venue.deal:
            response_text += f"🔥 {venue.deal}\n"

        response_text += "\n"

    return {
        "reply": response_text
    }