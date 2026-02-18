"""
Configuration management for NEXIS platform
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "NEXIS Credit Trust Platform - India"
    PROJECT_DESCRIPTION: str = "Rule-based behavioral credit assessment system"
    API_V1_PREFIX: str = "/api/v1"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./nexis.db"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Assessment Configuration
    ASSESSMENT_VALIDITY_DAYS: int = 90
    MIN_DOCUMENTATION_MONTHS: int = 6
    TOTAL_RULES: int = 12
    MAX_SCORE_POINTS: int = 360
    MIN_SCORE: int = 420  # Realistic minimum for demo
    MAX_SCORE: int = 860  # Realistic maximum for demo
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # CORS - Allow all origins in development
    BACKEND_CORS_ORIGINS: list = ["*"]  # Allow all origins for development
    
    # India-specific settings
    COUNTRY: str = "India"
    CURRENCY: str = "INR"
    CURRENCY_SYMBOL: str = "₹"
    PHONE_PREFIX: str = "+91"
    TIMEZONE: str = "Asia/Kolkata"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
