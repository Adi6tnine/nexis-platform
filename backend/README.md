# NEXIS Backend - Credit Trust Platform

Production-ready backend for explainable alternative credit scoring.

## 🏗️ Architecture

```
backend/
├── app/
│   ├── api/              # API routes
│   ├── core/             # Configuration & security
│   ├── db/               # Database models & session
│   ├── ml/               # ML models & explainability
│   │   ├── model.py              # Credit trust model
│   │   ├── feature_engineering.py # Feature engineering
│   │   ├── explainability.py     # SHAP explanations
│   │   └── improvement.py        # Recommendations
│   ├── main.py           # FastAPI application
│   └── schemas.py        # Pydantic schemas
├── models/               # Trained ML models (generated)
├── train_model.py        # Model training script
├── requirements.txt      # Python dependencies
└── Dockerfile           # Container configuration
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Train ML Model

```bash
python train_model.py
```

This will:
- Generate 2000 synthetic training samples
- Train Random Forest classifier
- Create SHAP explainer
- Save models to `models/` directory

### 4. Start API Server

```bash
uvicorn app.main:app --reload
```

API will be available at: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

## 📊 ML Model Details

### Model Architecture
- **Algorithm**: Random Forest Classifier
- **Purpose**: Interpretable and stable credit risk prediction
- **Classes**: 3 risk categories (Low, Moderate, High)
- **Features**: 20 engineered features from behavioral data

### Feature Engineering

Raw behavioral data is transformed into ML features:

1. **Payment Consistency Score** (0-100)
   - Utility payment months × 2
   - Payment consistency × 50

2. **Transaction Stability Score** (0-100)
   - Normalized transaction count × 40
   - Transaction regularity × 40
   - Inverted volatility × 20

3. **Savings Discipline Index** (0-100)
   - Normalized balance × 40
   - Savings growth × 30
   - Withdrawal discipline × 30

4. **Volatility Index** (0-100)
   - Inverted spending volatility

5. **Income Regularity Flag** (binary)
   - Based on regularity score and stability months

6. **Tenure Score** (0-100)
   - Account tenure + address stability

7. **Financial Health Score** (composite)
   - Weighted combination of all scores

### Explainability (SHAP)

Every prediction includes SHAP values that explain:
- Which features contributed positively
- Which features contributed negatively
- Magnitude of each contribution

These are converted to human-readable explanations with NO technical jargon.

## 🔌 API Endpoints

### POST `/api/v1/consent`
Submit user consent for credit analysis.

**Request:**
```json
{
  "name": "Alex Rivera",
  "email": "alex@example.com",
  "phone": "+1234567890",
  "consent_given": true
}
```

**Response:**
```json
{
  "user_id": "NEX-A1B2C3D4",
  "message": "Consent recorded successfully",
  "consent_timestamp": "2026-02-17T10:00:00Z",
  "next_step": "proceed_to_scoring"
}
```

### POST `/api/v1/score`
Calculate credit trust score.

**Request:**
```json
{
  "user_id": "NEX-A1B2C3D4",
  "behavioral_data": {
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
```

**Response:**
```json
{
  "user_id": "NEX-A1B2C3D4",
  "trust_score": 742,
  "risk_level": "Low-Moderate",
  "risk_color": "text-emerald-500",
  "percentile": 84,
  "confidence": 0.89,
  "scored_at": "2026-02-17T10:05:00Z",
  "message": "Your credit trust score has been calculated."
}
```

### GET `/api/v1/explainability/{user_id}`
Get detailed score explanation with SHAP-based factors.

### GET `/api/v1/improvement/{user_id}`
Get personalized improvement recommendations.

### GET `/api/v1/roadmap/{user_id}`
Get step-by-step improvement roadmap.

### GET `/api/v1/lender-view/{user_id}`
Get lender decision support interface (AI advisory only).

### POST `/api/v1/lender-decision`
Record lender decision with justification (audit trail).

## 🔒 Security & Privacy

### Data Protection
- Personal identifiers are masked in logs
- Consent is explicitly tracked
- No sensitive attributes (caste, religion, gender) are used
- Clear audit trail for all decisions

### Authentication
- Token-based authentication (JWT)
- Configurable token expiration
- Password hashing with bcrypt

### Compliance
- GDPR-compliant data handling
- Explicit consent required
- Right to explanation (SHAP)
- Audit trail for all decisions

## 🧪 Testing

### Test API with curl

```bash
# Health check
curl http://localhost:8000/health

# Submit consent
curl -X POST http://localhost:8000/api/v1/consent \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "consent_given": true
  }'

# Calculate score (use user_id from consent response)
curl -X POST http://localhost:8000/api/v1/score \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

### Sample Request File

Create `sample_request.json`:
```json
{
  "user_id": "NEX-XXXXXXXX",
  "behavioral_data": {
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
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker build -t nexis-backend .

# Run container
docker run -p 8000:8000 nexis-backend

# Or use docker-compose
docker-compose up -d
```

### Production Deployment

For production, update `docker-compose.yml` to use PostgreSQL:

```yaml
services:
  backend:
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/nexis
    depends_on:
      - postgres
  
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: nexis
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: nexis
```

## 📈 Model Performance

Based on synthetic training data (2000 samples):
- **Train Accuracy**: ~95%
- **Test Accuracy**: ~92%
- **Features**: 20 engineered features
- **Classes**: 3 risk categories

### Risk Distribution
- Low Risk: 40% of population
- Moderate Risk: 40% of population
- High Risk: 20% of population

## 🔄 Model Retraining

To retrain with new data:

1. Update `generate_synthetic_training_data()` in `app/ml/model.py`
2. Run `python train_model.py`
3. Restart API server

For production, implement:
- Scheduled retraining pipeline
- Model versioning
- A/B testing framework
- Performance monitoring

## 🚨 Important Notes

### Human-in-the-Loop
- AI provides **advisory scores only**
- Final lending decisions require **human approval**
- All decisions must include **written justification**
- Audit trail is maintained for compliance

### Responsible AI
- Model is **explainable** (SHAP values)
- No discriminatory features used
- Transparent scoring methodology
- User-friendly explanations

### Data Requirements
- Minimum 6 months of behavioral data recommended
- More data = better accuracy
- Regular updates improve score accuracy

## 📞 Support

For issues or questions:
1. Check API docs: `http://localhost:8000/docs`
2. Review logs for errors
3. Verify model is trained: `ls models/`

## 📄 License

© 2026 NEXIS. All rights reserved.
