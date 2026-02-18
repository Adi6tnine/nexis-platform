"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime


# ============= AUTHENTICATION =============
class RegisterRequest(BaseModel):
    """User registration"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    password: str = Field(..., min_length=8, max_length=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alex Rivera",
                "email": "alex@example.com",
                "phone": "+1234567890",
                "password": "SecurePass123!"
            }
        }


class LoginRequest(BaseModel):
    """User login"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "alex@example.com",
                "password": "SecurePass123!"
            }
        }


class AuthResponse(BaseModel):
    """Authentication response"""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    name: str
    message: str


class UserProfileResponse(BaseModel):
    """User profile information"""
    user_id: str
    name: str
    email: str
    phone: Optional[str]
    consent_given: bool
    profile_completed: bool
    has_score: bool
    trust_score: Optional[int] = None
    risk_level: Optional[str] = None
    last_scored_at: Optional[datetime] = None
    created_at: datetime


# ============= CONSENT =============
class ConsentRequest(BaseModel):
    """User consent submission"""
    consent_given: bool = Field(..., description="Must be True to proceed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "consent_given": True
            }
        }


class ConsentResponse(BaseModel):
    """Consent confirmation"""
    user_id: str
    message: str
    consent_timestamp: datetime
    next_step: str = "proceed_to_scoring"


# ============= BEHAVIORAL DATA =============
class BehavioralDataInput(BaseModel):
    """Alternative credit data input"""
    # Utility Payments
    utility_payment_months: int = Field(ge=0, le=120, description="Consecutive on-time months")
    utility_payment_consistency: float = Field(ge=0.0, le=1.0)
    
    # Digital Transactions
    monthly_transaction_count: int = Field(ge=0)
    transaction_regularity_score: float = Field(ge=0.0, le=1.0)
    spending_volatility: float = Field(ge=0.0, le=1.0, description="Lower is better")
    
    # Savings
    avg_month_end_balance: float = Field(ge=0.0)
    savings_growth_rate: float = Field(ge=-1.0, le=1.0)
    withdrawal_discipline_score: float = Field(ge=0.0, le=1.0)
    
    # Income
    income_regularity_score: float = Field(ge=0.0, le=1.0)
    income_stability_months: int = Field(ge=0, le=120)
    
    # Account Info
    account_tenure_months: int = Field(ge=0, le=600)
    address_stability_years: float = Field(ge=0.0, le=50.0)
    
    # Spending
    discretionary_income_ratio: float = Field(ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "utility_payment_months": 14,
                "utility_payment_consistency": 0.95,
                "monthly_transaction_count": 45,
                "transaction_regularity_score": 0.88,
                "spending_volatility": 0.12,
                "avg_month_end_balance": 5000.0,
                "savings_growth_rate": 0.15,
                "withdrawal_discipline_score": 0.82,
                "income_regularity_score": 0.90,
                "income_stability_months": 18,
                "account_tenure_months": 38,
                "address_stability_years": 2.5,
                "discretionary_income_ratio": 0.22
            }
        }


# ============= SCORING =============
class ScoreRequest(BaseModel):
    """Request for credit trust scoring"""
    user_id: str
    behavioral_data: BehavioralDataInput


class ScoreResponse(BaseModel):
    """Credit trust score result"""
    user_id: str
    trust_score: int = Field(ge=300, le=900)
    risk_level: str
    risk_color: str
    assessment_strength: str = Field(..., description="Strong, Moderate, or Weak")
    rule_match_level: str = Field(..., description="High, Medium, or Low")
    rules_evaluated: int
    rules_satisfied: int
    rules_partial: int
    rules_not_met: int
    total_points: int
    max_points: int
    scored_at: datetime
    valid_until: datetime
    message: str


# ============= EXPLAINABILITY =============
class Factor(BaseModel):
    """Individual scoring factor"""
    id: int
    type: str = Field(..., description="positive, neutral, or negative")
    title: str
    description: str
    impact: str = Field(..., description="High, Medium, or Low")
    icon: str = Field(..., description="Icon name for frontend")
    rule_id: Optional[str] = None
    user_value: Optional[float] = None
    required_threshold: Optional[float] = None
    threshold_met: Optional[bool] = None
    points_earned: Optional[int] = None
    max_points: Optional[int] = None
    status: Optional[str] = None


class ExplainabilityResponse(BaseModel):
    """Detailed score explanation"""
    user_id: str
    trust_score: int
    factors: List[Factor]
    assessment_strength: str
    rule_match_level: str
    rules_evaluated: int
    rules_satisfied: int
    rules_partial: int
    rules_not_met: int
    total_points: int
    max_points: int
    valid_until: datetime
    explanation_generated_at: datetime


# ============= IMPROVEMENT PLAN =============
class Recommendation(BaseModel):
    """Single improvement recommendation"""
    rule_id: str
    rule_name: str
    action: str
    description: str
    current_value: float
    target_threshold: float
    gap: float
    gap_unit: str
    score_impact: int = Field(ge=0, le=150, description="Fixed score increase")
    timeframe: str
    difficulty: str = Field(..., description="Easy, Medium, or Hard")
    category: str
    status: str
    completion_criteria: str
    verification: str


class ImprovementResponse(BaseModel):
    """Personalized improvement plan"""
    user_id: str
    current_score: int
    target_score: int
    recommendations: List[Recommendation]
    total_potential_increase: int
    estimated_new_score: int
    generated_at: datetime


# ============= LENDER VIEW =============
class BehavioralMetric(BaseModel):
    """Single behavioral metric"""
    label: str
    value: str
    status: str


class LenderViewResponse(BaseModel):
    """Lender decision support interface"""
    user_id: str
    name: str
    trust_score: int
    risk_level: str
    
    # Assessment Summary (replaced AI recommendation)
    assessment_classification: str
    assessment_strength: str
    rule_match_level: str
    ai_recommendation_text: str  # Keep for backward compatibility, but rename in display
    
    # Top signals
    top_trust_signal: str
    key_observation: str
    
    # Behavioral metrics
    behavioral_metrics: List[BehavioralMetric]
    
    # Rule coverage
    rules_evaluated: int
    rules_satisfied: int
    rules_partial: int
    
    # Compliance
    program_note: str
    reviewed_at: datetime


class LenderDecisionRequest(BaseModel):
    """Lender decision submission"""
    user_id: str
    lender_id: str
    decision: str = Field(..., description="approve, request_more_data, or decline")
    justification: str = Field(..., min_length=20, description="Required written justification")
    loan_amount: Optional[float] = None
    interest_rate: Optional[float] = None
    term_months: Optional[int] = None


class LenderDecisionResponse(BaseModel):
    """Decision confirmation"""
    decision_id: int
    message: str
    recorded_at: datetime


# ============= ROADMAP =============
class RoadmapStep(BaseModel):
    """Single roadmap step"""
    title: str
    description: str
    status: str = Field(..., description="ongoing, next, or future")


class RoadmapResponse(BaseModel):
    """User improvement roadmap"""
    user_id: str
    roadmap: List[RoadmapStep]
