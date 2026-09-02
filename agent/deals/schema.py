from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class DealBase(BaseModel):
    """
    Shared fields for creating and reading deals.
    """

    venue_id: int
    title: str
    description: Optional[str] = None
    deal_type: str = "unknown"
    category: Optional[str] = None
    discount_value: Optional[str] = None
    discount_unit: Optional[str] = None
    items: list[str] = Field(default_factory=list)
    days: list[str] = Field(default_factory=list)
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    source_url: str
    source_type: str = "website"
    source_text: Optional[str] = None
    source_hash: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    is_active: bool = True
    verified_at: Optional[datetime] = None


class DealCreate(DealBase):
    """
    Data we accept when creating a deal.
    """
    pass


class DealRead(DealBase):
    """
    Data we return back to the API client.
    """

    id: int
    first_seen_at: datetime
    last_seen_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DealSourceEventBase(BaseModel):
    """
    Shared fields for source history events.
    """

    deal_id: int
    source_url: str
    source_type: str = "website"
    source_text: Optional[str] = None
    source_hash: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    status: Optional[str] = None
    verified_at: Optional[datetime] = None


class DealSourceEventCreate(DealSourceEventBase):
    pass


class DealSourceEventRead(DealSourceEventBase):
    id: int
    fetched_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)