""" 認証モデル """

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """トークンモデル"""

    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    """トークンデータモデル"""

    id: Optional[str] = None


class UserLogin(BaseModel):
    """ユーザーログインモデル"""

    id: str
    password: str
