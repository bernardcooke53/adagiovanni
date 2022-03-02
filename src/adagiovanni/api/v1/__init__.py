# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
Import all the routers to the `adagiovanni.api.v1` namespace
for easier access.
"""
from adagiovanni.api.v1.home import router as home_router
from adagiovanni.api.v1.order import router as order_router
from adagiovanni.api.v1.ping import router as ping_router
from adagiovanni.api.v1.schedule import router as schedule_router
