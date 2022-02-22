import logging

from fastapi import FastAPI

import adagiovanni.api.v1 as api_v1
from adagiovanni import db
from adagiovanni.core.config import API_V1_PREFIX

log = logging.getLogger(__name__)


def app() -> FastAPI:
    app = FastAPI(
        title="Giovanni's Italian Caffe",
        docs_url=None,
    )
    api = FastAPI(root_path=API_V1_PREFIX)
    api.include_router(api_v1.home_router)
    api.include_router(api_v1.ping_router)
    api.include_router(api_v1.order_router)
    api.include_router(api_v1.schedule_router)

    log.info("Application created successfully")

    api.add_event_handler("startup", db.connect)
    api.add_event_handler("shutdown", db.disconnect)
    app.mount(API_V1_PREFIX, api)
    return app
