# src\models\agent_session.py
import uuid
from datetime import datetime
from sqlalchemy import Text, DateTime, Index, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from ..core.db import Base

class AgentSession(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)

    step: Mapped[str] = mapped_column(Text, nullable=False, default="session_started")
    status: Mapped[str] = mapped_column(Text, nullable=False, default="active", index=True)
    memory: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

Index("ix_sessions_user_company", AgentSession.user_id, AgentSession.company_id)
Index("ix_sessions_conversation", AgentSession.conversation_id)