from fastapi import APIRouter, Depends, status, HTTPException
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
    """
    Create a new phone number for the authenticated user.

    Parameters:
    - phonenumber (PhoneNumberCreate): Data for the new phone number.
    - current_user (User): The currently authenticated user (injected dependency).
    - db (AsyncSession): Database session (injected dependency).

    Returns:
    - PhoneNumberRead: The created phone number's details.

    Raises:
    - HTTPException: If the phone number is already registered.
    """
    # Check if the phone number already exists in the database
    result = await db.execute(
        select(PhoneNumber).filter(PhoneNumber.number == phonenumber.number)
    )
    db_phonenumber = result.scalar_one_or_none()

    if db_phonenumber:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number already registered!",
        )

    # Create a new phone number associated with the authenticated user
    new_phonenumber = PhoneNumber(
        user_id=current_user.user_id,
        number=phonenumber.number,
    )
    db.add(new_phonenumber)
    await db.commit()
    await db.refresh(new_phonenumber)

    return new_phonenumber


@router.get("/", response_model=list[PhoneNumberRead], status_code=status.HTTP_200_OK)
async def get_phonenumbers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve all phone numbers associated with the authenticated user.

    Parameters:
    - current_user (User): The currently authenticated user (injected dependency).
    - db (AsyncSession): Database session (injected dependency).

    Returns:
    - list[PhoneNumberRead]: A list of phone numbers for the authenticated user.
    """
    # Query phone numbers belonging to the authenticated user
    result = await db.execute(
        select(PhoneNumber).filter(PhoneNumber.user_id == current_user.user_id)
    )
    phonenumbers = result.scalars().all()

    # Check if no phone numbers are found
    if not phonenumbers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No phone numbers found for {current_user.email}.",
        )

    return phonenumbers
