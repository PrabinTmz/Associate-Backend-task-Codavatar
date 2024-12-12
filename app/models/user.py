from uuid import uuid4
from email_validator import validate_email as validate_email_address, EmailSyntaxError
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.database import Base


class User(Base):
    """
    SQLAlchemy User model representing the users table.
    Handles user authentication and stores user-related data.
    """
    __tablename__ = "users"

    # Primary key: Unique identifier for each user
    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    
    # User email, must be unique and indexed for faster lookup
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
    # Timestamps for record creation and update
    created_at = Column(DateTime, default=func.now())  # Automatically set on creation
    updated_at = Column(DateTime, onupdate=func.now())  # Automatically updated on change

    def validate_email(self):
        """
        Validates the user's email address using the `email_validator` package.

        Raises:
            ValueError: If the email is invalid according to standard email syntax rules.
        """
        try:
            # Validate email syntax
            validate_email_address(self.email)
        except EmailSyntaxError:
            # Raise an exception if the email is invalid
            raise ValueError("Invalid email address.")
