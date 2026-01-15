from app.models.prefab import Prefab
from typing import Any, Dict

async def prefab_to_search_doc(prefab: Prefab, creator_username: str) -> Dict[str, Any]:
    return {
        "id": str(prefab.id),
        "name": prefab.name,
        "description": prefab.description,
        "content": prefab.content,

        "use_cases": [uc.value for uc in prefab.use_cases],
        "categories": [c.value for c in prefab.categories],

        "licence_type": prefab.licence_type.value,
        "is_free": prefab.is_free,

        "creator": {
            "id": prefab.creator_id,
            "username": creator_username
        },

        "created_at": prefab.created_at.isoformat()
    }