from typing import Any

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
)
from neo4j import AsyncDriver, AsyncGraphDatabase
from opensearchpy import AsyncOpenSearch
import redis.asyncio as redis
from redis.asyncio import Redis

from app.core.config import (
    MONGO_URI,
    NEO4J_URI,
    NEO4J_USER,
    NEO4J_PASSWORD,
    OPENSEARCH_HOST,
    REDIS_URL,
)

# ---- MongoDB ----
mongo_client: AsyncIOMotorClient[dict[str, Any]] = AsyncIOMotorClient(
    MONGO_URI
)

mongo_db: AsyncIOMotorDatabase[dict[str, Any]] = (
    mongo_client.get_default_database()
)

# ---- Neo4j ----
neo4j_driver: AsyncDriver = AsyncGraphDatabase.driver( # type: ignore
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD),
)

# ---- OpenSearch ----
opensearch = AsyncOpenSearch(
    OPENSEARCH_HOST,
    http_compress=True,
)

# ---- Redis ----
redis_client: Redis = redis.from_url(REDIS_URL) # type: ignore
