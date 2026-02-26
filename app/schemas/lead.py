"""
Pydantic schemas for lead management.
"""

from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class LeadCreate(BaseModel):
    """Input schema for creating a new lead."""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    source: Optional[str] = None
    extra_data: Optional[Dict] = None


class LeadResponse(BaseModel):
    """Output schema for lead details."""
    id: str
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    source: Optional[str] = None
    extra_data: Optional[Dict] = None
    created_at: datetime

    class Config:
        from_attributes = True
