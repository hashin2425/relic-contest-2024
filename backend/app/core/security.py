"""Security module for authentication and authorization"""

from typing import Optional, Dict, Any
from functools import wraps
import os
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from fastapi import HTTPException, Security, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

security = HTTPBearer()
SECRET_KEY: str = os.getenv("SECRET_KEY", os.urandom(32).hex())
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
REFRESH_TOKEN_EXPIRE_DAYS: int = 30

# Rate limiting settings
RATE_LIMIT_TIMES = 5  # Number of requests
RATE_LIMIT_SECONDS = 60  # Time window in seconds


def get_password_hash(password: str) -> str:
    """Generate salted password hash"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    try:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    except Exception:
        return False

def create_token(data: dict, expires_delta: timedelta) -> str:
    """Create JWT token with expiration"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(data: dict) -> str:
    """Create access token"""
    return create_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(data: dict) -> str:
    """Create refresh token"""
    return create_token(data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


def decode_token(token: str) -> dict:
    """Decode and validate JWT token"""
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check token expiration
        exp = decoded_token.get("exp")
        if not exp or exp < datetime.now(timezone.utc).timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        # Check token issue time
        iat = decoded_token.get("iat")
        if not iat or iat > datetime.now(timezone.utc).timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token issue time",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        return decoded_token
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security),
    rate_limiter: None = Depends(RateLimiter(times=RATE_LIMIT_TIMES, seconds=RATE_LIMIT_SECONDS))
) -> dict:
    """Get current user with rate limiting"""
    token = decode_token(credentials.credentials)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return token


def require_auth(roles: Optional[list] = None, require_active: bool = True):
    """
    Enhanced decorator for protecting routes with JWT authentication and role-based access
    Args:
        roles: Optional list of required roles for accessing the endpoint
        require_active: Whether to require the user to be active
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args,
            token: Dict[str, Any] = Security(get_current_user),
            **kwargs
        ):
            # Check if user is active if required
            if require_active and not token.get("is_active", True):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Inactive user"
                )
                
            # Check roles if specified
            if roles:
                user_roles = token.get("roles", [])
                if not any(role in roles for role in user_roles):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="User doesn't have required roles"
                    )

            return await func(*args, **kwargs)
        return wrapper
    return decorator
