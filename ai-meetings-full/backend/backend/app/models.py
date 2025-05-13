from sqlalchemy import String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .db import Base
from typing import Optional


class Meeting(Base):
    __tablename__ = "meetings"
    id: Mapped[int]           = mapped_column(primary_key=True, index=True)
    title: Mapped[str]        = mapped_column(String(200))
    transcript: Mapped[str]   = mapped_column(Text)
    summary: Mapped[str]      = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    action_items = relationship("ActionItem", back_populates="meeting")
    decisions    = relationship("Decision", back_populates="meeting")

class ActionItem(Base):
    __tablename__ = "action_items"
    id: Mapped[int]          = mapped_column(primary_key=True)
    meeting_id: Mapped[int]  = mapped_column(ForeignKey("meetings.id"))
    description: Mapped[str] = mapped_column(Text)
    owner: Mapped[str]       = mapped_column(String(100))
    due_date: Mapped[Optional[str]] = mapped_column(String(50))
    done: Mapped[bool]       = mapped_column(Boolean, default=False)

    meeting = relationship("Meeting", back_populates="action_items")

class Decision(Base):
    __tablename__ = "decisions"
    id: Mapped[int]          = mapped_column(primary_key=True)
    meeting_id: Mapped[int]  = mapped_column(ForeignKey("meetings.id"))
    text: Mapped[str]        = mapped_column(Text)

    meeting = relationship("Meeting", back_populates="decisions")
