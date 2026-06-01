from sqlalchemy import Column, Integer
from database import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, nullable=False)