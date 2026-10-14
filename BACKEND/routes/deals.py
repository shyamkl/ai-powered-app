from fastapi import APIRouter

from agent.database.deal_store import DealStore


router = APIRouter(
    prefix="/deals",
    tags=["deals"]
)

deal_store = DealStore()


@router.get("/{venue_id}")
def get_venue_deals(venue_id: str):
    """
    Return active deals for a venue.
    """

    deals = deal_store.get_venue_deals(
        venue_id=venue_id,
        active_only=True
    )

    return deals