
import os
from pathlib import Path

from dotenv import load_dotenv

# Load the .env file from the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY", "")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")

AGENT_DATABASE_URL = os.getenv("AGENT_DATABASE_URL", "")

OVERPASS_URL = os.getenv(
    "OVERPASS_URL",
    "https://overpass-api.de/api/interpreter",
)

NOMINATIM_URL = os.getenv(
    "NOMINATIM_URL",
    "https://nominatim.openstreetmap.org",
)

MAX_VENUES_PER_SEARCH = 5000
MAX_PARALLEL_PROVIDERS = 2
