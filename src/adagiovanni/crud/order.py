import json
from typing import Dict, List, Optional

from bson import json_util
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from adagiovanni.core.config import MONGO_DB, ORDERS_COLLECTION_NAME
from adagiovanni.models.order import CustomerOrder, OrderInDb


async def read_orders(
    client: AsyncIOMotorClient,
    *,
    filter: Optional[Dict[str, str]] = None,
    length: Optional[int] = None,
) -> List[OrderInDb]:
    cursor = client[MONGO_DB][ORDERS_COLLECTION_NAME].find(filter)
    return [
        OrderInDb(**order)
        for order in json.loads(json_util.dumps(await cursor.to_list(length=length)))
    ]


async def place_order(
    client: AsyncIOMotorClient, customer_order: CustomerOrder
) -> OrderInDb:
    # TODO: get latest expected_completion_time from orders,
    # set order.collection_time, order.expected_completion_time to
    # max(expected_completion_time) + 2.5, + 3.5 respectively
    order = OrderInDb(**customer_order.dict())
    doc = await client[MONGO_DB][ORDERS_COLLECTION_NAME].insert_one(order.dict())
    order.id = doc.inserted_id
    order.created_date = ObjectId(order.id).generation_time
    order.updated_date = ObjectId(order.id).generation_time
    return order
