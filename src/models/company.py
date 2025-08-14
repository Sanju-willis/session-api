# src\models\company.py

import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.core.db import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)

    industry = Column(String, default="", nullable=False)
    size = Column(String, default="", nullable=False)
    type = Column(String, default="", nullable=False)
    target_market = Column(String, default="", nullable=False)
    address = Column(String, default="", nullable=False)
    website = Column(String, default="", nullable=False)
    website_domain = Column(String, default="", nullable=False)

    social_links = Column(JSON, default=list)
    brand_guide_url = Column(String, default="", nullable=False)
    logo_assets_url = Column(String, default="", nullable=False)
    press_kit_url = Column(String, default="", nullable=False)
    portfolio_url = Column(String, default="", nullable=False)
    content_library_url = Column(String, default="", nullable=False)
    product_pages = Column(JSON, default=list)
    description = Column(String, default="", nullable=False)
    target_audience = Column(String, default="", nullable=False)

    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
