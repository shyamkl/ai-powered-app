from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP
)

from sqlalchemy.sql import func

from database import Base


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