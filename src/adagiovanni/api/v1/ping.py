import logging
from typing import Dict

from fastapi import APIRouter

router = APIRouter()

log = logging.getLogger(__name__)


@router.get("/ping")
async def ping() -> Dict[str, str]:
    log.info("It's better than being pinged on Teams...")
    return {"message": "pong"}
