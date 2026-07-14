from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=64)

# Properties to receive via API on update
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=64)
    profile_image: Optional[str] = None
    gemini_api_key: Optional[str] = None

class GoogleLogin(BaseModel):
    token: str # ID token from Google

class UserInDBBase(UserBase):
    id: int
    auth_provider: str
    google_id: Optional[str] = None
    profile_image: Optional[str] = None
    gemini_api_key: Optional[str] = None
    role: str
    subscription_plan: str
    is_email_verified: bool
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password_hash: Optional[str] = None
