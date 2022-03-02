# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

import json

from tests.util import HTTPMethods, http_method_round_robin, not_found_all_methods

from adagiovanni.core.config import API_V1_PREFIX
from adagiovanni.crud.schedule import schedule_helper


def test_schedule_helper_no_orders():
    """
    Does the schedule_helper, which takes a list of orders
    and figures the schedule out based on those,
    consist of just "Take a break" if there are no orders?
    """
    assert schedule_helper([]) == [
        {"item_start_time": "00:00", "action": "Take a break"}
    ]


def test_schedule_helper_test_orders(test_order_1, test_order_2):
    """
    Does the schedule_helper, which takes a list of orders
    and figures the schedule out based on those,
    return the schedule we expect given our test orders?
    """
    expected_schedule = [
        {
            "item_start_time": "00:00",
            "action": f"Prepare sandwich for {test_order_1.customer_name} - {test_order_1.sandwich.value}",
        },
        {
            "item_start_time": "02:30",
            "action": f"Serve sandwich for {test_order_1.customer_name} - {test_order_1.sandwich.value}",
        },
        {
            "item_start_time": "03:30",
            "action": f"Prepare sandwich for {test_order_2.customer_name} - {test_order_2.sandwich.value}",
        },
        {
            "item_start_time": "06:00",
            "action": f"Serve sandwich for {test_order_2.customer_name} - {test_order_2.sandwich.value}",
        },
        {"item_start_time": "07:00", "action": "Take a break"},
    ]
    assert schedule_helper([], test_order_1, test_order_2) == expected_schedule


def test_schedule_helper_example_orders(test_example_orders):
    """
    Does the schedule_helper, which takes a list of orders
    and figures the schedule out based on those,
    return the schedule we expect given our example orders?
    """
    expected_schedule = [
        {
            "item_start_time": "00:00",
            "action": "Prepare sandwich for Stavros - BLT",
        },
        {
            "item_start_time": "02:30",
            "action": "Serve sandwich for Stavros - BLT",
        },
        {
            "item_start_time": "03:30",
            "action": "Prepare sandwich for Anisa - Egg Mayonnaise",
        },
        {
            "item_start_time": "06:00",
            "action": "Serve sandwich for Anisa - Egg Mayonnaise",
        },
        {
            "item_start_time": "07:00",
            "action": "Prepare sandwich for Adeel - Clubhouse",
        },
        {
            "item_start_time": "09:30",
            "action": "Serve sandwich for Adeel - Clubhouse",
        },
        {"item_start_time": "10:30", "action": "Take a break"},
    ]
    assert schedule_helper([], *test_example_orders) == expected_schedule


def test_api_v1_get_non_existent(test_app):
    """
    We should be getting 404 from all methods on a
    nonsense URL
    """
    return not_found_all_methods(
        test_app,
        f"{API_V1_PREFIX}/this/route/definitely/should/not/exist/and_this_is_just_to_make_sure",
    )


def test_api_v1_get_home(test_app):
    f"""
    Test GET "{API_V1_PREFIX}/"
    """
    test_map = {HTTPMethods.GET: (200, {"message": "Welcome to Giovanni's!"})}
    return http_method_round_robin(test_app, f"{API_V1_PREFIX}/", test_map)


def test_api_v1_ping(test_app):
    f"""
    Test GET "{API_V1_PREFIX}/ping/"
    """
    test_map = {HTTPMethods.GET: (200, {"message": "Welcome to Giovanni's!"})}
    test_map = {HTTPMethods.GET: (200, {"ping": "pong"})}
    return http_method_round_robin(test_app, f"{API_V1_PREFIX}/ping/", test_map)


def test_api_v1_orders(test_app, test_order_1, patch_read_orders_return):
    f"""
    Test GET "{API_V1_PREFIX}/orders/" returns 200 and the orders
    we expect, provided we patch out the function which would
    normally query the database for said orders. Also, test that
    we get 422 when trying to post with no data.
    """
    test_map = {HTTPMethods.GET: (200, {"message": "Welcome to Giovanni's!"})}
    patch_read_orders_return(test_order_1)
    expected_order = json.loads(test_order_1.json())
    order_id = expected_order.pop("id")
    expected_order["_id"] = order_id
    test_map = {
        HTTPMethods.GET: (200, {"orders": [expected_order]}),
        HTTPMethods.POST: (422, None),
    }
    return http_method_round_robin(test_app, f"{API_V1_PREFIX}/orders/", test_map)


def test_api_v1_schedule_single_order(test_app, test_order_1, patch_read_orders_return):
    f"""
    Test GET "{API_V1_PREFIX}/schedule/" returns 200 and the schedule
    we expect, provided we patch out the function which would
    normally query the database for said orders. This test patches with
    a single order.
    """
    patch_read_orders_return(test_order_1)

    expected_schedule = {"schedule": schedule_helper([], test_order_1)}
    test_map = {HTTPMethods.GET: (200, expected_schedule)}
    return http_method_round_robin(test_app, f"{API_V1_PREFIX}/schedule/", test_map)


def test_api_v1_schedule_multiple_orders(
    test_app, test_order_1, test_order_2, test_order_3, patch_read_orders_return
):
    f"""
    Test GET "{API_V1_PREFIX}/schedule/" returns 200 and the schedule
    we expect, provided we patch out the function which would
    normally query the database for said orders. This test patches with
    multiple orders.
    """
    patch_read_orders_return(test_order_1, test_order_2, test_order_3)
    test_orders = (
        test_order_1,
        test_order_2,
        test_order_3,
    )

    expected_schedule = {"schedule": schedule_helper([], *test_orders)}
    test_map = {HTTPMethods.GET: (200, expected_schedule)}
    return http_method_round_robin(test_app, f"{API_V1_PREFIX}/schedule/", test_map)


def test_api_v1_schedule_no_orders(test_app, patch_read_orders_return):
    f"""
    Test GET "{API_V1_PREFIX}/schedule/" returns 200 and the schedule
    we expect, provided we patch out the function which would
    normally query the database for said orders. This test patches with
    no orders, so we expect an immediate break.
    """
    patch_read_orders_return()
    expected_schedule = {"schedule": schedule_helper([])}
    test_map = {HTTPMethods.GET: (200, expected_schedule)}
    return http_method_round_robin(test_app, f"{API_V1_PREFIX}/schedule/", test_map)


def test_api_v1_schedule_example_orders(
    test_app, test_example_orders, patch_read_orders_return
):
    f"""
    Test GET "{API_V1_PREFIX}/schedule/" returns 200 and the schedule
    we expect, provided we patch out the function which would
    normally query the database for said orders. This test patches with
    no orders, so we expect an immediate break.
    """
    patch_read_orders_return(*test_example_orders)
    expected_schedule = {"schedule": schedule_helper([], *test_example_orders)}
    test_map = {HTTPMethods.GET: (200, expected_schedule)}
    return http_method_round_robin(test_app, f"{API_V1_PREFIX}/schedule/", test_map)
