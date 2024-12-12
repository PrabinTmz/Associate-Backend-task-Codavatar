from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.database import Base
import enum


# Enumerations for Call Type and Call Status
class CallType(str, enum.Enum):
    """
    Enumeration for different types of calls.
    """

    incoming = "incoming"
    outgoing = "outgoing"
    missed = "missed"
    rejected = "rejected"


class CallStatus(str, enum.Enum):
    """
    Enumeration for different statuses of a call.
    """

    completed = "completed"
    failed = "failed"
    no_answer = "no_answer"
    busy = "busy"


class CallLog(Base):
    """
    SQLAlchemy model representing the call log table.
    Tracks information about phone calls including caller/receiver numbers,
    time, type, duration, and status of the call.
    """

    __tablename__ = "call_logs"

    # Primary Key: Unique identifier for each call log entry
    call_log_id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )

    # Foreign Keys: Reference to the phonenumbers table involved in the call
    caller_phonenumber = Column(
        UUID(as_uuid=True), ForeignKey("phonenumbers.phonenumber_id"), nullable=False
    )
    receiver_phonenumber = Column(
        UUID(as_uuid=True), ForeignKey("phonenumbers.phonenumber_id"), nullable=False
    )

    # Call timestamps and duration
    call_start_time = Column(
        DateTime, nullable=False, default=func.now()
    )  # Call start time
    call_end_time = Column(DateTime, nullable=True)  # Call end time
    call_duration = Column(Float, nullable=True)  # Duration of the call in seconds

    # Call type field with enumerated choices
    call_type = Column(
        Enum(CallType, name="call_type"),
        nullable=False,
        default=CallType.outgoing,
    )

    # Call status field with enumerated choices
    call_status = Column(
        Enum(CallStatus, name="call_status"),
        nullable=True,
    )

    # Timestamps for creation and updates
    created_at = Column(DateTime, default=func.now())  # Record creation timestamp
    updated_at = Column(DateTime, onupdate=func.now())  # Record last updated timestamp
