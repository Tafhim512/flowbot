"""
Database engine and session factory.
Defaults to SQLite; swap to PostgreSQL by changing DATABASE_URL in .env.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# ---------- Engine ----------
# SQLite needs check_same_thread=False for FastAPI (multi-threaded)
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=(settings.APP_ENV == "development"),  # SQL logging in dev
)

# ---------- Session ----------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------- Base class for ORM models ----------
Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
