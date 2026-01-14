from typing import Any
from fastapi import APIRouter, HTTPException
import httpx
import time
from datetime import datetime, timezone
from jose import jwt

# Secrets
from app.core.config import (
    DISCORD_CLIENT_ID,
    DISCORD_CLIENT_SECRET,
    DISCORD_REDIRECT_URI,
    JWT_SECRET,
)

# Database
from app.core.database import mongo_db

# Models
from app.models.user import User, UserCreate


router = APIRouter(prefix="/auth/discord", tags=["auth"])

users_collection = mongo_db.users


@router.get("/login")
def discord_login():
    url = (
        "https://discord.com/api/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        "&response_type=code"
        "&scope=identify"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
    )
    return {"url": url}


@router.get("/callback")
async def discord_callback(code: str) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        # Exchange code for token
        token_res = await client.post(
            "https://discord.com/api/oauth2/token",
            data={
                "client_id": DISCORD_CLIENT_ID,
                "client_secret": DISCORD_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": DISCORD_REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if token_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Discord token exchange failed")

        access_token = token_res.json()["access_token"]

        # Fetch Discord user
        user_res = await client.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if user_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch Discord user")

        discord_user = user_res.json()

    # Check existing user
    existing = await users_collection.find_one(
        {"discord_id": discord_user["id"]}
    )

    now = datetime.now(timezone.utc)

    if existing:
        await users_collection.update_one(
            {"_id": existing["_id"]},
            {"$set": {"last_login": now}},
        )
        user = User(**existing)
    else:
        user_in = UserCreate(
            discord_id=discord_user["id"],
            username=discord_user["username"],
            discriminator=discord_user.get("discriminator"),
            avatar=discord_user.get("avatar"),
        )

        insert_data = user_in.model_dump()
        insert_data["created_at"] = now
        insert_data["last_login"] = now

        result = await users_collection.insert_one(insert_data)
        insert_data["_id"] = result.inserted_id

        user = User(**insert_data)

    # Create JWT
    payload: dict[str, Any] = {
        "sub": user.id,
        "discord_id": user.discord_id,
        "exp": int(time.time()) + 60 * 60 * 24,
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256") # type: ignore

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }
