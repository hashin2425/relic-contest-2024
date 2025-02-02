"""Authentication endpoints module"""

from datetime import datetime
from typing import Any
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi_limiter.depends import RateLimiter
from motor.motor_asyncio import AsyncIOMotorCollection

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_current_user,
    get_password_hash
)
from app.models.auth_models import Token, UserLogin, UserCreate, UserProfile
from app.core.security import require_auth
from app.utils.log_utils import logging
from app.core.mongodb_core import db

api_router = APIRouter()
security = HTTPBearer()

# Rate limiting settings
AUTH_RATE_LIMIT = 5  # requests
AUTH_RATE_TIME = 60  # seconds


@api_router.post("/register", response_model=UserProfile)
async def register(
    user_data: UserCreate,
    rate_limiter: None = Depends(RateLimiter(times=AUTH_RATE_LIMIT, seconds=AUTH_RATE_TIME))
) -> Any:
    """Register a new user"""
    # Ensure collection exists
    if not db.users:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service unavailable"
        )
        
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_dict = user_data.dict()
    user_dict["hashed_password"] = get_password_hash(user_data.password)
    user_dict["created_at"] = datetime.utcnow()
    user_dict["is_active"] = True
    del user_dict["password"]  # Remove plain password
    
    if not db.users:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service unavailable"
        )
    result = await db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    
    return UserProfile(**user_dict)

@api_router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    rate_limiter: None = Depends(RateLimiter(times=AUTH_RATE_LIMIT, seconds=AUTH_RATE_TIME))
) -> Any:
    """Login user"""
    if not db.users:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service unavailable"
        )
    user = await db.users.find_one({"email": user_data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
        
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )

    # Update last login time
    if not db.users:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service unavailable"
        )
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )

    token_data = {
        "sub": str(user["_id"]),
        "email": user["email"],
        "roles": user.get("roles", ["user"]),
        "is_active": user.get("is_active", True)
    }

    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
    }


@api_router.post("/refresh", response_model=Token)
@require_auth()
async def refresh_token(
    current_user: dict = Depends(get_current_user),
    rate_limiter: None = Depends(RateLimiter(times=AUTH_RATE_LIMIT, seconds=AUTH_RATE_TIME))
) -> Any:
    """Refresh access and refresh tokens"""
    # Get fresh user data
    if not db.users:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service unavailable"
        )
    user = await db.users.find_one({"_id": current_user["sub"]})
    if not user or not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    token_data = {
        "sub": str(user["_id"]),
        "email": user["email"],
        "roles": user.get("roles", ["user"]),
        "is_active": user.get("is_active", True)
    }

    return {
        "access_token": create_access_token(token_data),
        "refresh_token": create_refresh_token(token_data),
        "token_type": "bearer",
    }

@api_router.get("/is-logged-in")
@require_auth()
async def is_logged_in(current_user: dict = Depends(get_current_user)):
    """Lightweight auth check"""
    return {
        "message": "true",
        "id": current_user["sub"],
        "email": current_user.get("email")
    }

@api_router.get("/me", response_model=UserProfile)
@require_auth()
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Get detailed user profile"""
    if not db.users:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service unavailable"
        )
    user = await db.users.find_one({"_id": current_user["sub"]})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserProfile(**user)
