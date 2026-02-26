"""
API endpoint for business management.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.business import Business
from app.schemas.business import BusinessCreate, BusinessResponse


router = APIRouter()


@router.post("/businesses", response_model=BusinessResponse)
def create_business(business: BusinessCreate, db: Session = Depends(get_db)):
    """
    Create a new business in the system.
    """
    db_business = Business(**business.model_dump())
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


@router.get("/businesses", response_model=List[BusinessResponse])
def get_businesses(db: Session = Depends(get_db)):
    """
    Get all businesses in the system.
    """
    return db.query(Business).all()


@router.get("/businesses/{business_id}", response_model=BusinessResponse)
def get_business(business_id: str, db: Session = Depends(get_db)):
    """
    Get a specific business by ID.
    """
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business


@router.delete("/businesses/{business_id}")
def delete_business(business_id: str, db: Session = Depends(get_db)):
    """
    Delete a specific business by ID.
    """
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    db.delete(business)
    db.commit()
    return {"message": "Business deleted successfully"}
