from fastapi import FastAPI

from adagiovanni.api import routes


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(routes.home_router, prefix="/api")
    app.include_router(routes.ping_router, prefix="/api")
    return app


app = get_app()
