from sqlalchemy import Column, Integer, String, Float, Text, TIMESTAMP
from database import Base
from sqlalchemy.sql import func


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    venue_id = Column(Integer)

    user_name = Column(String(255))

    rating = Column(Integer)

    comment = Column(Text)

    image_url = Column(Text)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )
class Venue(Base):
    __tablename__ = "venues"
   
    id = Column(Integer, primary_key=True, index=True)

    # Core data
    name = Column(String(255))
    source = Column(String(255))
    lat = Column(Float)
    lon = Column(Float)
    address = Column(Text)
    country = Column(String(100), nullable=True),
    state = Column(String(100), nullable=True),
    city = Column(String(100), nullable=True)
    
    # Business info
    category = Column(String(100))
    area = Column(String(100))
    deal = Column(Text)
    timing = Column(String(255))

    # Media
    image_url = Column(Text)
    image_source = Column(String(255))
    local_image = Column(String(255))

    # External links
    website = Column(String(255))
    wikidata = Column(String(255))
    wikipedia = Column(String(255))

    # 🔥 AI-ready fields
    rating = Column(Float)              # future scoring
    reviews_count = Column(Integer)     # popularity
    embedding = Column(Text)            # vector (store JSON string)