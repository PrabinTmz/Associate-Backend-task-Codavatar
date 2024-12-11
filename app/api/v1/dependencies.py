from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user import User
from core.database import get_db  # Dependency for the database session
from utils.jwt import verify_access_token


async def get_current_user(
    request: Request, db: AsyncSession = Depends(get_db)
) -> User:
    # Extract token from the Authorization header
    token = request.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials!",
        )

    token = token.split(" ")[1]  # Extract only the token part

    # Decode the token
    payload = verify_access_token(token)
    user_email = payload.get("sub")

    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    # Query the database to validate user existence
    result = await db.execute(select(User).filter(User.email == user_email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
