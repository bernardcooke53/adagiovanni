from fastapi import APIRouter

from adagiovanni import db
from adagiovanni.crud.schedule import calculate_schedule
from adagiovanni.models.schedule import Schedule

router = APIRouter()


@router.get("/schedule")
async def get_schedule() -> Schedule:
    client = await db.get_client()
    return await calculate_schedule(client)
