# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

import logging
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

import adagiovanni.crud.order
from adagiovanni.main import app
from adagiovanni.models._mixin import PyObjectId
from adagiovanni.models.menu import Sandwich
from adagiovanni.models.order import OrderInDb

log = logging.getLogger(__name__)


@pytest.fixture
def test_order_1():
    yield OrderInDb(
        sandwich=Sandwich.HamAndCheese,
        customer_name="Ms Test Customer",
        _id=PyObjectId(),
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow(),
        is_complete=False,
    )


@pytest.fixture
def test_order_2():
    yield OrderInDb(
        sandwich=Sandwich.EggMayonnaise,
        customer_name="Miss Test Customer 2",
        _id=PyObjectId(),
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow(),
        is_complete=False,
    )


@pytest.fixture
def test_order_3():
    yield OrderInDb(
        sandwich=Sandwich.BLT,
        customer_name="Mr Test Customer 3",
        _id=PyObjectId(),
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow(),
        is_complete=False,
    )


@pytest.fixture
def test_example_orders():
    stavros_order = OrderInDb(
        sandwich=Sandwich.BLT,
        customer_name="Stavros",
        _id=PyObjectId(),
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow(),
        is_complete=False,
    )
    anisa_order = OrderInDb(
        sandwich=Sandwich.EggMayonnaise,
        customer_name="Anisa",
        _id=PyObjectId(),
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow(),
        is_complete=False,
    )
    adeel_order = OrderInDb(
        sandwich=Sandwich.Clubhouse,
        customer_name="Adeel",
        _id=PyObjectId(),
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow(),
        is_complete=False,
    )
    yield stavros_order, anisa_order, adeel_order


@pytest.fixture
def patch_read_orders_return(monkeypatch):
    def _mock_read_orders(*test_orders):
        async def read_orders(
            client,
            *,
            filter=None,
            length=None,
            sort=None,
        ):
            return [*test_orders]

        monkeypatch.setattr(adagiovanni.crud.order, "read_orders", read_orders)
        return read_orders

    return _mock_read_orders


@pytest.fixture
def test_app():
    yield TestClient(app())
