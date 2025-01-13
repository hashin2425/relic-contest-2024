""" FastAPI による認証関連のエンドポイントを定義するモジュール """

import os
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
import dotenv

from app.core.security import create_access_token, create_refresh_token, verify_password, get_current_user
from app.models.auth_models import Token, UserLogin
from app.core.security import require_auth
from app.utils.log_utils import logging

api_router = APIRouter()
security = HTTPBearer()
dotenv.load_dotenv()

MOCK_USER = {
    "id": os.getenv("MOCK_USER_ID", "test_user"),
    "hashed_password": os.getenv("MOCK_USER_PW", "pwd1234"),
}


@api_router.post("/login", response_model=Token)
async def login(user_data: UserLogin) -> Any:
    logging(user_data, MOCK_USER)
    if user_data.id != MOCK_USER["id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect id or password",
        )

    if not verify_password(user_data.password, MOCK_USER["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect id or password",
        )

    return {
        "access_token": create_access_token({"sub": user_data.id}),
        "refresh_token": create_refresh_token({"sub": user_data.id}),
        "token_type": "bearer",
    }


@api_router.post("/refresh", response_model=Token)
@require_auth()
async def refresh_token(current_user: dict = Depends(get_current_user)) -> Any:
    return {
        "access_token": create_access_token({"sub": current_user["sub"]}),
        "refresh_token": create_refresh_token({"sub": current_user["sub"]}),
        "token_type": "bearer",
    }


@api_router.get("/me")
@require_auth()
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"id": current_user["sub"]}
