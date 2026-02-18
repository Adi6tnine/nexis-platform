"""
API Routes for NEXIS Platform
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
import pandas as pd
import uuid

from ..db.database import get_db
from ..db import models
from .. import schemas
from ..rules.scoring_engine import ScoringEngine
from ..rules.explainability import ExplainabilityEngine
from ..rules.completion_pathway import CompletionPathwayGenerator
from ..core.config import settings
from ..core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    get_current_user
)

router = APIRouter()

# Global scoring engine instance
scoring_engine = ScoringEngine()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


# ============= AUTHENTICATION ROUTES =============

@router.post("/auth/register", response_model=schemas.AuthResponse)
@limiter.limit("3/hour")
async def register(
    request: Request,
    user_data: schemas.RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user account
    """
    # Check if user already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user_data.email
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_id = f"NEX-{uuid.uuid4().hex[:8].upper()}"
    hashed_password = get_password_hash(user_data.password)
    
    new_user = models.User(
        user_id=user_id,
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        hashed_password=hashed_password,
        is_active=True,
        is_verified=False,
        profile_completed=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user_id, "email": user_data.email}
    )
    
    return schemas.AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user_id,
        email=user_data.email,
        name=user_data.name,
        message="Registration successful"
    )


@router.post("/auth/login", response_model=schemas.AuthResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    credentials: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with email and password
    """
    # Find user
    user = db.query(models.User).filter(
        models.User.email == credentials.email
    ).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.user_id, "email": user.email}
    )
    
    return schemas.AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.user_id,
        email=user.email,
        name=user.name,
        message="Login successful"
    )


@router.get("/auth/me", response_model=schemas.UserProfileResponse)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user profile
    """
    user = db.query(models.User).filter(
        models.User.user_id == current_user["user_id"]
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get latest score if exists
    latest_score = db.query(models.CreditScore).filter(
        models.CreditScore.user_id == user.user_id
    ).order_by(models.CreditScore.scored_at.desc()).first()
    
    return schemas.UserProfileResponse(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        phone=user.phone,
        consent_given=user.consent_given,
        profile_completed=user.profile_completed,
        has_score=latest_score is not None,
        trust_score=latest_score.trust_score if latest_score else None,
        risk_level=latest_score.risk_level if latest_score else None,
        last_scored_at=latest_score.scored_at if latest_score else None,
        created_at=user.created_at
    )


@router.post("/auth/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout (client should discard token)
    """
    return {"message": "Logout successful. Please discard your access token."}


# ============= CONSENT & SCORING ROUTES =============


@router.post("/consent", response_model=schemas.ConsentResponse)
@limiter.limit("3/minute")
async def submit_consent(
    request: Request,
    consent: schemas.ConsentRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit user consent for credit analysis (requires authentication)
    
    - Validates consent
    - Updates user record
    - Returns confirmation
    """
    if not consent.consent_given:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consent must be explicitly given to proceed"
        )
    
    # Get authenticated user
    user = db.query(models.User).filter(
        models.User.user_id == current_user["user_id"]
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update consent
    user.consent_given = True
    user.consent_timestamp = datetime.utcnow()
    user.profile_completed = True
    db.commit()
    
    return schemas.ConsentResponse(
        user_id=user.user_id,
        message="Consent recorded successfully. You may now proceed to credit scoring.",
        consent_timestamp=datetime.utcnow(),
        next_step="proceed_to_scoring"
    )


@router.post("/score", response_model=schemas.ScoreResponse)
@limiter.limit("5/minute")
async def calculate_score(
    request: Request,
    score_request: schemas.ScoreRequest,
    db: Session = Depends(get_db)
):
    """
    Calculate credit trust score using rule-based assessment
    
    - Validates user consent
    - Applies behavioral rules
    - Stores results
    - Returns score and assessment metrics
    """
    # Verify user exists and has consent
    user = db.query(models.User).filter(
        models.User.user_id == score_request.user_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please submit consent first."
        )
    
    if not user.consent_given:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User consent not given"
        )
    
    # Store behavioral data
    behavioral_data = models.BehavioralData(
        user_id=score_request.user_id,
        **score_request.behavioral_data.model_dump()
    )
    db.add(behavioral_data)
    db.commit()
    
    # Calculate score using rule-based engine
    raw_data = score_request.behavioral_data.model_dump()
    score_result = scoring_engine.calculate_score(raw_data)
    
    # Calculate assessment strength
    documentation_months = raw_data.get('account_tenure_months', 0)
    assessment_strength = scoring_engine.get_assessment_strength(raw_data, documentation_months)
    rule_match_level = scoring_engine.get_rule_match_level(
        score_result['rules_satisfied'],
        score_result['rules_evaluated']
    )
    
    # Determine risk color
    if score_result['trust_score'] >= 700:
        risk_color = 'green'
    elif score_result['trust_score'] >= 550:
        risk_color = 'yellow'
    else:
        risk_color = 'red'
    
    # Calculate validity period
    scored_at = datetime.utcnow()
    valid_until = scored_at + timedelta(days=settings.ASSESSMENT_VALIDITY_DAYS)
    
    # Store score
    score_record = models.CreditScore(
        user_id=score_request.user_id,
        trust_score=score_result['trust_score'],
        risk_level=score_result['risk_level'],
        risk_category=score_result['risk_level'],
        assessment_strength=assessment_strength,
        rule_match_level=rule_match_level,
        rules_evaluated=score_result['rules_evaluated'],
        rules_satisfied=score_result['rules_satisfied'],
        rules_partial=score_result['rules_partial'],
        rules_not_met=score_result['rules_not_met'],
        total_points=score_result['total_points'],
        max_points=score_result['max_points'],
        scored_at=scored_at,
        valid_until=valid_until
    )
    db.add(score_record)
    
    # Generate and store explanation
    factors = ExplainabilityEngine.generate_factors(score_result['rule_results'])
    
    positive = [f for f in factors if f['type'] == 'positive']
    neutral = [f for f in factors if f['type'] == 'neutral']
    negative = [f for f in factors if f['type'] == 'negative']
    
    explanation_record = models.Explanation(
        user_id=score_request.user_id,
        score_id=score_record.id,
        positive_factors=positive,
        neutral_factors=neutral,
        negative_factors=negative,
        rule_results=score_result['rule_results']
    )
    db.add(explanation_record)
    
    # Generate improvement plan
    recommendations = CompletionPathwayGenerator.generate_recommendations(
        score_result['rule_results'],
        score_result['trust_score']
    )
    
    estimated_new_score = CompletionPathwayGenerator.calculate_potential_score(
        score_result['trust_score'],
        recommendations
    )
    
    total_potential_increase = estimated_new_score - score_result['trust_score']
    
    improvement_record = models.ImprovementPlan(
        user_id=score_request.user_id,
        recommendations=recommendations,
        estimated_score_increase=total_potential_increase
    )
    db.add(improvement_record)
    
    db.commit()
    
    return schemas.ScoreResponse(
        user_id=score_request.user_id,
        trust_score=score_result['trust_score'],
        risk_level=score_result['risk_level'],
        risk_color=risk_color,
        assessment_strength=assessment_strength,
        rule_match_level=rule_match_level,
        rules_evaluated=score_result['rules_evaluated'],
        rules_satisfied=score_result['rules_satisfied'],
        rules_partial=score_result['rules_partial'],
        rules_not_met=score_result['rules_not_met'],
        total_points=score_result['total_points'],
        max_points=score_result['max_points'],
        scored_at=scored_at,
        valid_until=valid_until,
        message=f"Your credit trust assessment has been completed. Assessment Strength: {assessment_strength}."
    )


@router.get("/explainability/{user_id}", response_model=schemas.ExplainabilityResponse)
async def get_explainability(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed score explanation with rule-based breakdown
    
    - Returns rule evaluation results
    - Human-readable explanations
    - Assessment metrics
    """
    # Get latest explanation
    explanation = db.query(models.Explanation).filter(
        models.Explanation.user_id == user_id
    ).order_by(models.Explanation.created_at.desc()).first()
    
    if not explanation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No explanation found. Please calculate score first."
        )
    
    # Get latest score
    score = db.query(models.CreditScore).filter(
        models.CreditScore.user_id == user_id
    ).order_by(models.CreditScore.scored_at.desc()).first()
    
    # Combine all factors
    all_factors = (
        explanation.positive_factors +
        explanation.neutral_factors +
        explanation.negative_factors
    )
    
    return schemas.ExplainabilityResponse(
        user_id=user_id,
        trust_score=score.trust_score,
        factors=all_factors,
        assessment_strength=score.assessment_strength,
        rule_match_level=score.rule_match_level,
        rules_evaluated=score.rules_evaluated,
        rules_satisfied=score.rules_satisfied,
        rules_partial=score.rules_partial,
        rules_not_met=score.rules_not_met,
        total_points=score.total_points,
        max_points=score.max_points,
        valid_until=score.valid_until,
        explanation_generated_at=explanation.created_at
    )


@router.get("/improvement/{user_id}", response_model=schemas.ImprovementResponse)
async def get_improvement_plan(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get personalized rule completion pathway
    
    - Specific actions to satisfy rules
    - Fixed score impacts
    - Deterministic timeframes
    """
    # Get latest improvement plan
    plan = db.query(models.ImprovementPlan).filter(
        models.ImprovementPlan.user_id == user_id
    ).order_by(models.ImprovementPlan.generated_at.desc()).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No improvement plan found. Please calculate score first."
        )
    
    # Get current score
    score = db.query(models.CreditScore).filter(
        models.CreditScore.user_id == user_id
    ).order_by(models.CreditScore.scored_at.desc()).first()
    
    target_score = min(score.trust_score + plan.estimated_score_increase, 900)
    estimated_new_score = min(score.trust_score + plan.estimated_score_increase, 900)
    
    return schemas.ImprovementResponse(
        user_id=user_id,
        current_score=score.trust_score,
        target_score=target_score,
        recommendations=plan.recommendations,
        total_potential_increase=plan.estimated_score_increase,
        estimated_new_score=estimated_new_score,
        generated_at=plan.generated_at
    )


@router.get("/roadmap/{user_id}", response_model=schemas.RoadmapResponse)
async def get_roadmap(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get improvement roadmap with rule completion steps
    """
    # Get improvement plan
    plan = db.query(models.ImprovementPlan).filter(
        models.ImprovementPlan.user_id == user_id
    ).order_by(models.ImprovementPlan.generated_at.desc()).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No plan found"
        )
    
    # Convert recommendations to roadmap steps
    roadmap = []
    for i, rec in enumerate(plan.recommendations[:3]):  # Top 3 recommendations
        status = "ongoing" if i == 0 else "next" if i == 1 else "future"
        roadmap.append({
            'title': rec['action'],
            'description': f"{rec['description']} - Will add +{rec['score_impact']} points",
            'status': status
        })
    
    return schemas.RoadmapResponse(
        user_id=user_id,
        roadmap=roadmap
    )


@router.get("/lender-view/{user_id}", response_model=schemas.LenderViewResponse)
async def get_lender_view(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Lender decision support interface
    
    - System assessment summary (NOT final decision)
    - Key trust signals
    - Behavioral metrics
    - Human-in-the-loop required
    """
    # Get user
    user = db.query(models.User).filter(
        models.User.user_id == user_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get latest score
    score = db.query(models.CreditScore).filter(
        models.CreditScore.user_id == user_id
    ).order_by(models.CreditScore.scored_at.desc()).first()
    
    if not score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No score found for user"
        )
    
    # Get explanation
    explanation = db.query(models.Explanation).filter(
        models.Explanation.user_id == user_id
    ).order_by(models.Explanation.created_at.desc()).first()
    
    # Get behavioral data
    behavioral = db.query(models.BehavioralData).filter(
        models.BehavioralData.user_id == user_id
    ).order_by(models.BehavioralData.created_at.desc()).first()
    
    # Generate assessment classification (advisory only)
    if score.trust_score >= 700:
        assessment_class = "Low Risk"
        ai_rec_text = "Qualified with Guidance"
    elif score.trust_score >= 550:
        assessment_class = "Moderate Risk"
        ai_rec_text = "Request Additional Information"
    else:
        assessment_class = "High Risk"
        ai_rec_text = "High Risk - Proceed with Caution"
    
    # Top signals
    positive_factors = explanation.positive_factors if explanation else []
    negative_factors = explanation.negative_factors if explanation else []
    
    top_signal = positive_factors[0]['title'] if positive_factors else "Limited data"
    key_observation = negative_factors[0]['title'] if negative_factors else "No major concerns"
    
    # Behavioral metrics
    metrics = [
        schemas.BehavioralMetric(
            label="Spending Volatility",
            value=f"{behavioral.spending_volatility * 100:.0f}%" if behavioral else "N/A",
            status="Stable" if behavioral and behavioral.spending_volatility < 0.3 else "Moderate"
        ),
        schemas.BehavioralMetric(
            label="Account Tenure",
            value=f"{behavioral.account_tenure_months / 12:.1f} yrs" if behavioral else "N/A",
            status="Established" if behavioral and behavioral.account_tenure_months >= 24 else "New"
        ),
        schemas.BehavioralMetric(
            label="Discretionary Income Ratio",
            value=f"{behavioral.discretionary_income_ratio * 100:.0f}%" if behavioral else "N/A",
            status="Healthy" if behavioral and behavioral.discretionary_income_ratio >= 0.15 else "Limited"
        )
    ]
    
    return schemas.LenderViewResponse(
        user_id=user_id,
        name=user.name,
        trust_score=score.trust_score,
        risk_level=score.risk_level,
        assessment_classification=assessment_class,
        assessment_strength=score.assessment_strength,
        rule_match_level=score.rule_match_level,
        ai_recommendation_text=ai_rec_text,
        top_trust_signal=top_signal,
        key_observation=key_observation,
        behavioral_metrics=metrics,
        rules_evaluated=score.rules_evaluated,
        rules_satisfied=score.rules_satisfied,
        rules_partial=score.rules_partial,
        program_note="This candidate is part of the 'Credit-Invisible India' inclusion pilot under RBI's financial inclusion initiative. All lending decisions must be accompanied by written justification as per regulatory guidelines.",
        reviewed_at=datetime.utcnow()
    )


@router.post("/lender-decision", response_model=schemas.LenderDecisionResponse)
@limiter.limit("10/minute")
async def submit_lender_decision(
    request: Request,
    decision: schemas.LenderDecisionRequest,
    db: Session = Depends(get_db)
):
    """
    Record lender decision (audit trail)
    
    - Requires written justification
    - Logs assessment vs human decision
    - Compliance tracking
    """
    # Get latest score for assessment classification
    score = db.query(models.CreditScore).filter(
        models.CreditScore.user_id == decision.user_id
    ).order_by(models.CreditScore.scored_at.desc()).first()
    
    if not score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No score found for user"
        )
    
    # Determine assessment classification
    if score.trust_score >= 700:
        assessment_class = "Low Risk"
    elif score.trust_score >= 550:
        assessment_class = "Moderate Risk"
    else:
        assessment_class = "High Risk"
    
    # Record decision
    decision_record = models.LenderDecision(
        user_id=decision.user_id,
        lender_id=decision.lender_id,
        assessment_classification=assessment_class,
        assessment_strength=score.assessment_strength,
        rule_match_level=score.rule_match_level,
        human_decision=decision.decision,
        decision_justification=decision.justification,
        loan_amount=decision.loan_amount,
        interest_rate=decision.interest_rate,
        term_months=decision.term_months,
        reviewed_at=datetime.utcnow(),
        decided_at=datetime.utcnow()
    )
    
    db.add(decision_record)
    db.commit()
    
    return schemas.LenderDecisionResponse(
        decision_id=decision_record.id,
        message="Decision recorded successfully. Audit trail created.",
        recorded_at=decision_record.decided_at
    )
