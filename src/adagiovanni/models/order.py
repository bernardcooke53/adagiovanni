from pydantic import BaseModel

from adagiovanni.models._mixin import CreatedUpdatedDatesModelMixin, IdModelMixin
from adagiovanni.models.menu import Sandwich


class CustomerOrder(BaseModel):
    customer_name: str
    sandwich: Sandwich


class OrderInDb(IdModelMixin, CreatedUpdatedDatesModelMixin, CustomerOrder):

    is_complete: bool = False
    # These fields will be useful for tracking progress of orders,
    # but beyond the scope of the MVP
    # in_progress: bool = False
    # is_prepared: bool = False
    # collection_time: Optional[datetime] = None
