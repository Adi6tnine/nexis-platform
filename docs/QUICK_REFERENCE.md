# NEXIS Platform - Quick Reference Card

## 🚀 Quick Start

```bash
# Automated Setup
./setup.sh          # Linux/Mac
setup.bat           # Windows

# Manual Setup
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt && python train_model.py
uvicorn app.main:app --reload

# In another terminal
npm install && npm run dev
```

## 🔗 URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | User interface |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Interactive docs |
| Health Check | http://localhost:8000/health | Status check |

## 📡 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/consent` | POST | Submit consent |
| `/api/v1/score` | POST | Calculate score |
| `/api/v1/explainability/{user_id}` | GET | Get explanations |
| `/api/v1/improvement/{user_id}` | GET | Get recommendations |
| `/api/v1/roadmap/{user_id}` | GET | Get roadmap |
| `/api/v1/lender-view/{user_id}` | GET | Lender interface |
| `/api/v1/lender-decision` | POST | Record decision |

## 🧪 Quick Test

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. Submit consent
curl -X POST http://localhost:8000/api/v1/consent \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","consent_given":true}'

# 3. Calculate score (use user_id from step 2)
curl -X POST http://localhost:8000/api/v1/score \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":"NEX-XXXXXXXX",
    "behavioral_data":{
      "utility_payment_months":14,
      "utility_payment_consistency":0.95,
      "monthly_transaction_count":45,
      "transaction_regularity_score":0.88,
      "spending_volatility":0.12,
      "avg_month_end_balance":5000.0,
      "savings_growth_rate":0.15,
      "withdrawal_discipline_score":0.82,
      "income_regularity_score":0.90,
      "income_stability_months":18,
      "account_tenure_months":38,
      "address_stability_years":2.5,
      "discretionary_income_ratio":0.22
    }
  }'
```

## 📊 Sample Profiles

### Excellent (Score: 780-850)
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

### Good (Score: 650-750)
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

### Poor (Score: 300-500)
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

## 🐳 Docker Commands

```bash
# Development
docker-compose up -d
docker-compose logs -f
docker-compose down

# Production
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs backend

# Rebuild
docker-compose build --no-cache
docker-compose up -d --force-recreate
```

## 🔧 Common Commands

### Backend
```bash
# Activate venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Train model
python train_model.py

# Run server
uvicorn app.main:app --reload

# Run with custom port
uvicorn app.main:app --port 8080

# Check Python version
python --version
```

### Frontend
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Check Node version
node --version
```

### Database
```bash
# SQLite (development)
sqlite3 backend/nexis.db
.tables
.schema users
SELECT * FROM users;

# PostgreSQL (production)
psql -U nexis -d nexis_prod
\dt
\d users
SELECT * FROM users;
```

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Check if port is in use
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Check model files
ls backend/models/

# Retrain model
cd backend && python train_model.py
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check if port is in use
lsof -i :3000  # Linux/Mac
netstat -ano | findstr :3000  # Windows
```

### CORS errors
```bash
# Check backend CORS settings
# backend/app/core/config.py
BACKEND_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173"
]
```

### Database errors
```bash
# Delete and recreate
rm backend/nexis.db
# Restart backend (will recreate tables)
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app |
| `backend/app/api/routes.py` | API endpoints |
| `backend/app/ml/model.py` | ML model |
| `backend/train_model.py` | Training script |
| `src/App.jsx` | Frontend app |
| `src/services/api.js` | API client |
| `.env` | Environment config |
| `docker-compose.yml` | Docker config |

## 🔐 Environment Variables

### Backend (.env)
```bash
DATABASE_URL=sqlite:///./nexis.db
SECRET_KEY=your-secret-key
ENVIRONMENT=development
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000/api/v1
```

## 📊 Model Info

- **Algorithm**: Random Forest
- **Features**: 20 engineered
- **Classes**: 3 (Low/Moderate/High risk)
- **Accuracy**: ~92%
- **Prediction Time**: <100ms

## 🎯 Score Ranges

| Range | Risk Level | Description |
|-------|------------|-------------|
| 700-900 | Low | Excellent credit behavior |
| 600-699 | Low-Moderate | Good credit behavior |
| 500-599 | Moderate | Fair credit behavior |
| 300-499 | High | Poor credit behavior |

## 📞 Support

- **Docs**: See `/docs` folder
- **API Docs**: http://localhost:8000/docs
- **Issues**: Check logs first
- **Email**: support@nexis.example.com

## 🔗 Documentation

- [README.md](README.md) - Main overview
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Setup guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing procedures
- [backend/README.md](backend/README.md) - Backend docs

## ⚡ Performance Tips

1. Use PostgreSQL in production (not SQLite)
2. Enable Redis caching
3. Use nginx reverse proxy
4. Enable gzip compression
5. Implement rate limiting
6. Use connection pooling
7. Monitor with Prometheus
8. Set up CDN for frontend

## 🚨 Production Checklist

- [ ] Change SECRET_KEY
- [ ] Use PostgreSQL
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up monitoring
- [ ] Enable backups
- [ ] Configure rate limiting
- [ ] Set up error tracking
- [ ] Review security settings
- [ ] Test disaster recovery

---

**Keep this card handy for quick reference!** 📋
