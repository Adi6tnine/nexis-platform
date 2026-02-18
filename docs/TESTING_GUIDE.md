# NEXIS Platform - Testing Guide

## 🧪 Testing Strategy

This guide covers all testing scenarios for the NEXIS platform.

## 📋 Test Categories

1. **Unit Tests** - Individual components
2. **Integration Tests** - API endpoints
3. **End-to-End Tests** - Complete user flows
4. **Performance Tests** - Load and stress testing
5. **Security Tests** - Vulnerability assessment

## 🚀 Quick Test

### Verify Installation

```bash
# Test backend
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python -c "import app; print('✅ Backend imports OK')"

# Test model
python -c "from app.ml.model import CreditTrustModel; print('✅ ML model OK')"

# Test frontend
cd ..
npm run build
echo "✅ Frontend builds OK"
```

## 🔌 API Testing

### 1. Health Check

```bash
# Start backend first
cd backend && uvicorn app.main:app --reload

# In another terminal
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "ml_model": "loaded",
  "environment": "development"
}
```

### 2. Consent Flow

```bash
curl -X POST http://localhost:8000/api/v1/consent \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+1234567890",
    "consent_given": true
  }'
```

**Expected Response:**
```json
{
  "user_id": "NEX-XXXXXXXX",
  "message": "Consent recorded successfully...",
  "consent_timestamp": "2026-02-17T...",
  "next_step": "proceed_to_scoring"
}
```

**Save the `user_id` for subsequent tests!**

### 3. Score Calculation

Create `test_score.json`:
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

```bash
curl -X POST http://localhost:8000/api/v1/score \
  -H "Content-Type: application/json" \
  -d @test_score.json
```

**Expected Response:**
```json
{
  "user_id": "NEX-XXXXXXXX",
  "trust_score": 742,
  "risk_level": "Low-Moderate",
  "risk_color": "text-emerald-500",
  "percentile": 84,
  "confidence": 0.89,
  "scored_at": "2026-02-17T...",
  "message": "Your credit trust score has been calculated..."
}
```

### 4. Explainability

```bash
curl http://localhost:8000/api/v1/explainability/NEX-XXXXXXXX
```

**Verify:**
- ✅ Returns list of factors
- ✅ Each factor has type (positive/neutral/negative)
- ✅ Descriptions are human-readable
- ✅ Impact levels are present

### 5. Improvement Plan

```bash
curl http://localhost:8000/api/v1/improvement/NEX-XXXXXXXX
```

**Verify:**
- ✅ Returns recommendations
- ✅ Each has estimated score increase
- ✅ Difficulty levels present
- ✅ Timeframes specified

### 6. Lender View

```bash
curl http://localhost:8000/api/v1/lender-view/NEX-XXXXXXXX
```

**Verify:**
- ✅ AI recommendation present
- ✅ Behavioral metrics included
- ✅ Top signals identified
- ✅ Compliance note present

## 🌐 Frontend Testing

### Manual Testing Checklist

#### Consent Screen
- [ ] Form validation works
- [ ] All fields required
- [ ] Consent checkbox required
- [ ] Submit button disabled until valid
- [ ] Success redirects to dashboard

#### Dashboard
- [ ] Score gauge displays correctly
- [ ] Score animates on load
- [ ] Risk level shows correct color
- [ ] Factors display (top 3)
- [ ] Roadmap section visible
- [ ] Navigation works

#### Explainability Detail
- [ ] All factors display
- [ ] Icons render correctly
- [ ] Impact badges show
- [ ] AI insights present
- [ ] Back button works

#### Improvement Plan
- [ ] Recommendations display
- [ ] Score increases shown
- [ ] Difficulty levels visible
- [ ] Descriptions clear
- [ ] Back button works

#### Lender View
- [ ] User info displays
- [ ] AI recommendation shows
- [ ] Metrics table renders
- [ ] Decision buttons present
- [ ] Compliance note visible

### Browser Testing

Test in:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Chrome
- [ ] Mobile Safari

### Responsive Testing

Test at:
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

## 🔬 Test Scenarios

### Scenario 1: Excellent Credit Profile

**Input:**
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

**Expected:**
- Score: 780-850
- Risk: Low
- Mostly positive factors
- Minimal improvement needed

### Scenario 2: Poor Credit Profile

**Input:**
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

**Expected:**
- Score: 300-500
- Risk: High
- Mostly negative factors
- Multiple improvement recommendations

### Scenario 3: Edge Cases

#### Minimum Values
```json
{
  "utility_payment_months": 0,
  "utility_payment_consistency": 0.0,
  "monthly_transaction_count": 0,
  "transaction_regularity_score": 0.0,
  "spending_volatility": 0.0,
  "avg_month_end_balance": 0.0,
  "savings_growth_rate": -1.0,
  "withdrawal_discipline_score": 0.0,
  "income_regularity_score": 0.0,
  "income_stability_months": 0,
  "account_tenure_months": 0,
  "address_stability_years": 0.0,
  "discretionary_income_ratio": 0.0
}
```

