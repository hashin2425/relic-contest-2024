""" Authentication Models """

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

class Token(BaseModel):
    """Token model for authentication"""
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    """Token data model"""
    id: Optional[str] = None
    roles: List[str] = []

class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: constr(min_length=8)

class UserCreate(BaseModel):
    """User creation model"""
    email: EmailStr
    password: constr(min_length=8)
    name: str
    roles: List[str] = ["user"]

class UserInDB(BaseModel):
    """User database model"""
    id: str
    email: EmailStr
    hashed_password: str
    name: str
    roles: List[str] = ["user"]
    created_at: datetime
    last_login: Optional[datetime]
    is_active: bool = True
    
class UserProfile(BaseModel):
    """User profile model (public data)"""
    id: str
    email: EmailStr
    name: str
    roles: List[str]
    created_at: datetime
