# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
Provides a default endpoint at /api/v1/,
a nicety so that we don't get an immediate 404
"""
from typing import Dict, Literal

from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    response_model=Dict[
        Literal["message"],
        Literal["Welcome to Giovanni's!"],
    ],
)
async def home() -> Dict[
    Literal["message"],
    Literal["Welcome to Giovanni's!"],
]:
    return {"message": "Welcome to Giovanni's!"}
