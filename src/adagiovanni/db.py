import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from adagiovanni.core.config import (
    MAX_MONGO_CONNECTION_POOL_SIZE,
    MIN_MONGO_CONNECTION_POOL_SIZE,
    MONGO_URL,
)

log = logging.getLogger(__name__)

client: Optional[AsyncIOMotorClient] = None


async def get_client() -> AsyncIOMotorClient:
    global client
    if not client:
        await connect()
    return client


async def connect() -> AsyncIOMotorClient:
    global client
    client = AsyncIOMotorClient(
        str(MONGO_URL),
        minPoolSize=MIN_MONGO_CONNECTION_POOL_SIZE,
        maxPoolSize=MAX_MONGO_CONNECTION_POOL_SIZE,
    )
    log.info("Successfully connected to MongoDB")
    return client


async def disconnect() -> None:
    global client
    log.info("Disconnecting from MongoDB")
    if not client:
        log.error("Disconnect called for MongoDB client, but no client exists")
    else:
        client.close()
