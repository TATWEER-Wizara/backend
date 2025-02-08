from fastapi import APIRouter, HTTPException, Depends
from app.database import users_collection
from app.models.users import UserCreate,UserBase,  TokenResponse,UserResponse,UserLogin
from app.services.auth_service import hash_password, verify_password, create_access_token
from bson import ObjectId


auth_router = APIRouter()

@auth_router.post("/register", response_model=TokenResponse)
async def register_user(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    
    user_data = user.model_dump()
    user_data["password"] = hash_password(user.password)
    user_data["company_name"] = user.company_name
    user_data["_id"] = str(ObjectId())

    await users_collection.insert_one(user_data)

    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

@auth_router.post("/login", response_model=TokenResponse)
async def login_user(user: UserLogin):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")


    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
