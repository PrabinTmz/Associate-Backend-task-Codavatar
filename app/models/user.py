from uuid import uuid4

from email_validator import validate_email as validate_email_address, EmailSyntaxError

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def validate_email(self):
        try:
            # Validate email syntax using email_validator
            validate_email_address(self.email)
        except EmailSyntaxError:
            raise ValueError("Invalid email address.")
