from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None


class UserCreate(BaseModel):
    """Matches spec request: username, password, email"""
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: int
    email: str
    username: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (use orm_mode=True for v1)


class UserInDB(UserBase):
    hashed_password: str