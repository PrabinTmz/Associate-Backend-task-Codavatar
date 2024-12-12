from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from core.database import get_db  # Dependency for database session
from api.v1.utils.jwt import verify_token
from fastapi.security import OAuth2PasswordBearer

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency to get the currently authenticated user.

    Args:
        token (str): JWT token extracted from the request's Authorization header.
        db (AsyncSession): Database session dependency.

    Returns:
        User: Authenticated user object.

    Raises:
        HTTPException: If token is invalid, expired, or user doesn't exist in DB.
    """

    # Ensure token is provided
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials are missing!",
        )

    # Decode and verify the token payload
    payload = await verify_token(token)
    user_email = payload.get("sub")

    invalid_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token!",
    )

    # Handle invalid token payloads
    if not user_email:
        raise invalid_token_exception

    # Query database to check if the user exists
    result = await db.execute(select(User).filter(User.email == user_email))
    user = result.scalar_one_or_none()

    # Handle cases where the user doesn't exist
    if not user:
        raise invalid_token_exception

    # Return the user if authentication is successful
    return user
