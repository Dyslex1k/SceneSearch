from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from bson import ObjectId

from .common import PyObjectId

class UserCreate(BaseModel):
    discord_id: str
    username: str
    discriminator: Optional[str] = None
    avatar: Optional[str] = None


class User(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    discord_id: str = Field(..., min_length=1)
    username: str = Field(...)
    discriminator: Optional[str] = None
    avatar: Optional[str] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "discord_id": "123456789012345678",
                "username": "Dyslex1k",
                "discriminator": "0001",
                "avatar": "a_1b2c3d4e",
            }
        },
    )