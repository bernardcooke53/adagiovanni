# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

import asyncio
import random
import string
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

import adagiovanni.db
from adagiovanni.core.config import (
    MAX_MONGO_CONNECTION_POOL_SIZE,
    MIN_MONGO_CONNECTION_POOL_SIZE,
    MONGO_URL,
)
from adagiovanni.main import app
from adagiovanni.models._mixin import PyObjectId
from adagiovanni.models.menu import Sandwich
from adagiovanni.models.order import CustomerOrder, OrderInDb


# This whole thing is a workaround for pytest
# not being able to use the mongo client on an
# open event loop - see:
# https://github.com/tiangolo/fastapi/issues/4473
# https://github.com/encode/starlette/issues/1315
#
# Tests can request the "test_db_client" fixture and
# then they will work with pytest
def mock_db_client():
    _client = adagiovanni.db.Client(
        str(MONGO_URL),
        minPoolSize=MIN_MONGO_CONNECTION_POOL_SIZE,
        maxPoolSize=MAX_MONGO_CONNECTION_POOL_SIZE,
    )

    # This next line allows the mongo client
    # to find the correct running event loop
    # during the tests.
    _client.get_io_loop = asyncio.get_event_loop
    return _client


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
def random_test_order():
    yield OrderInDb(
        sandwich=random.choice(list(Sandwich)),
        customer_name="".join(random.choice(string.ascii_letters) for _ in range(20)),
        _id=PyObjectId(),
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow(),
        is_complete=False,
    )


@pytest.fixture
def random_customer_order():
    yield CustomerOrder(
        sandwich=random.choice(list(Sandwich)),
        customer_name="".join(random.choice(string.ascii_letters) for _ in range(20)),
    )


@pytest.fixture
def test_db_client(monkeypatch):
    client = mock_db_client()
    monkeypatch.setattr(adagiovanni.db, "_client", client)


@pytest.fixture(scope="module")
def test_app():
    test_app_instance = app()
    test_app_instance.dependency_overrides[adagiovanni.db.get_client] = mock_db_client
    yield TestClient(test_app_instance)
