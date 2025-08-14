# src\models\conversation.py

import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.db import Base
from src.models.user import User
from src.models.company import Company


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    module = Column(Text, nullable=False)  # ✅ changed from Enum(Module)
    thread_type = Column(Text, nullable=False)  # ✅ changed from Enum(ThreadType)
    context_id = Column(UUID(as_uuid=True), nullable=True)

    thread_id = Column(String, nullable=False, unique=True)  # ✅ added to match Drizzle

    stage = Column(Text, nullable=False)
    step = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships (if needed)
    user = relationship(User, back_populates="conversations", lazy="joined")
    company = relationship(Company, back_populates="conversations", lazy="joined")

    __table_args__ = (Index("ix_conversation_user_company_module", "user_id", "company_id", "module"),)
