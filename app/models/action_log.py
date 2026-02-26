"""
Action log model — records every automated action the system takes.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from app.db.session import Base


class ActionLog(Base):
    __tablename__ = "actions_log"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False, index=True)
    conversation_id = Column(
        String, ForeignKey("conversations.id"), nullable=True
    )
    action_type = Column(String, nullable=False)  # "reply", "create_lead", "send_email", etc.
    payload = Column(JSON, nullable=True)
    status = Column(String, default="completed")  # "completed", "failed", "pending"
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def __repr__(self):
        return f"<ActionLog {self.action_type} [{self.status}]>"
