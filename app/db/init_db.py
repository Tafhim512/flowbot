"""
Database initialisation — creates all tables on first run.
"""

from app.db.session import engine, Base

# Import all models so Base.metadata knows about them
from app.models import business, conversation, lead, action_log  # noqa: F401


def create_tables():
    """Create all tables that don't already exist."""
    Base.metadata.create_all(bind=engine)
