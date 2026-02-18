"""
Consent enforcement middleware
"""
from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..db import models


async def verify_consent(user_id: str) -> bool:
    """
    Verify user has given consent
    
    Args:
        user_id: User identifier
        
    Returns:
        True if consent given, raises HTTPException otherwise
    """
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(
            models.User.user_id == user_id
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.consent_given:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User consent required. Please submit consent first."
            )
        
        return True
    finally:
        db.close()
