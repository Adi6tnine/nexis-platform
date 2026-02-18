# NEXIS Frontend

React-based frontend for the NEXIS Credit Trust Platform.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main application
│   ├── main.jsx             # Entry point
│   ├── index.css            # Global styles
│   └── services/
│       └── api.js           # Backend API client
├── public/                  # Static assets
├── index.html               # HTML template
├── package.json             # Dependencies
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind CSS config
└── postcss.config.js        # PostCSS config
```

## 🎨 Features

- **5 Main Screens**:
  - Consent Screen
  - Dashboard (Score Visualization)
  - Explainability Detail
  - Improvement Plan
  - Lender Portal

- **Responsive Design**: Mobile-friendly
- **Smooth Animations**: Framer Motion
- **Modern UI**: Tailwind CSS
- **API Integration**: Ready for backend

## 🔌 API Integration

The frontend uses `src/services/api.js` to communicate with the backend:

```javascript
import { api } from './services/api';

// Submit consent
const response = await api.submitConsent(consentData);

// Calculate score
const score = await api.calculateScore(userId, behavioralData);

// Get explainability
const explanation = await api.getExplainability(userId);
```

## 🛠️ Configuration

Create `.env` file:

```bash
VITE_API_URL=http://localhost:8000/api/v1
```

## 📦 Dependencies

- React 18.3
- Vite 5.1
- Tailwind CSS 3.4
- Framer Motion 11.0
- Lucide React 0.344

## 🐳 Docker

```bash
# Build
docker build -t nexis-frontend .

# Run
docker run -p 3000:80 nexis-frontend
```

## 📄 License

© 2026 NEXIS. All rights reserved.
