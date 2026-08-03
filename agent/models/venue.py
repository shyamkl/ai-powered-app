from dataclasses import dataclass, field


@dataclass
class Venue:
    """
    Standard venue model.

    Every provider converts its own JSON
    into this object.
    """

    # -----------------------------------
    # Provider information
    # -----------------------------------

    provider: str = ""
    provider_id: str = ""

    # -----------------------------------
    # Basic identity
    # -----------------------------------

    name: str = ""
    brand: str = ""
    category: str = ""

    # -----------------------------------
    # Coordinates
    # -----------------------------------

    latitude: float = 0.0
    longitude: float = 0.0

    # -----------------------------------
    # Address
    # -----------------------------------

    address: str = ""

    building: str = ""

    street: str = ""

    area: str = ""

    city: str = ""

    state: str = ""

    country: str = ""

    postcode: str = ""

    # -----------------------------------
    # Contact
    # -----------------------------------

    phone: str = ""

    website: str = ""

    email: str = ""

    # -----------------------------------
    # Business Information
    # -----------------------------------

    opening_hours: str = ""

    rating: float = 0.0

    reviews: int = 0

    price_level: str = ""

    # -----------------------------------
    # AI Fields
    # -----------------------------------

    confidence: float = 0.0

    canonical_category: str = ""

    detected_brand: str = ""

    # -----------------------------------
    # Happy Hour
    # -----------------------------------

    happy_hour: bool = False

    happy_hour_text: str = ""

    promotions: list = field(default_factory=list)

    # -----------------------------------
    # Metadata
    # -----------------------------------

    raw_categories: list = field(default_factory=list)

    source_data: dict = field(default_factory=dict)