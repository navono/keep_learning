import logging

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from pid_project_extract.settings import settings
from pid_project_extract.web.api.router import api_router
from importlib import metadata

from pid_project_extract.web.lifetime import (register_shutdown_event,
                                              register_startup_event)


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="pid_project_extract",
        version=metadata.version("pid_project_extract"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
