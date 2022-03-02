# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from adagiovanni.core.config import (
    MAX_DOCUMENT_FETCH_LIMIT,
    MONGO_DB,
    ORDERS_COLLECTION_NAME,
)
from adagiovanni.db import Client
from adagiovanni.models.order import CustomerOrder, OrderInDb

log = logging.getLogger(__name__)


async def read_orders(
    client: Client,
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


async def place_order(client: Client, customer_order: CustomerOrder) -> OrderInDb:
    db = client[MONGO_DB]
    now = datetime.utcnow().replace(microsecond=0)
    order = OrderInDb(**customer_order.dict())
    order.created_date = now
    order.updated_date = now
    doc = await db[ORDERS_COLLECTION_NAME].insert_one(order.dict())
    order.id = doc.inserted_id
    return order
