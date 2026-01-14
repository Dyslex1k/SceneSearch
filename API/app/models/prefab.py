
from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from enum import Enum

from app.models.common import PyObjectId


class UseCase(str, Enum):
    WORLDS = "Worlds"
    AVATARS = "Avatars"
    OSC = "Osc"

class Categories(str, Enum):
    # Art
    MODELS_3D = "3D Models"
    ANIMATION = "Animations"
    MATERIALS = "Materials"
    AUDIO = "Audio"

    #Effects
    VFX = "Visual Effects"
    PARTICLES = "Particles"

    # Untiy Tools
    TOOLING = "Tooling"
    LIGHTING = "Lighting"

    # UI Elements
    UI = "UI"

    # VRC Programming
    UDON = "Udon"
    SHADERS = "Shaders"

class LinkType(str, Enum):
    GUMROAD = "Gumroad"
    BOOTH = "Booth"
    JINXY = "Jinxy"
    GITHUB = "Github"
    GITLAB = "Gitlab"

class ExternalLink(BaseModel):
    type: LinkType = Field(...)
    url: HttpUrl = Field(...)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "Booth",
                "url": "https://booth.pm/en/items/3024678"
            }
        },
    )

class UserCreatedPrefab(BaseModel):
    name: str = Field(...)
    description: str = Field(..., max_length=400)
    content: str = Field(..., max_length=4000)

    use_cases: List[UseCase] = Field(..., max_length=2)
    categories: List[Categories] = Field(...)
    external_links: List[ExternalLink] = Field(...)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "VRC-Skeletal-Hands",
                "description": "A OSC app that is used to add full skeletal hand tracking to your avatar",
                "content": "# OSC app that is used for data that is really cool\nThis is a cool little project I have",
                "use_cases": [
                    "Avatars",
                    "Osc"
                ],
                "categories": [
                    "Animations",
                    "Tooling"
                ],
                "external_links": [
                    {
                        "type": "Github",
                        "url": "https://github.com/Dyslex1k/VRC-Skeletal-Hands"
                    }  
                ]
            }
        },
    )

class PrefabUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = Field(default=None, max_length=400)
    content: Optional[str] = Field(default=None, max_length=4000)

    use_cases: Optional[List[UseCase]] = None
    categories: Optional[List[Categories]] = None
    external_links: Optional[List[ExternalLink]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "A OSC app that is used to add full skeletal hand tracking to your avatar",
                "external_links": [
                    {
                        "type": "Github",
                        "url": "https://github.com/Dyslex1k/VRC-Skeletal-Hands"
                    }  
                ]
            }
        },
    )

class Prefab(UserCreatedPrefab):
    id: Optional[PyObjectId] = Field(alias="_id", default=None) #Converted as Pydantic does not support ObjectID

    creator_id: PyObjectId = Field(...)

    created_at: datetime = Field(default=datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in anophotonics",
                "gpa": 3.0,
            }
        },
    )