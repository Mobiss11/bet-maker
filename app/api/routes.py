from fastapi import APIRouter
from .endpoints import events, bets

router = APIRouter()
router.include_router(events.router, tags=["events"])
router.include_router(bets.router, tags=["bets"])
