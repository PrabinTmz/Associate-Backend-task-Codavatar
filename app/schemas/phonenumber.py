from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime
import phonenumbers


class PhoneNumberCreate(BaseModel):
    """
    Pydantic model to handle phone number creation and validation.
    Includes logic to validate international phone numbers.
    """

    number: str

    @field_validator("number")
    def validate_number(cls, v):
        """
        Validates international phone numbers using the phonenumbers library.
        This ensures the phone number is properly formatted and valid according to global standards.
        Handles country codes automatically.
        """
        try:
            # Parse the phone number. 'None' allows automatic country code detection.
            parsed_number = phonenumbers.parse(v, None)

            # Check if the number is valid
            if not phonenumbers.is_valid_number(parsed_number):
                # Raise an exception if the number fails validation
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid phone number. Include the country code (e.g., +1234567890) and "
                    "ensure it follows the correct format.",
                )
        except phonenumbers.NumberParseException:
            # Handle parsing exceptions gracefully
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone number.",
            )

        # Return the validated and properly formatted phone number (E.164 standard)
        return phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )


class PhoneNumberRead(BaseModel):
    """
    Pydantic model to represent a read response for phone numbers.
    Designed for use with database responses.
    """

    phonenumber_id: UUID  # Unique identifier for the phone number
    number: str  # The phone number itself
    created_at: datetime  # Timestamp of when the phone number was created

    class Config:
        """
        Configuration for Pydantic's compatibility with SQLAlchemy models.
        Allows SQLAlchemy models to convert attributes into Pydantic responses seamlessly.
        """

        from_attributes = (
            True  # Maps SQLAlchemy model attributes directly to Pydantic responses
        )
