# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
menu

Though we're just serving sandwiches for the moment,
this module is designed to model whatever food
we wish to make available to order in the future.
"""
from enum import Enum


# For MVP purposes we have loaded a sample menu of
# sandwiches as an enum to demonstrate the product
class Sandwich(str, Enum):
    """
    A sample menu as an early preview,
    instead of its own collection it's a
    humble Enum for now.
    """

    def __format__(self, __format_spec: str) -> str:
        return str.__format__(self, __format_spec)

    HamAndCheese = "Ham and Cheese"
    BLT = "BLT"
    ChickenAndBacon = "Chicken and Bacon"
    Clubhouse = "Clubhouse"
    EggMayonnaise = "Egg Mayonnaise"
