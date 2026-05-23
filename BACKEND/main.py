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
# CHAT REQUEST MODEL
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

# =========================
# CHATBOT
# =========================

@app.post("/chat")
async def ai_chat(
    payload: ChatRequest,
    db: Session = Depends(get_db)
):

    message = payload.message.lower().strip()

    # =========================
    # GREETINGS
    # =========================

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
                "Try asking:\n"
                "• Vegetarian restaurants in Bangkok\n"
                "• Bars in Mumbai\n"
                "• Pubs in Chennai\n"
                "• Cafes in Bangalore\n"
                "• Premium bars in Chennai\n"
                "• Cocktail bars in Bangkok"
            )
        }

    query = db.query(Venue)

    # =========================
    # CATEGORY DETECTION
    # =========================

    category_keywords = {
        "bar": ["bar", "bars"],
        "pub": ["pub", "pubs"],
        "restaurant": ["restaurant", "restaurants"],
        "cafe": ["cafe", "cafes", "coffee"],
        "lounge": ["lounge", "lounges"],
        "club": ["club", "clubs"]
    }

    detected_category = None

    for category, words in category_keywords.items():

        if any(word in message for word in words):
            detected_category = category
            break

    # =========================
    # VEG / NONVEG
    # =========================

    veg_search = any(word in message for word in [
        "veg",
        "vegetarian",
        "pure veg"
    ])

    nonveg_search = any(word in message for word in [
        "non veg",
        "nonveg",
        "chicken",
        "biryani",
        "bbq",
        "grill"
    ])

    # =========================
    # PREMIUM
    # =========================

    premium_only = "premium" in message

    # =========================
    # CITY FILTER
    # =========================

    known_cities = [
        "bangkok",
        "mumbai",
        "chennai",
        "bangalore",
        "kochi",
        "delhi",
        "hyderabad",
        "pune",
        "kolkata"
    ]

    detected_city = None

    for city in known_cities:

        if city in message:
            detected_city = city
            break

    if detected_city:

        query = query.filter(
            Venue.city.ilike(f"%{detected_city}%")
        )

    # =========================
    # AREA FILTER
    # =========================

    known_areas = [
        "sukhumvit",
        "powai",
        "royapuram",
        "bandra",
        "juhu",
        "andheri",
        "adyar",
        "koramangala",
        "fort kochi",
        "t nagar",
        "velachery",
        "indiranagar",
        "sathorn"
    ]

    detected_area = None

    for area in known_areas:

        if area in message:
            detected_area = area
            break

    if detected_area:

        query = query.filter(
            or_(
                Venue.area.ilike(f"%{detected_area}%"),
                Venue.address.ilike(f"%{detected_area}%")
            )
        )

    # =========================
    # FLEXIBLE CATEGORY FILTER
    # =========================

    if detected_category == "bar":

        query = query.filter(
            or_(
                Venue.category.ilike("%bar%"),
                Venue.category.ilike("%pub%"),
                Venue.category.ilike("%lounge%"),
                Venue.name.ilike("%bar%")
            )
        )

    elif detected_category == "pub":

        query = query.filter(
            or_(
                Venue.category.ilike("%pub%"),
                Venue.category.ilike("%bar%")
            )
        )

    elif detected_category == "restaurant":

        query = query.filter(
            or_(
                Venue.category.ilike("%restaurant%"),
                Venue.category.ilike("%hotel%"),
                Venue.category.ilike("%dining%")
            )
        )

    elif detected_category == "cafe":

        query = query.filter(
            Venue.category.ilike("%cafe%")
        )

    # =========================
    # VEG FILTER
    # =========================

    if veg_search:

        query = query.filter(
            Venue.food_type.ilike("%veg%")
        )

        query = query.filter(
            ~Venue.food_type.ilike("%non%")
        )

    # =========================
    # NONVEG FILTER
    # =========================

    if nonveg_search:

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

    if "cocktail" in message or "cocktails" in message:

        query = query.filter(
            or_(
                Venue.drink_type.ilike("%cocktail%"),
                Venue.deal.ilike("%cocktail%")
            )
        )

    # =========================
    # BUY ONE GET ONE FILTER
    # =========================

    if (
        "buy one get one" in message
        or "buy 1 get 1" in message
        or "bogo" in message
    ):

        query = query.filter(
            or_(
                Venue.deal.ilike("%buy%"),
                Venue.deal.ilike("%1+1%"),
                Venue.deal.ilike("%free%")
            )
        )

    # =========================
    # PREMIUM FILTER
    # =========================

    if premium_only:

        query = query.filter(
            Venue.is_premium == True
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
            "reply": (
                "😔 Sorry, I couldn't find matching venues.\n\n"
                "Try searches like:\n"
                "• Vegetarian restaurants in Bangkok\n"
                "• Bars in Mumbai\n"
                "• Cocktail bars in Chennai\n"
                "• Cafes in Bangalore"
            )
        }

    # =========================
    # FORMAT RESPONSE
    # =========================

    response = "🍽️ Here are some places I found:\n\n"

    for idx, venue in enumerate(venues, start=1):

        response += f"{idx}. {venue.name}\n"

        location_parts = []

        # CLEAN AREA
        if (
            venue.area
            and str(venue.area).lower() != "nan"
            and str(venue.area).lower() != "none"
        ):
            location_parts.append(venue.area.strip())

        # CLEAN CITY
        if (
            venue.city
            and str(venue.city).lower() != "nan"
            and str(venue.city).lower() != "none"
        ):
            location_parts.append(venue.city.strip())

        # FALLBACK TO ADDRESS
        if (
            not location_parts
            and venue.address
            and str(venue.address).lower() != "nan"
            and str(venue.address).lower() != "none"
        ):
            if location_parts:
                response += f"📍 {', '.join(location_parts)}\n"
            else:
                response += "📍 Location unavailable\n"
            location_parts.append(venue.address.strip())

            if venue.category:
                response += f"🍴 {venue.category}\n"

            if venue.food_type:
                response += f"🥗 {venue.food_type}\n"

            if venue.drink_type:
                response += f"🍹 {venue.drink_type}\n"

            if venue.rating:location
            response += f"⭐ {venue.rating}\n"

            if venue.deal:
                response += f"🔥 {venue.deal}\n"

            response += "\n"

        return {
            "reply": response
        }