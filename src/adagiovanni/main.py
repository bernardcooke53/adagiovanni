# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
Main entry point for the application.

Provides an `app` factory function for
creating the FastAPI instance.
"""
import logging
import logging.config
import pathlib

import yaml
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

import adagiovanni.api.v1 as api_v1
from adagiovanni import db
from adagiovanni.core.config import API_V1_PREFIX

HERE = pathlib.Path(__file__).parent
with open(HERE / "logging_config.yaml") as file:
    logging.config.dictConfig(yaml.safe_load(file))

log = logging.getLogger(__name__)


def get_api_v1() -> FastAPI:
    api = FastAPI(
        root_path=API_V1_PREFIX,
        title="Giovanni's Italian Caffe Order and Schedule API (v1)",
    )

    api.include_router(api_v1.home_router)
    api.include_router(api_v1.ping_router)
    api.include_router(api_v1.order_router)
    api.include_router(api_v1.schedule_router)

    api.add_event_handler("startup", db.connect)
    api.add_event_handler("shutdown", db.disconnect)

    log.info("API v1 created successfully")
    return api


def app() -> FastAPI:
    app = FastAPI(
        title="Giovanni's Italian Caffe",
        docs_url=None,
    )

    # Mount the API with its relevant path
    api = get_api_v1()

    # These are just temporary niceties in lieu of a frontend,
    # so that visiting "/" or "/ping" don't just return "not found"
    @app.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    async def home() -> RedirectResponse:
        return RedirectResponse(f"{API_V1_PREFIX}/")

    @app.get("/ping", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    async def ping() -> RedirectResponse:
        return RedirectResponse(f"{API_V1_PREFIX}/ping")

    log.info("Application created successfully")

    app.mount(API_V1_PREFIX, api)
    return app
