"""
Pydantic schemas for message handling.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict


class MessageInput(BaseModel):
    """Input schema for incoming messages."""
    business_id: str
    session_id: str
    text: str


class MessageOutput(BaseModel):
    """Output schema for AI responses."""
    reply: str
    intent: str
    actions_taken: List[str]
    session_id: str


class ConversationTurn(BaseModel):
    """Schema for a single conversation turn (user or assistant)."""
    role: str
    content: str


class BusinessConfig(BaseModel):
    """Schema for business configuration loaded from YAML."""
    business: Dict[str, str]
    role: str
    greeting: str
    personality: Dict[str, str]
    services: List[str]
    rules: List[str]
    knowledge_dir: str
