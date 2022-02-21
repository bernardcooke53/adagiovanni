from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from adagiovanni.models._mixin import CreatedUpdatedDatesModelMixin, IdModelMixin
from adagiovanni.models.menu import Sandwich


class CustomerOrder(BaseModel):
    customer_name: str
    sandwich: Sandwich


class OrderInDb(CreatedUpdatedDatesModelMixin, IdModelMixin, CustomerOrder):
    in_progress: bool = False
    is_complete: bool = False
    collection_time: Optional[datetime] = None
    expected_completion_time: Optional[datetime] = None
