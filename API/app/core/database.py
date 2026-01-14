from typing import Any

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
)
from neo4j import AsyncDriver, AsyncGraphDatabase
from opensearchpy import OpenSearch
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

# ---- Runtime validation to satisfy type narrowing ----

if MONGO_URI is None:
    raise RuntimeError("MONGO_URI is not set")

if NEO4J_URI is None:
    raise RuntimeError("NEO4J_URI is not set")

if NEO4J_USER is None or NEO4J_PASSWORD is None:
    raise RuntimeError("NEO4J credentials are not set")

if REDIS_URL is None:
    raise RuntimeError("REDIS_URL is not set")

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
opensearch: OpenSearch = OpenSearch(OPENSEARCH_HOST)

# ---- Redis ----
redis_client: Redis = redis.from_url(REDIS_URL) # type: ignore
