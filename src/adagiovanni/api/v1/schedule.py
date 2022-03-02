# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
Provides the endpoint at /api/v1/schedule/,
which allows visibility over the schedule based
on the orders that have been submitted.
"""
from fastapi import APIRouter
from fastapi.params import Depends

from adagiovanni.crud import schedule as crud_schedule
from adagiovanni.db import Client, get_client
from adagiovanni.models.schedule import Schedule

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.get("/", response_model=Schedule)
async def get_schedule(client: Client = Depends(get_client)) -> Schedule:
    """
    Get the sandwich preparation schedule information
    based on the orders that have been submitted.
    """
    return await crud_schedule.calculate_schedule(client)
