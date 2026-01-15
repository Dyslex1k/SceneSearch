from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from app.core.database import mongo_db
from app.dependencies import get_current_user_id
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

users_collection = mongo_db.users


@router.get("/me", response_model=User)
async def get_me(user_id: str = Depends(get_current_user_id)):
    user = await users_collection.find_one(
        {"_id": ObjectId(user_id)}
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return User(**user)
