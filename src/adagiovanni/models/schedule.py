# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
schedule

A module providing models to represent the
schedule and the items that we add to it.
"""
from typing import List

from pydantic import BaseModel


class ScheduleItem(BaseModel):
    """
    Representation of an item in the schedule
    """

    item_start_time: str
    action: str


class Schedule(BaseModel):
    """
    Representation of the schedule itself.
    """

    schedule: List[ScheduleItem]
