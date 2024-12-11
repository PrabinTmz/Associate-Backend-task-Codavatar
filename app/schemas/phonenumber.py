from pydantic import BaseModel, field_validator, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

import phonenumbers


# Schema for creating a phone number
class PhoneNumberCreate(BaseModel):
    # number: str = Field(..., pattern=r"^\+?\d{10,15}$")
    number: str

    @field_validator("number")
    def validate_number(cls, v):
        """
        Validates international phone numbers using the numbers library.
        Handles numbers across all countries.
        """
        try:
            # Parse the phone number. It will detect the country code automatically
            parsed_number = phonenumbers.parse(
                v, None
            )  # None means auto-detect the country code

            # Check if the number is valid
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Invalid phone number.")
        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number format.")

        # Return the validated and properly formatted phone number
        return phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )  # Validation for phone number length


class PhoneNumberRead(BaseModel):
    user_id: UUID
    phonenumber_id: UUID
    number: str
    created_at: datetime

    class Config:
        orm_mode = True  # Allows compatibility with SQLAlchemy models
