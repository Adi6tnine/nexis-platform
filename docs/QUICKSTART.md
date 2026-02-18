# NEXIS Platform - Quick Start Guide

**Get up and running in 5 minutes!**

---

## 🚀 Quick Start (3 Commands)

### 1. Train the Model
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python train_model.py
```

### 2. Start Backend
```bash
# In backend directory with venv activated
uvicorn app.main:app --reload
```

### 3. Start Frontend (New Terminal)
```bash
cd frontend
npm install
npm run dev
```

### 4. Open Browser
Navigate to: `http://localhost:5173`

---

## ✅ What You'll See

1. **Consent Screen** - Fill in your details
2. **Dashboard** - See your REAL credit trust score
3. **Explainability** - Understand why you got that score
4. **Improvement Plan** - Get actionable recommendations
5. **Lender Portal** - See the lender decision interface

---

## 🎯 Demo Flow (3 Minutes)

1. Fill consent form → Submit
2. Wait for loading → See dashboard with real score
3. Click "View Detailed Analysis" → See SHAP factors
4. Click "Explore Improvement Plan" → See recommendations
5. Click "Lender Portal" → Make a decision

---

## 📊 Expected Results

- **Trust Score**: 700-800 range (varies based on sample data)
- **Risk Level**: Low-Moderate
- **Factors**: 4-6 factors (positive, neutral, negative)
- **Recommendations**: 3 actionable steps
- **Response Time**: < 500ms per API call

---

## 🔧 Troubleshooting

### Backend won't start?
```bash
# Check if model is trained
ls backend/models/

# Should see:
# - credit_trust_model.pkl
# - scaler.pkl
# - explainer.pkl
```

### Frontend can't connect?
```bash
# Check backend is running
curl http://localhost:8000/health

# Should return:
# {"status":"healthy",...}
```

### Rate limit errors?
Wait 1 minute between requests or restart backend.

---

## 📚 Full Documentation

- [INTEGRATION_COMPLETE.md](docs/INTEGRATION_COMPLETE.md) - Complete integration guide
- [CURRENT_STATUS.md](docs/CURRENT_STATUS.md) - Detailed status
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
- API Docs: http://localhost:8000/docs

---

## 🎉 You're Ready!

The platform is fully integrated and demo-ready. Enjoy exploring NEXIS!

**Questions?** Check the docs folder for comprehensive guides.