**Expected:**
- Score: 300 (minimum)
- No crashes
- Graceful handling

#### Maximum Values
```json
{
  "utility_payment_months": 120,
  "utility_payment_consistency": 1.0,
  "monthly_transaction_count": 200,
  "transaction_regularity_score": 1.0,
  "spending_volatility": 0.0,
  "avg_month_end_balance": 50000.0,
  "savings_growth_rate": 1.0,
  "withdrawal_discipline_score": 1.0,
  "income_regularity_score": 1.0,
  "income_stability_months": 120,
  "account_tenure_months": 600,
  "address_stability_years": 50.0,
  "discretionary_income_ratio": 1.0
}
```

**Expected:**
- Score: 850-900
- No crashes
- Graceful handling

## ⚡ Performance Testing

### Load Testing with Apache Bench

```bash
# Install Apache Bench
# Ubuntu: sudo apt-get install apache2-utils
# Mac: brew install httpd

# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Test score endpoint (requires auth)
ab -n 100 -c 5 -p test_score.json -T application/json \
  http://localhost:8000/api/v1/score
```

**Expected:**
- Requests per second: >100
- Mean response time: <200ms
- No failed requests

### Stress Testing

```bash
# Gradually increase load
for i in {1..10}; do
  ab -n $((i * 100)) -c $((i * 2)) http://localhost:8000/health
  sleep 5
done
```

**Monitor:**
- CPU usage
- Memory usage
- Response times
- Error rates

## 🔒 Security Testing

### 1. Input Validation

```bash
# Test SQL injection
curl -X POST http://localhost:8000/api/v1/consent \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test'; DROP TABLE users; --",
    "email": "test@example.com",
    "consent_given": true
  }'
```

**Expected:** Validation error, no SQL execution

### 2. XSS Prevention

```bash
# Test XSS
curl -X POST http://localhost:8000/api/v1/consent \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<script>alert(\"XSS\")</script>",
    "email": "test@example.com",
    "consent_given": true
  }'
```

**Expected:** Input sanitized or rejected

### 3. CORS Testing

```bash
# Test CORS from unauthorized origin
curl -X POST http://localhost:8000/api/v1/consent \
  -H "Origin: http://evil.com" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "email": "test@example.com",
    "consent_given": true
  }'
```

**Expected:** CORS error

### 4. Rate Limiting

```bash
# Send many requests quickly
for i in {1..100}; do
  curl http://localhost:8000/health &
done
wait
```

**Expected:** Some requests rate-limited (if implemented)

## 🐛 Error Handling Tests

### 1. Invalid User ID

```bash
curl http://localhost:8000/api/v1/explainability/INVALID-ID
```

**Expected:** 404 Not Found

### 2. Missing Required Fields

```bash
curl -X POST http://localhost:8000/api/v1/consent \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test"
  }'
```

**Expected:** 422 Validation Error

### 3. Invalid Data Types

```bash
curl -X POST http://localhost:8000/api/v1/score \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "NEX-TEST",
    "behavioral_data": {
      "utility_payment_months": "invalid"
    }
  }'
```

**Expected:** 422 Validation Error

### 4. Database Connection Error

```bash
# Stop database
docker-compose stop postgres

# Try API call
curl http://localhost:8000/api/v1/consent \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","consent_given":true}'
```

**Expected:** 500 Internal Server Error with graceful message

## 📊 Test Results Template

### Test Run: [Date]

#### Environment
- Backend: Running ✅ / Failed ❌
- Frontend: Running ✅ / Failed ❌
- Database: Connected ✅ / Failed ❌
- ML Model: Loaded ✅ / Failed ❌

#### API Tests
- Health Check: ✅ / ❌
- Consent: ✅ / ❌
- Score Calculation: ✅ / ❌
- Explainability: ✅ / ❌
- Improvement Plan: ✅ / ❌
- Lender View: ✅ / ❌

#### Frontend Tests
- Consent Screen: ✅ / ❌
- Dashboard: ✅ / ❌
- Explainability: ✅ / ❌
- Improvement Plan: ✅ / ❌
- Lender View: ✅ / ❌

#### Performance
- Avg Response Time: ___ms
- Requests/Second: ___
- Error Rate: ___%

#### Security
- Input Validation: ✅ / ❌
- XSS Prevention: ✅ / ❌
- CORS: ✅ / ❌
- SQL Injection: ✅ / ❌

#### Issues Found
1. [Issue description]
2. [Issue description]

## 🎯 Acceptance Criteria

Platform is ready for production when:

- [ ] All API endpoints return 200 OK
- [ ] All frontend screens render correctly
- [ ] Score calculation completes in <2s
- [ ] Explanations are human-readable
- [ ] No console errors
- [ ] No security vulnerabilities
- [ ] Performance meets targets
- [ ] Error handling works gracefully
- [ ] Documentation is complete
- [ ] All tests pass

## 📞 Reporting Issues

When reporting issues, include:

1. **Environment**: Dev/Staging/Prod
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Screenshots/logs**
6. **Browser/OS** (for frontend issues)

---

**Happy Testing!** 🧪
