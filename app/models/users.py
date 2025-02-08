from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime, UTC

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The email address for the user")
   
class UserLogin(UserBase):
    password: str = Field(..., description="The password for the user")

class UserCreate(UserBase):
    company_name: str = Field(..., description="The companyname of the user")

    password: str = Field(..., description="The password for the user")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="The date and time the user was created")

    

class UserResponse(UserBase):
    id: str = Field(..., description="The unique identifier for the user")
    company_name: str = Field(..., description="The company name of the user")
    
    

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="The access token for the user")
    token_type: str = Field(..., description="The type of token")
