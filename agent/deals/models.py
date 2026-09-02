from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    DateTime,
    func,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models in this module.

    SQLAlchemy uses this class to discover our models
    and build their database table definitions.
    """

    pass


class Deal(Base):
    """
    Main table containing normalized happy-hour and
    promotional deals.
    """

    __tablename__ = "ai_deals"

    # -------------------------------------------------
    # Primary key
    # -------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # -------------------------------------------------
    # Venue
    # -------------------------------------------------

    venue_id: Mapped[int] = mapped_column(
        Integer,
        index=True,
        nullable=False,
    )

    # -------------------------------------------------
    # Deal identity
    # -------------------------------------------------

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Example:
    # happy-hour
    # bogo
    # percentage_discount
    # fixed_price

    deal_type: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        default="unknown",
    )

    # Example:
    # drinks
    # food
    # cocktails
    # beer
    # dessert

    category: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True,
    )

    # Example:
    # "50"
    # "2"
    # "10"

    discount_value: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    # Example:
    # %
    # off
    # free

    discount_unit: Mapped[Optional[str]] = mapped_column(
        String(30),
        nullable=True,
    )

    # JSON list of items mentioned in the deal.
    #
    # Example:
    # ["cocktails", "beer"]

    items: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    # JSON list of applicable days.
    #
    # Example:
    # ["Friday", "Saturday"]

    days: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    # We initially store time as strings because
    # websites can use many different formats.
    #
    # Examples:
    # "5 PM"
    # "17:00"
    # "17.00"

    start_time: Mapped[Optional[str]] = mapped_column(
        String(16),
        nullable=True,
    )

    end_time: Mapped[Optional[str]] = mapped_column(
        String(16),
        nullable=True,
    )

    # -------------------------------------------------
    # Source information
    # -------------------------------------------------

    source_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    source_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="website",
    )

    # Original text extracted from the website,
    # poster, menu, OCR, etc.

    source_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Hash of the source content.
    #
    # Used to detect whether the same source content
    # was seen before.

    source_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
    )

    # -------------------------------------------------
    # AI / verification information
    # -------------------------------------------------

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    # -------------------------------------------------
    # Timestamps
    # -------------------------------------------------

    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # -------------------------------------------------
    # Relationship to source history
    # -------------------------------------------------

    source_events: Mapped[list["DealSourceEvent"]] = relationship(
        "DealSourceEvent",
        back_populates="deal",
        cascade="all, delete-orphan",
    )


class DealSourceEvent(Base):
    """
    Stores the history of every crawl or verification
    event associated with a deal.
    """

    __tablename__ = "ai_deal_source_events"

    # -------------------------------------------------
    # Primary key
    # -------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # -------------------------------------------------
    # Relationship to Deal
    # -------------------------------------------------

    deal_id: Mapped[int] = mapped_column(
        ForeignKey(
            "ai_deals.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # -------------------------------------------------
    # Source information
    # -------------------------------------------------

    source_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    source_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="website",
    )

    # What the crawler/OCR/LLM saw at that time.

    source_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Hash of the exact source snapshot.

    source_hash: Mapped[str] = mapped_column(
        String(64),
        index=True,
        nullable=False,
    )

    # AI confidence for this particular event.

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    # Example:
    # success
    # failed
    # changed
    # verified

    status: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    # When the source was fetched.

    fetched_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    # When this particular event was verified.

    verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    # -------------------------------------------------
    # Back relationship to Deal
    # -------------------------------------------------

    deal: Mapped["Deal"] = relationship(
        "Deal",
        back_populates="source_events",
    )