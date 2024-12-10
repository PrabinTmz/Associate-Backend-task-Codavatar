from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from schemas.auth import UserCreate, UserLogin, Token
from utils.jwt import create_access_token
from utils.password import verify_password, hash_password


router = APIRouter()


# Register User
@router.post("/register", status_code=201)
async def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_create.email).first()

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered!")

    hashed_password = hash_password(user_create.password)
    db_user = User(
        email=user_create.email,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    response = {"message": "User registered successfully."}

    return JSONResponse(response)


# Login User
@router.post("/login", response_model=Token)
async def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_login.email).first()
    if not db_user or not verify_password(user_login.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})

    return JSONResponse(
        status_code=200, 
        content={"access_token": access_token, "token_type": "bearer"}
    )
