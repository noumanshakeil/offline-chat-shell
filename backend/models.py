from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base

def utcnow(): return datetime.utcnow()

class OfflineMessage(Base):
    __tablename__ = "offline_messages"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    role: Mapped[str] = mapped_column(String(16), default="user")
    content: Mapped[str] = mapped_column(Text)
    sync_status: Mapped[str] = mapped_column(String(16), default="pending", index=True)  # pending | synced
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    synced_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
