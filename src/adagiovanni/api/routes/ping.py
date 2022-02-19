from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping() -> Dict[str, str]:
    return {"message": "pong"}
