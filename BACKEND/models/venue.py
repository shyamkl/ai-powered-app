from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from database import Base
from fastapi import UploadFile, File, Form
import shutil
import os
import uuid

class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    source = Column(String(255))

    lat = Column(Float)
    lon = Column(Float)

    address = Column(Text)
    is_premium = Column(Boolean, default=False)
    # ✅ ADD THESE NEW COLUMNS
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))

    category = Column(String(100))
    area = Column(String(100))

    deal = Column(Text)
    timing = Column(String(255))
    image_url = Column(Text)
    image_source = Column(String(255))
    local_image = Column(Text)
    website = Column(Text)
    wikidata = Column(Text)
    wikipedia = Column(Text)
    food_type = Column(String(100))
    drink_type = Column(String(255))
    menu_type = Column(String(255))
    rating = Column(Float)
    reviews_count = Column(Integer)

    embedding = Column(Text)