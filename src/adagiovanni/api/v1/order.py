from typing import Dict, List

from fastapi import APIRouter

from adagiovanni.crud.order import place_order, read_orders
from adagiovanni.db import get_client
from adagiovanni.models.order import CustomerOrder, OrderInDb

router = APIRouter()


@router.get("/orders", response_model=Dict[str, List[OrderInDb]])
async def get_orders() -> Dict[str, List[OrderInDb]]:
    client = await get_client()
    return {"orders": await read_orders(client)}


@router.post("/order", response_model=OrderInDb)
async def post_order(order: CustomerOrder) -> OrderInDb:
    client = await get_client()
    return await place_order(client, order)
