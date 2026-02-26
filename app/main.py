"""
FastAPI application entry point.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.init_db import create_tables

# Create all tables on startup
create_tables()

# Initialize FastAPI app
app = FastAPI(
    title="FlowBot AI Business Automation Platform",
    description="Config-driven AI automation backend for multiple businesses",
    version="1.0.0",
)

# Include routers
from app.api import messages, businesses, leads

app.include_router(messages.router, prefix="/api/v1", tags=["Messages"])
app.include_router(businesses.router, prefix="/api/v1", tags=["Businesses"])
app.include_router(leads.router, prefix="/api/v1", tags=["Leads"])


@app.get("/")
async def root():
    return {"message": "FlowBot AI Business Automation Platform"}
