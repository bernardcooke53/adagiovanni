from typing import List

from pydantic import BaseModel


class ScheduleItem(BaseModel):
    item_start_time: str
    action: str


class Schedule(BaseModel):
    schedule: List[ScheduleItem]
