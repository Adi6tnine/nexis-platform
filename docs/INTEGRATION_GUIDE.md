# NEXIS Platform - Complete Integration Guide

## 🎯 Overview

This guide walks you through integrating the NEXIS frontend with the backend API.

## 📋 Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- 4GB RAM minimum
- 2GB disk space

## 🚀 Complete Setup (90-Day Production Ready)

### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env if needed

# Train ML model (takes ~30 seconds)
python train_model.py

# Start backend server
uvicorn app.main:app --reload
```

Backend will run at: `http://localhost:8000`

### Step 2: Frontend Setup

```bash
# Navigate to project root
cd ..

# Install frontend dependencies
npm install

# Configure API endpoint
cp .env.example .env
# Verify VITE_API_URL=http://localhost:8000/api/v1

# Start frontend
npm run dev
```

Frontend will run at: `http://localhost:3000`

### Step 3: Verify Integration

1. Open browser: `http://localhost:3000`
2. Click "Check My Credit Trust"
3. Backend should calculate real score
4. Verify all screens work with live data

## 🔌 Frontend Integration

### Update App.jsx to Use Real API

Replace the mock data section with API calls:

```javascript
import { api, SAMPLE_BEHAVIORAL_DATA } from './services/api';
import { useState, useEffect } from 'react';

// Inside your component:
const [userData, setUserData] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);

// Handle consent submission
const handleConsent = async (consentData) => {
  setLoading(true);
  setError(null);
  
  try {
    const response = await api.submitConsent(consentData);
    const userId = response.user_id;
    
    // Calculate score with sample data
    const scoreResponse = await api.calculateScore(
      userId,
      SAMPLE_BEHAVIORAL_DATA
    );
    
    setUserData({
      userId,
      ...scoreResponse
    });
    
    setCurrentScreen('dashboard');
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

// Fetch explainability
const fetchExplainability = async (userId) => {
  try {
    const data = await api.getExplainability(userId);
    return data.factors;
  } catch (err) {
    console.error('Failed to fetch explainability:', err);
    return [];
  }
};

// Fetch improvement plan
const fetchImprovementPlan = async (userId) => {
  try {
    const data = await api.getImprovementPlan(userId);
    return data.recommendations;
  } catch (err) {
    console.error('Failed to fetch improvement plan:', err);
    return [];
  }
};
```

### API Integration Points

#### 1. Consent Screen
```javascript
const ConsentScreen = ({ onNext }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    consent_given: false
  });

  const handleSubmit = async () => {
    try {
      const response = await api.submitConsent(formData);
      onNext(response.user_id);
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    // ... form UI
    <Button onClick={handleSubmit}>Check My Credit Trust</Button>
  );
};
```

#### 2. Dashboard
```javascript
const Dashboard = ({ userId, onNavigate }) => {
  const [scoreData, setScoreData] = useState(null);
  const [factors, setFactors] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      // Score is already calculated during consent
      // Fetch explainability
      const explainability = await api.getExplainability(userId);
      setFactors(explainability.factors);
    };
    
    loadData();
  }, [userId]);

  return (
    // ... render with real data
  );
};
```

#### 3. Explainability Detail
```javascript
const ExplainabilityDetail = ({ userId, onBack }) => {
  const [factors, setFactors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadExplanation = async () => {
      try {
        const data = await api.getExplainability(userId);
        setFactors(data.factors);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    
    loadExplanation();
  }, [userId]);

  if (loading) return <div>Loading explanation...</div>;

  return (
    // ... render factors
  );
};
```

#### 4. Improvement Plan
```javascript
const ImprovementPlan = ({ userId, onBack }) => {
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    const loadPlan = async () => {
      const data = await api.getImprovementPlan(userId);
      setRecommendations(data.recommendations);
    };
    
    loadPlan();
  }, [userId]);

  return (
    // ... render recommendations
  );
};
```

#### 5. Lender View
```javascript
const LenderView = ({ userId, onBack }) => {
  const [lenderData, setLenderData] = useState(null);

  useEffect(() => {
    const loadLenderView = async () => {
      const data = await api.getLenderView(userId);
      setLenderData(data);
    };
    
    loadLenderView();
  }, [userId]);

  const handleDecision = async (decision, justification) => {
    await api.submitLenderDecision({
      user_id: userId,
      lender_id: 'LENDER-001',
      decision,
      justification
    });
    
    alert('Decision recorded successfully');
  };

  return (
    // ... render lender interface
  );
};
```

## 🧪 Testing the Integration

### Test Flow 1: Complete User Journey

```bash
# 1. Start both servers
# Terminal 1: Backend
cd backend && uvicorn app.main:app --reload

# Terminal 2: Frontend
npm run dev

# 2. Open browser: http://localhost:3000
# 3. Fill consent form:
#    - Name: Test User
#    - Email: test@example.com
#    - Check consent box
# 4. Click "Check My Credit Trust"
# 5. Verify dashboard shows real score
# 6. Navigate through all screens
# 7. Check browser console for API calls
```

### Test Flow 2: API Direct Testing

```bash
# Test consent
curl -X POST http://localhost:8000/api/v1/consent \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "consent_given": true
  }'

# Save the user_id from response

# Test scoring
curl -X POST http://localhost:8000/api/v1/score \
  -H "Content-Type: application/json" \
  -d '{
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
  }'

# Test explainability
curl http://localhost:8000/api/v1/explainability/NEX-XXXXXXXX

# Test improvement plan
curl http://localhost:8000/api/v1/improvement/NEX-XXXXXXXX

# Test lender view
curl http://localhost:8000/api/v1/lender-view/NEX-XXXXXXXX
```

## 🔧 Troubleshooting

### Issue: CORS Error

