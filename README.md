# NEXIS - Credit Trust Assessment Platform

> Rule-based credit assessment system for India's underbanked population

[![Netlify Status](https://api.netlify.com/api/v1/badges/YOUR-BADGE-ID/deploy-status)](https://app.netlify.com/sites/YOUR-SITE-NAME/deploys)

## 🎯 Overview

NEXIS is a transparent, rule-based credit trust assessment platform designed for India's financial ecosystem. It evaluates creditworthiness using behavioral financial data without relying on traditional credit scores.

### Key Features

- ✅ **12 Transparent Rules** - Clear, explainable assessment criteria
- ✅ **Behavioral Data Analysis** - UPI transactions, utility payments, savings patterns
- ✅ **Real-time Scoring** - Instant credit trust assessment (300-900 scale)
- ✅ **Rule Completion Path** - Actionable steps to improve assessment
- ✅ **India-Focused** - Built for Indian financial context and regulations

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/nexis-platform.git
   cd nexis-platform
   ```

2. **Start Backend**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Mac/Linux
   pip install -r requirements.txt
   python -m uvicorn app.main:app --reload
   ```

3. **Start Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Quick Start Scripts

**Windows:**
- `QUICK_START.bat` - Start both frontend and backend
- `START_BACKEND.bat` - Start backend only
- `START_FRONTEND.bat` - Start frontend only

## 📦 Tech Stack

### Frontend
- React 18 + Vite
- Tailwind CSS
- Framer Motion
- Lucide Icons

### Backend
- FastAPI (Python)
- SQLAlchemy ORM
- SQLite (dev) / PostgreSQL (prod)
- JWT Authentication

## 🌐 Deployment

### Deploy to Netlify (Frontend)

1. **Push to Git**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Connect to Netlify**
   - Go to [Netlify](https://app.netlify.com/)
   - Click "Add new site" → Import from Git
   - Select your repository
   - Build settings are auto-configured from `netlify.toml`

3. **Set Environment Variable**
   - Site settings → Environment variables
   - Add: `VITE_API_URL` = `YOUR_BACKEND_URL/api/v1`

4. **Deploy!**
   - Click "Deploy site"
   - Live in 2-3 minutes ⚡

📚 **Detailed Guide:** [docs/deployment/NETLIFY_DEPLOYMENT_GUIDE.md](docs/deployment/NETLIFY_DEPLOYMENT_GUIDE.md)

### Deploy Backend

Recommended platforms:
- **Render.com** - Easy Python deployment, free tier
- **Railway.app** - Simple deployment, free tier
- **Heroku** - Classic choice with PostgreSQL add-on

## 📖 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get up and running
- **[Deployment Guide](docs/deployment/NETLIFY_DEPLOYMENT_GUIDE.md)** - Deploy to production
- **[Architecture](docs/ARCHITECTURE.md)** - System design and structure
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when running)
- **[Testing Guide](docs/TESTING_GUIDE.md)** - Run tests and QA

## 🎓 For Judges/Reviewers

- **[Judge Presentation](docs/JUDGE_PRESENTATION.md)** - Project overview for evaluation
- **[System Flowchart](docs/SYSTEM_FLOWCHART.md)** - Visual system architecture
- **[Quick QA Guide](docs/QUICK_QA_GUIDE.md)** - Test the platform quickly

## 🔐 Security & Privacy

- End-to-end encryption for data transmission
- JWT-based authentication
- No PII stored without consent
- Account Aggregator framework compliant (India)
- GDPR-inspired data handling

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend build test
cd frontend
npm run build
```

## 📊 Sample Data

The platform uses realistic sample data for demonstration. In production, data would be sourced from:
- Account Aggregator framework
- Bank APIs (with consent)
- UPI transaction history
- Verified financial institutions

## 🤝 Contributing

This is a hackathon/demo project. For production use, please contact the team.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 👥 Team

Built for India's financial inclusion mission.

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/YOUR-USERNAME/nexis-platform/issues)
- **Documentation:** [docs/](docs/)
- **Email:** support@nexis.in (demo)

---

**Made with ❤️ for India's underbanked population**
