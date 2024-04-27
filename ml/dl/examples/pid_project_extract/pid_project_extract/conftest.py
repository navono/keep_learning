import asyncio
import sys
import uuid
from asyncio.events import AbstractEventLoop
from typing import Any, AsyncGenerator, Generator
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from pid_project_extract.settings import settings
from pid_project_extract.web.application import get_app
from piccolo.conf.apps import Finder
from piccolo.table import create_tables, drop_tables


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return 'asyncio'

@pytest.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    """
    Fixture to create all tables before test and drop them after.

    :yield: nothing.
    """
    tables = Finder().get_table_classes()
    create_tables(*tables, if_not_exists=True)

    yield

    drop_tables(*tables)



@pytest.fixture
def fastapi_app(
    
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
            yield ac
