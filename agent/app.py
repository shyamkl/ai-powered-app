from fastapi import FastAPI
from contextlib import asynccontextmanager

from providers.provider_manager import ProviderManager
from geocoder import reverse_geocode
from scheduler.crawler import BackgroundCrawler


# -----------------------------------
# Create manager
# -----------------------------------

manager = ProviderManager()

crawler = BackgroundCrawler(manager)


# -----------------------------------
# Lifespan
# -----------------------------------

@asynccontextmanager
async def lifespan(app):

    print("Starting background crawler...")

    crawler.start()

    yield

    print("Stopping background crawler...")

    crawler.stop()


# -----------------------------------
# Create FastAPI app
# -----------------------------------

app = FastAPI(
    lifespan=lifespan
)


# -----------------------------------
# Routes
# -----------------------------------

@app.get("/")
def home():
    return {
        "status": "Agent Running"
    }


import time

@app.get("/nearby")
def nearby(lat: float, lon: float):

    t0 = time.time()

    venues = manager.search(lat, lon)

    t1 = time.time()

    print("Search time:", round(t1 - t0, 3), "seconds")

    return {
        "count": len(venues),
        "venues": venues
    }