**Symptom**: Browser console shows CORS policy error

**Solution**:
```python
# backend/app/core/config.py
BACKEND_CORS_ORIGINS: list = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000"
]
```

### Issue: Model Not Found

**Symptom**: API returns "Model not loaded"

**Solution**:
```bash
cd backend
python train_model.py
# Restart API server
```

### Issue: Database Error

**Symptom**: SQLAlchemy errors

**Solution**:
```bash
# Delete database and recreate
rm backend/nexis.db
# Restart API server (will recreate tables)
```

### Issue: Port Already in Use

**Symptom**: "Address already in use"

**Solution**:
```bash
# Find process using port
# Linux/Mac:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 📊 Demo User Profiles

### Profile 1: Excellent Credit (Score: 780-850)
```json
{
  "utility_payment_months": 24,
  "utility_payment_consistency": 0.98,
  "monthly_transaction_count": 60,
  "transaction_regularity_score": 0.92,
  "spending_volatility": 0.08,
  "avg_month_end_balance": 8000.0,
  "savings_growth_rate": 0.20,
  "withdrawal_discipline_score": 0.95,
  "income_regularity_score": 0.95,
  "income_stability_months": 36,
  "account_tenure_months": 60,
  "address_stability_years": 5.0,
  "discretionary_income_ratio": 0.30
}
```

### Profile 2: Good Credit (Score: 650-750)
```json
{
  "utility_payment_months": 14,
  "utility_payment_consistency": 0.88,
  "monthly_transaction_count": 40,
  "transaction_regularity_score": 0.80,
  "spending_volatility": 0.15,
  "avg_month_end_balance": 4000.0,
  "savings_growth_rate": 0.12,
  "withdrawal_discipline_score": 0.75,
  "income_regularity_score": 0.85,
  "income_stability_months": 18,
  "account_tenure_months": 30,
  "address_stability_years": 2.5,
  "discretionary_income_ratio": 0.22
}
```

### Profile 3: Fair Credit (Score: 500-650)
```json
{
  "utility_payment_months": 8,
  "utility_payment_consistency": 0.70,
  "monthly_transaction_count": 25,
  "transaction_regularity_score": 0.60,
  "spending_volatility": 0.35,
  "avg_month_end_balance": 1500.0,
  "savings_growth_rate": 0.05,
  "withdrawal_discipline_score": 0.55,
  "income_regularity_score": 0.65,
  "income_stability_months": 10,
  "account_tenure_months": 18,
  "address_stability_years": 1.5,
  "discretionary_income_ratio": 0.15
}
```

### Profile 4: Poor Credit (Score: 300-500)
```json
{
  "utility_payment_months": 3,
  "utility_payment_consistency": 0.45,
  "monthly_transaction_count": 12,
  "transaction_regularity_score": 0.35,
  "spending_volatility": 0.65,
  "avg_month_end_balance": 500.0,
  "savings_growth_rate": -0.05,
  "withdrawal_discipline_score": 0.30,
  "income_regularity_score": 0.40,
  "income_stability_months": 4,
  "account_tenure_months": 8,
  "address_stability_years": 0.8,
  "discretionary_income_ratio": 0.08
}
```

## 🚀 Production Deployment

### Environment Variables

**Backend (.env)**:
```bash
DATABASE_URL=postgresql://user:pass@db:5432/nexis
SECRET_KEY=<generate-secure-key>
ENVIRONMENT=production
BACKEND_CORS_ORIGINS=["https://nexis.example.com"]
```

**Frontend (.env)**:
```bash
VITE_API_URL=https://api.nexis.example.com/api/v1
```

### Docker Deployment

```bash
# Build and deploy
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Scale if needed
docker-compose up -d --scale backend=3
```

### Health Monitoring

```bash
# Check backend health
curl https://api.nexis.example.com/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "ml_model": "loaded",
  "environment": "production"
}
```

## 📈 Performance Optimization

### Backend
- Use PostgreSQL for production (not SQLite)
- Enable database connection pooling
- Cache model predictions (Redis)
- Use async database queries
- Implement rate limiting

### Frontend
- Enable code splitting
- Lazy load screens
- Cache API responses
- Optimize images
- Use CDN for static assets

## 🔒 Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Use HTTPS only
- [ ] Enable rate limiting
- [ ] Implement authentication
- [ ] Sanitize user inputs
- [ ] Enable CORS only for trusted origins
- [ ] Regular security audits
- [ ] Encrypt sensitive data
- [ ] Implement audit logging
- [ ] Regular backups

## 📞 Support

If you encounter issues:

1. Check logs: `docker-compose logs backend`
2. Verify API health: `curl http://localhost:8000/health`
3. Check browser console for frontend errors
4. Review API docs: `http://localhost:8000/docs`

## ✅ Integration Checklist

- [ ] Backend server running
- [ ] ML model trained
- [ ] Frontend server running
- [ ] API calls working
- [ ] Consent flow functional
- [ ] Score calculation working
- [ ] Explainability displaying
- [ ] Improvement plan showing
- [ ] Lender view accessible
- [ ] Error handling working
- [ ] Loading states implemented
- [ ] All screens navigable

## 🎉 Success Criteria

Your integration is complete when:

1. ✅ User can submit consent
2. ✅ Real credit score is calculated
3. ✅ SHAP explanations display correctly
4. ✅ Improvement recommendations are personalized
5. ✅ Lender view shows AI advisory
6. ✅ All API endpoints respond correctly
7. ✅ Error handling works gracefully
8. ✅ No console errors
9. ✅ Performance is acceptable (<2s for scoring)
10. ✅ Ready for demo/production

---

**Congratulations!** You now have a production-ready explainable credit scoring platform. 🚀
