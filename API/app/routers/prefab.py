from fastapi import APIRouter
from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from app.schemas.prefab import PrefabCreate
from app.core.database import mongo_db
from datetime import datetime, timezone

router = APIRouter(prefix="/prefabs", tags=["Prefabs"])


@router.post("")
async def create_prefab(payload: PrefabCreate):
    prefab_id = str(uuid4())

    document = jsonable_encoder(payload)
    document["_id"] = prefab_id
    document["status"] = "published"
    document["created_at"] = datetime.now(timezone.utc)

    await mongo_db.prefabs.insert_one(document)

    return {"prefab_id": prefab_id}
