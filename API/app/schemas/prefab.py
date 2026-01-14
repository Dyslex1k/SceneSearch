from pydantic import BaseModel, HttpUrl
from typing import List

class ExternalLink(BaseModel):
    type: str
    url: HttpUrl

class PrefabCreate(BaseModel):
    name: str
    description: str
    use_cases: List[str]
    categories: List[str]
    tags: List[str]
    external_links: List[ExternalLink]
