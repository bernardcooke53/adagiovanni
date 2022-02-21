from typing import Any, Dict, List

from fastapi import FastAPI

from adagiovanni import db
from adagiovanni.crud.order import read_orders

router = FastAPI()


@router.get("/schedule")
async def schedule() -> Dict[str, List[Any]]:
    client = await db.get_client()
    orders = await read_orders(client)
    return {"schedule": orders}
