# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
order

This module contains two models - one for incoming orders
from the customer, and one for orders that we load back out
of the database.
"""
from pydantic import BaseModel

from adagiovanni.models._mixin import CreatedUpdatedDatesModelMixin, IdModelMixin
from adagiovanni.models.menu import Sandwich


class CustomerOrder(BaseModel):
    """
    The required fields for an inbound order
    from a customer.
    """

    customer_name: str
    sandwich: Sandwich


class OrderInDb(IdModelMixin, CreatedUpdatedDatesModelMixin, CustomerOrder):
    """
    The order information that we retrieve from the database.
    """

    is_complete: bool = False

    # These fields will be useful for tracking progress of orders,
    # but beyond the scope of the MVP
    # in_progress: bool = False
    # is_prepared: bool = False
    # collection_time: Optional[datetime] = None
