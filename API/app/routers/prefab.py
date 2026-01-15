from datetime import datetime, timezone
from typing import Any, List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder

# Databases
from app.core.database import mongo_db, opensearch

# Custom Data
from app.models.prefab import Prefab, PrefabUpdate, UserCreatedPrefab

# Auth
from app.dependencies import get_current_user_id

# Fucntions
from app.services.openSearch import prefab_to_search_doc


router = APIRouter(prefix="/prefabs", tags=["Prefabs"])

@router.post("/")
async def create_prefab(
    payload: UserCreatedPrefab,
    user_id: str = Depends(get_current_user_id)
):
    cleaned_payload = Prefab(
        **payload.model_dump(),
        creator_id=user_id
    )

    result = await mongo_db.prefabs.insert_one(
        cleaned_payload.model_dump(
            by_alias=True,
            exclude_none=True,
            mode="json"
        )
    )

    prefab_id = result.inserted_id
    cleaned_payload.id = prefab_id

    # fetch creator username
    user_doc = await mongo_db.users.find_one({"_id": ObjectId(user_id)})
    creator_username = user_doc["username"] # type: ignore

    search_doc = await prefab_to_search_doc(cleaned_payload, creator_username) # type: ignore

    # index into OpenSearch
    await opensearch.index(
        index="prefabs_v1",
        id=str(prefab_id),
        body=search_doc
    )

    return {"id": str(prefab_id)}

@router.get("/search")
async def search_prefabs(
    q: str = Query(..., min_length=1),
    use_cases: List[str] | None = Query(None),
    categories: List[str] | None = Query(None),
    is_free: bool | None = None,
    licence_type: str | None = None,
    limit: int = 20,
    offset: int = 0
) -> dict[str, Any]:
    filters = []

    if use_cases:
        filters.append({"terms": {"use_cases": use_cases}}) # type: ignore

    if categories:
        filters.append({"terms": {"categories": categories}}) # type: ignore

    if is_free is not None:
        filters.append({"term": {"is_free": is_free}}) # type: ignore

    if licence_type:
        filters.append({"term": {"licence_type": licence_type}}) # type: ignore

    query_body = { # type: ignore
        "from": offset,
        "size": limit,
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": q,
                            "fields": [
                                "name^4",
                                "description^2",
                                "content",
                                "creator.username^3"
                            ]
                        }
                    }
                ],
                "filter": filters
            }
        }
    }

    response = await opensearch.search(
        index="prefabs_v1",
        body=query_body # type: ignore
    )

    results = [
        hit["_source"] | {"_score": hit["_score"]}
        for hit in response["hits"]["hits"]
    ]

    return {
        "total": response["hits"]["total"]["value"],
        "results": results
    }

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
async def update_prefab(prefab_id: str, payload: PrefabUpdate, user_id: str = Depends(get_current_user_id)):
    if not ObjectId.is_valid(prefab_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid prefab id"
        )
    
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    update_data["updated_at"] = datetime.now(timezone.utc)
    update_doc = jsonable_encoder(update_data)

    # Restrict update to creator only
    result = await mongo_db.prefabs.find_one_and_update(
        {"_id": ObjectId(prefab_id), "creator_id": user_id},
        {"$set": update_doc},
        return_document=True
    )

    if result is None: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prefab not found or you're not the creator"
        )
    
    # after result is returned
    user_doc = await mongo_db.users.find_one({"_id": ObjectId(user_id)})

    await opensearch.index(
        index="prefabs_v1",
        id=str(prefab_id),
        body=prefab_to_search_doc(Prefab(**result), user_doc["username"]) # type: ignore
    )

    return Prefab(**result)

@router.delete("/{prefab_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prefab(prefab_id: str, user_id: str = Depends(get_current_user_id)):
    if not ObjectId.is_valid(prefab_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid prefab id"
        )

    # Restrict deletion to creator only
    result = await mongo_db.prefabs.delete_one(
        {"_id": ObjectId(prefab_id), "creator_id": user_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prefab not found or you're not the creator"
        )
    
    await opensearch.delete(
        index="prefabs_v1",
        id=prefab_id
    )
    
    return None


