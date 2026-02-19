"""
Health Assessment Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.health_assessment import HealthAssessment
from app.schemas.health_assessment import (
    HealthAssessmentCreate,
    HealthAssessmentUpdate,
    HealthAssessmentResponse
)

router = APIRouter()

@router.post("/", response_model=HealthAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    assessment_data: HealthAssessmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create or update health assessment (12-question form)
    """
    # Check if assessment already exists
    existing = db.query(HealthAssessment).filter(
        HealthAssessment.user_id == current_user.id
    ).first()
    
    if existing:
        # Update existing assessment
        for key, value in assessment_data.dict().items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing
    
    # Create new assessment
    new_assessment = HealthAssessment(
        user_id=current_user.id,
        **assessment_data.dict()
    )
    
    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)
    
    return new_assessment

@router.get("/", response_model=HealthAssessmentResponse)
async def get_assessment(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's health assessment
    """
    assessment = db.query(HealthAssessment).filter(
        HealthAssessment.user_id == current_user.id
    ).first()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health assessment not found. Please complete the assessment first."
        )
    
    return assessment

@router.put("/", response_model=HealthAssessmentResponse)
async def update_assessment(
    assessment_data: HealthAssessmentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update health assessment
    """
    assessment = db.query(HealthAssessment).filter(
        HealthAssessment.user_id == current_user.id
    ).first()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health assessment not found"
        )
    
    # Update fields
    for key, value in assessment_data.dict(exclude_unset=True).items():
        setattr(assessment, key, value)
    
    db.commit()
    db.refresh(assessment)
    
    return assessment
