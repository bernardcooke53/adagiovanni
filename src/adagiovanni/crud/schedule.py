import logging
from typing import Callable

from motor.motor_asyncio import AsyncIOMotorClient

from adagiovanni.core.config import SANDWICH_PREP_TIME_SECS, SANDWICH_SERVICE_TIME_SECS
from adagiovanni.crud.order import read_orders
from adagiovanni.models.schedule import Schedule, ScheduleItem

log = logging.getLogger(__name__)


async def calculate_schedule(client: AsyncIOMotorClient) -> Schedule:
    schedule = Schedule(schedule=[])
    orders_outstanding = await read_orders(
        client, filter={"is_complete": False}, sort="created_date"
    )

    repr_seconds: Callable[
        [int], str
    ] = lambda secs: f"{(secs // 60):02}:{(secs % 60):02}"

    seconds_from_now = 0
    for order in orders_outstanding:
        schedule.schedule.append(
            ScheduleItem(
                item_start_time=repr_seconds(seconds_from_now),
                action=f"Prepare sandwich for {order.customer_name} - {order.sandwich.value}",
            )
        )
        # Advance time for prep
        seconds_from_now += SANDWICH_PREP_TIME_SECS

        schedule.schedule.append(
            ScheduleItem(
                item_start_time=repr_seconds(seconds_from_now),
                action=f"Serve sandwich for {order.customer_name} - {order.sandwich.value}",
            )
        )
        # Advance time for service
        seconds_from_now += SANDWICH_SERVICE_TIME_SECS

    # Add break when orders complete
    schedule.schedule.append(
        ScheduleItem(
            item_start_time=repr_seconds(seconds_from_now),
            action="Take a break",
        )
    )

    return schedule
