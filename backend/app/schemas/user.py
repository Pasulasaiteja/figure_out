"""
User Schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[int] = None
    height: Optional[int] = None
    gender: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    age: Optional[int] = None
    weight: Optional[int] = None
    height: Optional[int] = None
    gender: Optional[str] = None
    workout_streak: int
    total_calories_burned: int
    charity_contribution: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    user_id: Optional[int] = None
