"""
Business model — one row per onboarded business.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime
from app.db.session import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    config_path = Column(String, nullable=False)  # path to YAML config
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def __repr__(self):
        return f"<Business {self.slug}>"
