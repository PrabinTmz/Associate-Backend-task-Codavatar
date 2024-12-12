from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from models.user import User
from schemas.auth import UserCreate, UserLogin, Token, TokenRefresh, TokenAccess
from api.v1.utils.jwt import generate_tokens, verify_token
from api.v1.utils.password import verify_password, hash_password

router = APIRouter()


# Register User
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user.

    Parameters:
    - user_create (UserCreate): The user registration details.
    - db (AsyncSession): Database session dependency.

    Returns:
    - JSONResponse: Success message if registration is successful.

    Raises:
    - HTTPException: If the email is already registered or invalid.
    """

    # Check if the email is already registered
    result = await db.execute(select(User).filter(User.email == user_create.email))
    db_user = result.scalar_one_or_none()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered!",
        )

    # Hash the user's password
    hashed_password = hash_password(user_create.password)

    # Create a new user instance
    user = User(email=user_create.email, password=hashed_password)

    # Validate email format on model level
    try:
        user.validate_email()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format!",
        )

    # Add and commit the new user to the database
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return JSONResponse(
        content={"message": "User registered successfully."},
    )


# Login user endpoint
@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def create_token(
    user_login: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """
    Handles user login by verifying credentials and issuing JWT tokens.

    Args:
        user_login (UserLogin): User credentials (email & password) provided for login.
        db (AsyncSession): Database session dependency.

    Returns:
        JSONResponse: JWT tokens (access & refresh) if authentication is successful.

    Raises:
        HTTPException: If credentials are invalid.
    """
    # Retrieve the user from the database by email
    result = await db.execute(select(User).filter(User.email == user_login.email))
    db_user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if not db_user or not verify_password(user_login.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    # Generate access and refresh tokens asynchronously
    tokens = await generate_tokens({"sub": db_user.email})

    return tokens


# Refresh token endpoint
@router.post("/refresh", response_model=TokenAccess, status_code=status.HTTP_200_OK)
async def refresh_access_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db),
):
    """
    Handles the process of refreshing an access token using a valid refresh token.

    Args:
        token_data (TokenRefresh): Data containing the refresh token sent by the client.
        db (AsyncSession): Database session dependency.

    Returns:
        JSONResponse: New JWT access token if refresh is valid.

    Raises:
        HTTPException: If the refresh token is invalid or expired.
    """
    # Verify the provided refresh token asynchronously
    payload = await verify_token(token_data.refresh_token, "refresh")

    # Check if token verification was unsuccessful or payload is invalid
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        )

    # Generate new access tokens based on the verified payload
    new_token = await generate_tokens({"sub": payload["sub"]}, "access")

    return new_token
