"""SQLAlchemy models for rules, webhook events, and DM records."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DMStatus(str, enum.Enum):
    """Lifecycle states reserved for future DM processing."""

    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    SENT = "SENT"
    FAILED = "FAILED"


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    keyword: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    dm_message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProcessedEvent(Base):
    __tablename__ = "processed_events"

    event_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    event_type: Mapped[str] = mapped_column(String(100))
    comment_id: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[str] = mapped_column(String(255))
    username: Mapped[str] = mapped_column(String(255))
    post_id: Mapped[str] = mapped_column(String(255))
    comment_text: Mapped[str] = mapped_column(Text)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    processed: Mapped[bool] = mapped_column(default=False)
    duplicates_blocked: Mapped[int] = mapped_column(Integer, default=0, server_default="0")


class DMRecord(Base):
    __tablename__ = "dm_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_id: Mapped[str] = mapped_column(String(36), index=True)
    recipient_user_id: Mapped[str] = mapped_column(String(255))
    comment_id: Mapped[str] = mapped_column(String(255))
    status: Mapped[DMStatus] = mapped_column(Enum(DMStatus, name="dm_status"), default=DMStatus.QUEUED)
    attempts: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    dm_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
