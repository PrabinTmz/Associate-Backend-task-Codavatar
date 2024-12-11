from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from models.user import User
from schemas.auth import UserCreate, UserLogin, Token
from utils.jwt import create_access_token
from utils.password import verify_password, hash_password


router = APIRouter()


# Register User
@router.post("/register", status_code=201)
async def register_user(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    # Asynchronously check if the email is already registered
    result = await db.execute(
        select(User).filter(User.email == user_create.email)
    )
    db_user = result.scalar_one_or_none()


    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered!"
        )

    hashed_password = hash_password(user_create.password)

    user = User(
        email=user_create.email,
        password=hashed_password,
    )

    
    try:
        user.validate_email()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid email format!"
        )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    response = {"message": "User registered successfully."}

    return JSONResponse(response)


# Login User
@router.post("/login", response_model=Token)
async def login_user(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).filter(User.email == user_login.email)
    )
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(user_login.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": db_user.email})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": access_token, "token_type": "bearer"},
    )
