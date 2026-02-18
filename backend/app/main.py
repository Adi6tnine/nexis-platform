"""
NEXIS Credit Trust Platform - Main Application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
import time

from .core.config import settings
from .db.database import engine
from .db import models
from .api.routes import router, scoring_engine
from .middleware.error_handler import (
    validation_exception_handler,
    database_exception_handler,
    general_exception_handler
)
from .middleware.logging import setup_logging

# Setup logging
logger = setup_logging()

# Setup rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup: Validate environment and create tables
    print("🚀 Starting NEXIS Platform...")
    
    # Validate required environment variables
    required_vars = ["DATABASE_URL", "SECRET_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("   Using default values for development. Set these for production!")
    else:
        print("✅ Environment variables validated")
    
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Initialize scoring engine
    print("✅ Rule-based scoring engine initialized")
    print(f"   - Total Rules: {len(scoring_engine.RULES)}")
    print(f"   - Maximum Points: {scoring_engine.MAX_POINTS}")
    print("   - Assessment Type: Deterministic Rule-Based")
    
    print("✅ NEXIS Platform ready!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down NEXIS Platform...")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Rule-Based Behavioral Credit Assessment Platform for Financial Inclusion",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiter state
app.state.limiter = limiter

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response

# CORS middleware - Must be added BEFORE routes
# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when allow_origins is ["*"]
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include API routes
app.include_router(router, prefix=settings.API_V1_PREFIX, tags=["credit-scoring"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "NEXIS Credit Trust Platform API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    scoring_engine_ready = scoring_engine is not None
    
    return {
        "status": "healthy" if scoring_engine_ready else "degraded",
        "database": "connected",
        "scoring_engine": "ready" if scoring_engine_ready else "not_initialized",
        "assessment_type": "rule-based",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health/engine")
async def engine_health_check():
    """Scoring engine health check"""
    if scoring_engine is None:
        return {
            "status": "not_initialized",
            "message": "Scoring engine not initialized."
        }
    
    return {
        "status": "ready",
        "engine_type": "Rule-Based Deterministic",
        "total_rules": len(scoring_engine.RULES),
        "max_points": scoring_engine.MAX_POINTS,
        "assessment_method": "Predefined behavioral rules with fixed thresholds"
    }


@app.get("/health/cors")
async def cors_check():
    """CORS configuration check"""
    return {
        "status": "ok",
        "allowed_origins": settings.BACKEND_CORS_ORIGINS,
        "message": "CORS is configured. If you see this, CORS is working!"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False
    )
