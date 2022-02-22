import logging
from typing import Any, Dict, List, Optional

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from adagiovanni.core.config import (
    MAX_DOCUMENT_FETCH_LIMIT,
    MONGO_DB,
    ORDERS_COLLECTION_NAME,
)
from adagiovanni.models.order import CustomerOrder, OrderInDb

log = logging.getLogger(__name__)


async def read_orders(
    client: AsyncIOMotorClient,
    *,
    filter: Optional[Dict[str, Any]] = None,
    length: Optional[int] = None,
    sort: Optional[str] = None
) -> List[OrderInDb]:
    cursor = client[MONGO_DB][ORDERS_COLLECTION_NAME].find(filter)
    if sort:
        cursor = cursor.sort(sort)
    return [
        OrderInDb(**order)
        for order in await cursor.to_list(
            length=min(length or MAX_DOCUMENT_FETCH_LIMIT, MAX_DOCUMENT_FETCH_LIMIT)
        )
    ]


async def place_order(
    client: AsyncIOMotorClient, customer_order: CustomerOrder
) -> OrderInDb:
    db = client[MONGO_DB]
    order = OrderInDb(**customer_order.dict())
    doc = await db[ORDERS_COLLECTION_NAME].insert_one(order.dict())
    order.id = doc.inserted_id
    order.created_date = ObjectId(order.id).generation_time
    order.updated_date = ObjectId(order.id).generation_time
    return order
