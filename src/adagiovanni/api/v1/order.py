from typing import Any, Dict, List

from fastapi import APIRouter

from adagiovanni.crud.order import place_order, read_orders
from adagiovanni.db import get_client
from adagiovanni.models.order import CustomerOrder

router = APIRouter()


@router.get("/orders")
async def get_orders() -> Dict[str, List[Any]]:
    client = await get_client()
    return {"orders": await read_orders(client)}


@router.post("/order")
async def post_order(order: CustomerOrder) -> Dict[str, str]:
    client = await get_client()
    order_in_db = await place_order(client, order)

    return {
        "message": "Your order has been placed!",
        "collection_time": "None"
        if order_in_db.collection_time is None
        else order_in_db.collection_time.strftime("%Y-%m-%d %H:%M:%S"),
    }
