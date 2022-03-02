# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
Provides the endpoint at /api/v1/orders,
handling both get and post functionality.
"""
import logging
from typing import Dict, List, Literal

from fastapi import APIRouter
from fastapi.params import Depends

from adagiovanni.crud import order as crud_order
from adagiovanni.db import Client, get_client
from adagiovanni.models.order import CustomerOrder, OrderInDb

log = logging.getLogger(__name__)
router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=Dict[Literal["orders"], List[OrderInDb]])
async def get_orders(
    client: Client = Depends(get_client),
) -> Dict[Literal["orders"], List[OrderInDb]]:
    """
    Returns a map with one top level key,
    `"orders"`, whose value is a list of orders
    that have been submitted to the app.
    """
    return {"orders": await crud_order.read_orders(client)}


@router.post("/", response_model=OrderInDb)
async def post_order(
    order: CustomerOrder, client: Client = Depends(get_client)
) -> OrderInDb:
    """
    Place a new order by providing the customer name and
    the sandwich to order in the `customer_name` and
    `sandwich` fields of the request body, respectively.
    """
    return await crud_order.place_order(client, order)
