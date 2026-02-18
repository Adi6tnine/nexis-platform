"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    """User profile and consent tracking"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    
    # Authentication
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Consent tracking
    consent_given = Column(Boolean, default=False)
    consent_timestamp = Column(DateTime(timezone=True))
    
    # Profile
    profile_completed = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BehavioralData(Base):
    """Alternative credit data points"""
    __tablename__ = "behavioral_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    
    # Utility Payment Data
    utility_payment_months = Column(Integer, default=0)  # Consecutive on-time months
    utility_payment_consistency = Column(Float, default=0.0)  # 0-1 score
    
    # Digital Transaction Data
    monthly_transaction_count = Column(Integer, default=0)
    transaction_regularity_score = Column(Float, default=0.0)  # 0-1
    spending_volatility = Column(Float, default=0.0)  # Lower is better
    
    # Savings Behavior
    avg_month_end_balance = Column(Float, default=0.0)
    savings_growth_rate = Column(Float, default=0.0)
    withdrawal_discipline_score = Column(Float, default=0.0)  # 0-1
    
    # Income Consistency
    income_regularity_score = Column(Float, default=0.0)  # 0-1
    income_stability_months = Column(Integer, default=0)
    
    # Account Information
    account_tenure_months = Column(Integer, default=0)
    address_stability_years = Column(Float, default=0.0)
    
    # Discretionary Spending
    discretionary_income_ratio = Column(Float, default=0.0)  # Percentage
    
    # Metadata
    data_collection_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CreditScore(Base):
    """Credit trust score results"""
    __tablename__ = "credit_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    
    # Score
    trust_score = Column(Integer, nullable=False)  # 300-900
    risk_level = Column(String, nullable=False)  # Low, Moderate, High
    risk_category = Column(String, nullable=False)  # For internal use
    
    # Rule-based metrics
    assessment_strength = Column(String)  # Strong, Moderate, Weak
    rule_match_level = Column(String)  # High, Medium, Low
    rules_evaluated = Column(Integer)
    rules_satisfied = Column(Integer)
    rules_partial = Column(Integer)
    rules_not_met = Column(Integer)
    total_points = Column(Integer)
    max_points = Column(Integer)
    
    # Validity
    scored_at = Column(DateTime(timezone=True), server_default=func.now())
    valid_until = Column(DateTime(timezone=True))  # scored_at + 90 days


class Explanation(Base):
    """Rule-based explanations for scores"""
    __tablename__ = "explanations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    score_id = Column(Integer, index=True)
    
    # Factor explanations (JSON structure)
    positive_factors = Column(JSON)  # List of positive contributors
    neutral_factors = Column(JSON)   # List of neutral factors
    negative_factors = Column(JSON)  # List of negative contributors
    
    # Rule evaluation results (for audit)
    rule_results = Column(JSON)  # Complete rule evaluation data
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ImprovementPlan(Base):
    """Personalized improvement recommendations"""
    __tablename__ = "improvement_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    
    # Recommendations (JSON array)
    recommendations = Column(JSON)  # List of actionable steps
    
    # Potential impact
    estimated_score_increase = Column(Integer)  # Total potential gain
    
    # Metadata
    generated_at = Column(DateTime(timezone=True), server_default=func.now())


class LenderDecision(Base):
    """Lender decision tracking (audit trail)"""
    __tablename__ = "lender_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    lender_id = Column(String, index=True)
    
    # System Assessment Summary
    assessment_classification = Column(String)  # Low Risk, Moderate Risk, High Risk
    assessment_strength = Column(String)  # Strong, Moderate, Weak
    rule_match_level = Column(String)  # High, Medium, Low
    
    # Human Decision
    human_decision = Column(String)  # approve, request_more_data, decline
    decision_justification = Column(Text)  # Required written justification
    
    # Loan details (if applicable)
    loan_amount = Column(Float)
    interest_rate = Column(Float)
    term_months = Column(Integer)
    
    # Timestamps
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())
    decided_at = Column(DateTime(timezone=True))
