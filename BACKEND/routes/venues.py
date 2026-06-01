from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.review import Review
import os
import uuid

from fastapi import (
    UploadFile,
    File,
    HTTPException
)



from database import get_db


from database import SessionLocal
from models.venue import Venue

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/venues")
def get_venues(
    page: int = 1,
    limit: int = 50,

    country: str = None,
    state: str = None,
    city: str = None,
    area: str = None,
    search: str = None,
    category: str = None,

    food_type: str = None,
    drink_type: str = None,
    menu_type: str = None,

    premium_only: bool = False,
    

    db: Session = Depends(get_db)
):

    query = db.query(Venue)

    print("TOTAL VENUES:", db.query(Venue).count())

    bangkok_count = db.query(Venue).filter(
        Venue.city == "Bangkok"
    ).count()

    print("BANGKOK COUNT:", bangkok_count)

    thailand_count = db.query(Venue).filter(
        Venue.country == "Thailand"
    ).count()

    print("THAILAND COUNT:", thailand_count)

    print("COUNTRY:", country)
    print("STATE:", state)
    print("CITY:", city)
    print("AREA:", area)
    print("CATEGORY:", category)
    # print(
    #         db.query(Venue.city).distinct().limit(30).all()
    #     )

    # print(
    #         db.query(Venue.category).distinct().limit(30).all()
    #     )

    # print(
    #         db.query(Venue.area).distinct().limit(30).all()
    #     )
    # print(
    #         db.query(Venue.state).distinct().limit(30).all()
    #     )
    # COUNTRY FILTER


    # COUNTRY
    if country:
        query = query.filter(Venue.country == country)

    if state:
        query = query.filter(Venue.state == state)

    if city:
        query = query.filter(Venue.city == city)

    if area:
        query = query.filter(
        Venue.area.ilike(f"%{area}%") |
        (Venue.address.ilike(f"%{area}%"))
    )
        
    if search:
        query = query.filter(
        Venue.name.ilike(f"%{search}%")
    )
        
    if category:
        query = query.filter(
        func.lower(Venue.category) == category.lower()
    )

    if food_type:
        query = query.filter(Venue.food_type == food_type)

    if drink_type:
        query = query.filter(Venue.drink_type == drink_type)

    if menu_type:
        query = query.filter(Venue.menu_type == menu_type)

    if premium_only:
        query = query.filter(Venue.is_premium == True)


    print("COUNTRY:", country)
    print("CITY:", city)
    print("AREA:", area)
    print("CATEGORY:", category)
    # PAGINATION
    offset = (page - 1) * limit

    print(
    query.statement.compile(
        compile_kwargs={"literal_binds": True}
    )
)
    print("FINAL COUNTRY =", repr(country))
    print("FINAL STATE =", repr(state))
    print("FINAL CITY =", repr(city))
    print("FINAL AREA =", repr(area))
    print("FINAL CATEGORY =", repr(category))
    print(str(query))
    venues = query.offset(offset).limit(limit).all()

   

    result = []

    for v in venues:

        reviews = (
            db.query(Review)
            .filter(Review.venue_id == v.id)
            .all()
        )

        if reviews:
                highest_rating = max(r.rating for r in reviews)
                reviews_count = len(reviews)
        else:
                highest_rating = None
                reviews_count = 0

        result.append({
                "id": v.id,
                "name": v.name,

                "category": v.category,

                "image_url": v.image_url,
                "local_image": v.local_image,

                "address": v.address,

                "city": v.city,
                "state": v.state,
                "country": v.country,

                "area": v.area,

                "deal": v.deal,
                "timing": v.timing,

                "food_type": v.food_type,
                "menu_type": v.menu_type,
                "drink_type": v.drink_type,

                "is_premium": v.is_premium,

                # REAL REVIEW DATA
                "rating": highest_rating,
                "reviews_count": reviews_count,

                "lat": v.lat,
                "lon": v.lon
        })

    return result

@router.put("/venues/{venue_id}/image")
async def update_venue_image(
    venue_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    venue = db.query(Venue).filter(
        Venue.id == venue_id
    ).first()

    if not venue:
        raise HTTPException(
            status_code=404,
            detail="Venue not found"
        )

    os.makedirs("uploads", exist_ok=True)

    extension = image.filename.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}"

    filepath = os.path.join("uploads", filename)

    with open(filepath, "wb") as f:
        f.write(await image.read())

    # IMPORTANT
    venue.local_image = f"/uploads/{filename}"
    
    db.commit()

    db.refresh(venue)

    return {
        "message": "Image uploaded successfully",
        "local_image": venue.local_image
    }