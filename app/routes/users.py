from fastapi import APIRouter, Depends, HTTPException
from app.database import users_collection
from app.models.users import UserResponse
from bson import ObjectId

users_router = APIRouter()

@users_router.get("/users", response_model=list[UserResponse])
async def get_users():


    users = await users_collection.find().to_list(100)
    return [{"id": str(user["_id"]), "email": user["email"], "company_name": user["company_name"]} for user in users]

@users_router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": str(user["_id"]), "email": user["email"], "full_name": user["company_name"]}


