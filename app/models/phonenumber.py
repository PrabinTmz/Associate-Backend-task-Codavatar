from uuid import uuid4

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.database import Base


# from models.user import User
class PhoneNumber(Base):
    """
    SQLAlchemy User model representing the users table.
    """

    __tablename__ = "phonenumbers"

    phonenumber_id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    number = Column(String(15), unique=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
