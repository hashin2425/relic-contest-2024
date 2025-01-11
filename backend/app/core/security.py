"""Security module for authentication and authorization"""

from typing import Optional, Dict, Any
from functools import wraps
import os
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
SECRET_KEY: str = os.getenv("SECRET_KEY", os.urandom(32).hex())
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
REFRESH_TOKEN_EXPIRE_DAYS: int = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_token["exp"] >= datetime.now(timezone.utc).timestamp():
            return decoded_token
        else:
            raise ValueError("Token expired")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    token = decode_token(credentials.credentials)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired token")
    return token


def require_auth(roles: Optional[list] = None):
    """
    Decorator for protecting routes with JWT authentication and optional role-based access
    Args:
        roles: Optional list of required roles for accessing the endpoint
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, token: Dict[str, Any] = Security(get_current_user), **kwargs):
            # Check roles if specified
            if roles:
                user_roles = token.get("roles", [])
                if not any(role in roles for role in user_roles):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have required roles")

            return await func(*args, **kwargs)

        return wrapper

    return decorator
