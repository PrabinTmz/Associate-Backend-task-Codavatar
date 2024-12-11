from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from schemas.phonenumber import PhoneNumberCreate, PhoneNumberRead
from models.user import User
from models.phonenumber import PhoneNumber

from api.v1.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=PhoneNumberRead, status_code=status.HTTP_201_CREATED)
async def create_phonenumber(
    phonenumber: PhoneNumberCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PhoneNumberRead:
    result = await db.execute(
        select(PhoneNumber).filter(PhoneNumber.number == phonenumber.number)
    )

    db_phonenumber = result.scalar_one_or_none()

    if db_phonenumber:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Number already registered!"
        )

    phonenumber = PhoneNumber(
        user_id=current_user.user_id,
        number=phonenumber.number,
    )

    db.add(phonenumber)
    await db.commit()
    await db.refresh(phonenumber)

    return phonenumber


@router.get("/", response_model=list[PhoneNumberRead], status_code=status.HTTP_200_OK)
async def get_phonenumbers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(PhoneNumber).filter(PhoneNumber.user_id == current_user.user_id)
    )
    phonenumbers = result.scalars().all()

    return phonenumbers
