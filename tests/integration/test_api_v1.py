# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
Integration tests for adagiovanni API v1

See tests/integration/conftest.py - even though test_db_client
is unused where it's requested as a fixture, it's required due
to a bug in how the mongo client looks for an event loop when
this is being run by pytest
"""
import json
import logging

from fastapi import status

from adagiovanni.core.config import API_V1_PREFIX
from adagiovanni.crud.schedule import schedule_helper
from adagiovanni.models.order import OrderInDb

log = logging.getLogger(__name__)


def test_submit_order(test_app, test_db_client, random_customer_order):
    f"""
    After posting an order to {API_V1_PREFIX}/orders/, does
    GET {API_V1_PREFIX}/orders/ return the new order too?
    """
    current_orders_response = test_app.get(f"{API_V1_PREFIX}/orders/")
    assert current_orders_response.status_code == status.HTTP_200_OK
    current_orders = current_orders_response.json()
    assert "orders" in current_orders.keys()
    existing_orders = current_orders["orders"]

    # Submit new order
    order_in_db_response = test_app.post(
        f"{API_V1_PREFIX}/orders/", json=json.loads(random_customer_order.json())
    )
    assert order_in_db_response.status_code == status.HTTP_200_OK
    order_in_db = order_in_db_response.json()
    assert order_in_db["customer_name"] == random_customer_order.customer_name
    assert order_in_db["sandwich"] == random_customer_order.sandwich.value

    new_orders_response = test_app.get(f"{API_V1_PREFIX}/orders/")
    assert new_orders_response.status_code == status.HTTP_200_OK

    new_orders = new_orders_response.json()
    assert "orders" in new_orders.keys()
    assert all(
        order in [*existing_orders, order_in_db] for order in new_orders["orders"]
    )
    assert all(
        order in new_orders["orders"] for order in [*existing_orders, order_in_db]
    )


def test_schedule(test_app, test_db_client):
    """
    Does /schedule return what we expect based on the
    orders present in the DB?
    """
    current_orders_response = test_app.get(f"{API_V1_PREFIX}/orders/")
    assert current_orders_response.status_code == status.HTTP_200_OK
    current_orders = current_orders_response.json()
    assert "orders" in current_orders.keys()
    existing_orders = map(lambda o: OrderInDb(**o), current_orders["orders"])
    expected_schedule = {"schedule": schedule_helper([], *existing_orders)}

    # Get schedule
    actual_schedule_response = test_app.get(f"{API_V1_PREFIX}/schedule/")
    assert actual_schedule_response.status_code == status.HTTP_200_OK
    actual_schedule = actual_schedule_response.json()
    assert actual_schedule == expected_schedule


def test_submit_new_order_schedule_update(
    test_app, test_db_client, random_customer_order
):
    f"""
    Does posting a new order to {API_V1_PREFIX}/orders/ correctly
    update the response at {API_V1_PREFIX}/schedule/ as we expect?
    """
    # Submit new order
    order_in_db_response = test_app.post(
        f"{API_V1_PREFIX}/orders/", json=json.loads(random_customer_order.json())
    )
    assert order_in_db_response.status_code == status.HTTP_200_OK
    order_in_db = order_in_db_response.json()
    assert order_in_db["customer_name"] == random_customer_order.customer_name
    assert order_in_db["sandwich"] == random_customer_order.sandwich.value

    # Get the orders
    current_orders_response = test_app.get(f"{API_V1_PREFIX}/orders/")
    assert current_orders_response.status_code == status.HTTP_200_OK
    current_orders = current_orders_response.json()
    assert "orders" in current_orders.keys()
    existing_orders = map(lambda o: OrderInDb(**o), current_orders["orders"])

    expected_new_schedule = {"schedule": schedule_helper([], *existing_orders)}

    # Get the new schedule from the app
    new_schedule_response = test_app.get(f"{API_V1_PREFIX}/schedule/")
    assert new_schedule_response.status_code == status.HTTP_200_OK
    new_schedule = new_schedule_response.json()
    assert new_schedule == expected_new_schedule
