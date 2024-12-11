from uuid import uuid4

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Float

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.database import Base

import enum


class CallType(str, enum.Enum):
    incoming = "incoming"
    outgoing = "outgoing"
    missed = "missed"
    rejected = "rejected"


class CallStatus(str, enum.Enum):
    completed = "completed"
    failed = "failed"
    no_answer = "no_answer"
    busy = "busy"


class CallLog(Base):
    __tablename__ = "call_logs"

    call_log_id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )

    caller_phonenumber = Column(
        UUID(as_uuid=True), ForeignKey("phonenumbers.phonenumber_id"), nullable=False
    )
    receiver_phonenumber = Column(
        UUID(as_uuid=True), ForeignKey("phonenumbers.phonenumber_id"), nullable=False
    )

    call_start_time = Column(DateTime, nullable=False, default=func.now())
    call_end_time = Column(DateTime, nullable=True)
    call_duration = Column(Float, nullable=True)  # Duration in seconds

    call_type = Column(Enum(CallType, name="call_type"), nullable=False, default=CallType.outgoing)  # Use Python Enum
    call_status = Column(Enum(CallStatus, name="call_status"), nullable=True)  # Use Python Enum

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
