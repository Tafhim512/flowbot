"""
Pydantic schemas for business management.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BusinessCreate(BaseModel):
    """Input schema for creating a new business."""
    name: str
    slug: str
    config_path: str


class BusinessResponse(BaseModel):
    """Output schema for business details."""
    id: str
    name: str
    slug: str
    config_path: str
    created_at: datetime

    class Config:
        from_attributes = True
