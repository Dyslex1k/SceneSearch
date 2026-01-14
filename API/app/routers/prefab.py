from datetime import datetime, timezone
from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

# Databases
from app.core.database import mongo_db

# Custom Data
from app.models.prefab import Prefab, PrefabUpdate, UserCreatedPrefab

router = APIRouter(prefix="/prefabs", tags=["Prefabs"])

@router.post("/")
async def create_prefab(payload: UserCreatedPrefab):

    cleaned_payload = Prefab(**payload.model_dump())
    
    result = await mongo_db.prefabs.insert_one(
        cleaned_payload.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json"
        )
    )

    return {"id": str(result.inserted_id)}

@router.get("/", response_model=List[Prefab])
async def get_all_prefabs():
    prefabs: List[Prefab] = []

    cursor = mongo_db.prefabs.find()

    async for doc in cursor:
        prefabs.append(Prefab(**doc))

    return prefabs

@router.get("/{prefab_id}", response_model=Prefab)
async def get_prefab(prefab_id: str):
    if not ObjectId.is_valid(prefab_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid prefab id"
        )

    doc = await mongo_db.prefabs.find_one(
        {"_id": ObjectId(prefab_id)}
    )

    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prefab not found"
        )

    return Prefab(**doc)

@router.patch("/{prefab_id}", response_model=Prefab)
async def update_prefab(prefab_id: str, payload: PrefabUpdate):
    if not ObjectId.is_valid(prefab_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid prefab id"
        )
    
    update_data = payload.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    update_data["updated_at"] = datetime.now(timezone.utc)

    update_doc = jsonable_encoder(update_data)

    result = await mongo_db.prefabs.find_one_and_update(
        {"_id": ObjectId(prefab_id)},
        {"$set": update_doc},
        return_document=True
    )

    if result is None: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prefab not found"
        )

    return Prefab(**result)

@router.delete("/{prefab_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prefab(prefab_id: str):
    if not ObjectId.is_valid(prefab_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid prefab id"
        )

    result = await mongo_db.prefabs.delete_one(
        {"_id": ObjectId(prefab_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prefab not found"
        )
    
    return None