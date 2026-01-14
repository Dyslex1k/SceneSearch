import os

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value

# Databases
MONGO_URI = require_env("MONGO_URI")
NEO4J_URI = require_env("NEO4J_URI")
NEO4J_USER = require_env("NEO4J_USER")
NEO4J_PASSWORD = require_env("NEO4J_PASSWORD")
OPENSEARCH_HOST = require_env("OPENSEARCH_HOST")
REDIS_URL = require_env("REDIS_URL")

# External Services
DISCORD_CLIENT_ID = require_env("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = require_env("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")

# Secrets
JWT_SECRET = require_env("JWT_SECRET")