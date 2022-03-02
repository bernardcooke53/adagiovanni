# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
Module providing the database client.

This keeps track of the active client in a
global private instance, as opposed to hiding
beneath a class namespace & further abstracting.

Calling code should use the `Client` type alias
and call `get_client` when requesting an instance -
this should make it somewhat easier to change the
database out in the future, though to properly
encapsulate that a full interface will need to be
implemented in this module.
"""
import logging
from typing import Any, AsyncGenerator, Optional

from motor.motor_asyncio import AsyncIOMotorClient as _AsyncIOMotorClient
from typing_extensions import TypeAlias

from adagiovanni.core.config import (
    MAX_MONGO_CONNECTION_POOL_SIZE,
    MIN_MONGO_CONNECTION_POOL_SIZE,
    MONGO_URL,
)

log = logging.getLogger(__name__)

# Ripping out and changing the db will be much easier
# if all the typed code just uses "Client"
Client: TypeAlias = _AsyncIOMotorClient


_client: Optional[Client] = None


async def get_client() -> AsyncGenerator[Client, Any]:
    """
    Main entry point to retrieve the database client
    from this module. Calling code should use this
    function.
    """
    global _client
    if not _client:
        await connect()
    yield _client


async def connect() -> Client:
    """
    Set up the client instance to use for MongoDB;
    in its current version this doesn't perform any
    immediate communication as the client connects
    lazily, however it gives us a hook to ensure the
    client is properly initialized on application
    startup.
    """
    global _client
    _client = Client(
        str(MONGO_URL),
        minPoolSize=MIN_MONGO_CONNECTION_POOL_SIZE,
        maxPoolSize=MAX_MONGO_CONNECTION_POOL_SIZE,
    )

    return _client


async def disconnect() -> None:
    """
    Close down the client connection to the
    database, if it was ever set up. Called
    as a shutdown hook for the application.
    """
    global _client
    log.info("Disconnecting from MongoDB")
    if not _client:
        log.warning("Disconnect called for MongoDB client, but no client exists")
    else:
        _client.close()
