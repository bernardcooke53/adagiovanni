# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
schedule

Performs the necessary I/O with the database to
find the order information and calculate the
sandwich preparation schedule based on the configured
prep and service times.
"""
import logging
from typing import Callable, List

from adagiovanni.core.config import SANDWICH_PREP_TIME_SECS, SANDWICH_SERVICE_TIME_SECS
from adagiovanni.crud import order as crud_order
from adagiovanni.db import Client
from adagiovanni.models.order import OrderInDb
from adagiovanni.models.schedule import Schedule, ScheduleItem

log = logging.getLogger(__name__)


# Abstracting this out is more testable as we can use it
# without prejudice on whether "orders" is real data
# or synthetic
def schedule_helper(
    schedule_list: List[ScheduleItem], *orders: OrderInDb
) -> List[ScheduleItem]:
    """
    Given a list of orders, calculate the schedule of
    when they should be prepared and served.
    """
    repr_seconds: Callable[
        [int], str
    ] = lambda secs: f"{(secs // 60):02}:{(secs % 60):02}"

    # Keep track of total items for calculating when
    # break time starts - avoids a call to len()
    total_items = 0
    for index, order in enumerate(orders):
        # Avoids a call to len()
        total_items = index + 1

        schedule_list.append(
            ScheduleItem(
                item_start_time=repr_seconds(
                    index * (SANDWICH_PREP_TIME_SECS + SANDWICH_SERVICE_TIME_SECS)
                ),
                action=f"Prepare sandwich for {order.customer_name} - {order.sandwich.value}",
            )
        )
        schedule_list.append(
            ScheduleItem(
                item_start_time=repr_seconds(
                    SANDWICH_PREP_TIME_SECS
                    + (index * (SANDWICH_PREP_TIME_SECS + SANDWICH_SERVICE_TIME_SECS))
                ),
                action=f"Serve sandwich for {order.customer_name} - {order.sandwich.value}",
            )
        )

    # Add break when orders complete
    schedule_list.append(
        ScheduleItem(
            item_start_time=repr_seconds(
                total_items * (SANDWICH_PREP_TIME_SECS + SANDWICH_SERVICE_TIME_SECS)
            ),
            action="Take a break",
        )
    )

    return schedule_list


async def calculate_schedule(client: Client) -> Schedule:
    """
    Retrieve the orders from the database, then pass these
    off into `schedule_helper` to apply the schedule calculation
    to them.
    """
    # N.B. `order.is_complete` is always False as we don't update it anywhere -
    # the MVP is just a projection of the upcoming schedule.
    orders_outstanding = await crud_order.read_orders(
        client, filter={"is_complete": False}, sort="created_date"
    )

    schedule = Schedule(schedule=schedule_helper([], *orders_outstanding))
    return schedule
