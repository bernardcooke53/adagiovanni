# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
Another nicety for checking application status;
provides a valid route at /api/v1/ping/
"""
import logging
from typing import Dict, Literal

from fastapi import APIRouter
from fastapi.logger import logger

router = APIRouter(prefix="/ping")

log = logging.getLogger(__name__)


@router.get("/", response_model=Dict[Literal["ping"], Literal["pong"]])
async def ping() -> Dict[Literal["ping"], Literal["pong"]]:
    logger.info("It's better than being pinged on Teams...")
    return {"ping": "pong"}
