from typing import Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home() -> Dict[str, str]:
    return {"message": "Welcome to Giovanni's!"}
