# NEXIS Platform - Production Deployment Guide

## 🎯 Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Load Balancer                        │
│                    (HTTPS/SSL)                           │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼──────┐  ┌──────▼────────┐
│   Frontend   │  │    Backend    │
│   (React)    │  │   (FastAPI)   │
│   Port 3000  │  │   Port 8000   │
└──────────────┘  └───────┬───────┘
                          │
                  ┌───────▼────────┐
                  │   PostgreSQL   │
                  │   Port 5432    │
                  └────────────────┘
```

## 🚀 Deployment Options

### Option 1: Docker Compose (Recommended for MVP)

**Pros**: Simple, fast, all-in-one
**Cons**: Single server, limited scaling

```bash
# 1. Clone repository
git clone <repo-url>
cd nexis-platform

# 2. Configure environment
cp backend/.env.example backend/.env
cp .env.example .env

# Edit backend/.env:
DATABASE_URL=postgresql://nexis:secure_password@postgres:5432/nexis
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ENVIRONMENT=production

# Edit .env:
VITE_API_URL=https://api.yourdomain.com/api/v1

# 3. Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# 4. Check status
docker-compose ps
docker-compose logs -f
```

### Option 2: Kubernetes (For Scale)

**Pros**: Auto-scaling, high availability
**Cons**: Complex setup

```bash
# 1. Create namespace
kubectl create namespace nexis

# 2. Create secrets
kubectl create secret generic nexis-secrets \
  --from-literal=database-url=postgresql://... \
  --from-literal=secret-key=... \
  -n nexis

# 3. Deploy
kubectl apply -f k8s/ -n nexis

# 4. Check status
kubectl get pods -n nexis
kubectl get services -n nexis
```

### Option 3: Cloud Platform (AWS/GCP/Azure)

#### AWS Deployment

**Services Used**:
- ECS/Fargate: Container orchestration
- RDS PostgreSQL: Database
- ALB: Load balancer
- S3 + CloudFront: Frontend hosting
- ECR: Container registry

```bash
# 1. Build and push images
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

docker build -t nexis-backend backend/
docker tag nexis-backend:latest <account>.dkr.ecr.us-east-1.amazonaws.com/nexis-backend:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/nexis-backend:latest

# 2. Deploy to ECS
aws ecs update-service --cluster nexis-cluster --service nexis-backend --force-new-deployment

# 3. Build and deploy frontend
npm run build
aws s3 sync dist/ s3://nexis-frontend/
aws cloudfront create-invalidation --distribution-id <id> --paths "/*"
```

## 🔧 Production Configuration

### Backend Configuration

**backend/.env**:
```bash
# Database (PostgreSQL required for production)
DATABASE_URL=postgresql://nexis_user:secure_password@db.internal:5432/nexis_prod

# Security
SECRET_KEY=<64-char-hex-string>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_V1_PREFIX=/api/v1
PROJECT_NAME=NEXIS Credit Trust Platform

# ML Model
MODEL_PATH=/app/models/credit_trust_model.pkl
SCALER_PATH=/app/models/feature_scaler.pkl
EXPLAINER_PATH=/app/models/shap_explainer.pkl

# Environment
ENVIRONMENT=production

# CORS (restrict to your domain)
BACKEND_CORS_ORIGINS=["https://nexis.yourdomain.com"]

# Logging
LOG_LEVEL=INFO
```

### Frontend Configuration

**.env.production**:
```bash
VITE_API_URL=https://api.yourdomain.com/api/v1
```

### Database Setup

```sql
-- Create production database
CREATE DATABASE nexis_prod;
CREATE USER nexis_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE nexis_prod TO nexis_user;

-- Connect to database
\c nexis_prod

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO nexis_user;
```

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/nexis

# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name nexis.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name nexis.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/nexis.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nexis.yourdomain.com/privkey.pem;
    
    root /var/www/nexis/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🔒 SSL/TLS Setup

### Using Let's Encrypt (Free)

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Get certificates
sudo certbot --nginx -d api.yourdomain.com -d nexis.yourdomain.com

# Auto-renewal (cron)
sudo crontab -e
# Add: 0 0 * * * certbot renew --quiet
```

## 📊 Monitoring & Logging

### Application Monitoring

**Prometheus + Grafana**:

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prometheus_data:
  grafana_data:
```

### Logging

**Centralized Logging with ELK Stack**:

```bash
# Install Elasticsearch, Logstash, Kibana
docker-compose -f docker-compose.elk.yml up -d

# Configure backend to send logs
# backend/app/core/logging.py
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

### Health Checks

```bash
# Backend health
curl https://api.yourdomain.com/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "ml_model": "loaded",
  "environment": "production"
}

# Set up monitoring alerts
# If health check fails, send alert to Slack/PagerDuty
```

## 🔄 CI/CD Pipeline

### GitHub Actions

**.github/workflows/deploy.yml**:

```yaml
name: Deploy NEXIS Platform

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Train model
        run: |
          cd backend
          python train_model.py
      
      - name: Run tests
        run: |
          cd backend
          pytest tests/

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and push Docker image
        run: |
          docker build -t nexis-backend backend/
          docker tag nexis-backend:latest ${{ secrets.DOCKER_REGISTRY }}/nexis-backend:latest
          docker push ${{ secrets.DOCKER_REGISTRY }}/nexis-backend:latest
      
      - name: Deploy to production
        run: |
          ssh ${{ secrets.PROD_SERVER }} "docker pull ${{ secrets.DOCKER_REGISTRY }}/nexis-backend:latest && docker-compose up -d"

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Build frontend
        run: |
          npm install
          npm run build
      
      - name: Deploy to S3
        run: |
          aws s3 sync dist/ s3://nexis-frontend/
          aws cloudfront create-invalidation --distribution-id ${{ secrets.CF_DIST_ID }} --paths "/*"
```

## 📈 Scaling Strategy

### Horizontal Scaling

```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  backend:
    image: nexis-backend
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 2G
      restart_policy:
        condition: on-failure
  
  nginx:
    image: nginx
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
```

### Database Scaling

```sql
-- Read replicas for PostgreSQL
-- Primary: Write operations
-- Replicas: Read operations (explainability, lender view)

-- Connection pooling
-- Use PgBouncer or SQLAlchemy pool
```

### Caching Strategy

```python
# Redis caching for scores
import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)

def get_cached_score(user_id):
    cached = redis_client.get(f"score:{user_id}")
    if cached:
        return json.loads(cached)
    return None

def cache_score(user_id, score_data, ttl=3600):
    redis_client.setex(
        f"score:{user_id}",
        ttl,
        json.dumps(score_data)
    )
```

## 🔐 Security Hardening

### Application Security

```python
# Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/score")
@limiter.limit("10/minute")
async def calculate_score(...):
    ...

# Input validation
from pydantic import validator

class BehavioralDataInput(BaseModel):
    utility_payment_months: int
    
    @validator('utility_payment_months')
    def validate_months(cls, v):
        if v < 0 or v > 120:
            raise ValueError('Invalid payment months')
        return v
```

### Infrastructure Security

```bash
# Firewall rules
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp # HTTPS
sudo ufw enable

# Fail2ban for SSH protection
sudo apt-get install fail2ban
sudo systemctl enable fail2ban

# Regular updates
sudo apt-get update && sudo apt-get upgrade -y
```

## 📊 Performance Optimization

### Backend Optimization

```python
# Async database queries
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine(DATABASE_URL)

async def get_user_async(user_id: str):
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

# Connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

### Frontend Optimization

```javascript
// Code splitting
const Dashboard = lazy(() => import('./Dashboard'));
const ExplainabilityDetail = lazy(() => import('./ExplainabilityDetail'));

// API response caching
const cache = new Map();

async function cachedFetch(url, ttl = 60000) {
  const cached = cache.get(url);
  if (cached && Date.now() - cached.timestamp < ttl) {
    return cached.data;
  }
  
  const data = await fetch(url).then(r => r.json());
  cache.set(url, { data, timestamp: Date.now() });
  return data;
}
```

## 🚨 Disaster Recovery

### Backup Strategy

```bash
# Automated database backups
#!/bin/bash
# /etc/cron.daily/backup-nexis-db

BACKUP_DIR="/backups/nexis"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
pg_dump -U nexis_user nexis_prod | gzip > $BACKUP_DIR/nexis_$DATE.sql.gz

# Backup ML models
tar -czf $BACKUP_DIR/models_$DATE.tar.gz /app/models/

# Upload to S3
aws s3 cp $BACKUP_DIR/nexis_$DATE.sql.gz s3://nexis-backups/
aws s3 cp $BACKUP_DIR/models_$DATE.tar.gz s3://nexis-backups/

# Keep only last 30 days
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
```

### Recovery Procedure

```bash
# 1. Restore database
gunzip < nexis_20260217.sql.gz | psql -U nexis_user nexis_prod

# 2. Restore models
tar -xzf models_20260217.tar.gz -C /app/

# 3. Restart services
docker-compose restart
```

## ✅ Pre-Launch Checklist

- [ ] SSL certificates installed
- [ ] Environment variables configured
- [ ] Database backups automated
- [ ] Monitoring dashboards set up
- [ ] Error tracking configured (Sentry)
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Security headers added
- [ ] Load testing completed
- [ ] Disaster recovery tested
- [ ] Documentation updated
- [ ] Team trained on operations

## 📞 Production Support

### Runbook

**Issue: High CPU usage**
```bash
# Check processes
docker stats
# Scale up if needed
docker-compose up -d --scale backend=5
```

**Issue: Database connection errors**
```bash
# Check connections
psql -U nexis_user -c "SELECT count(*) FROM pg_stat_activity;"
# Restart if needed
docker-compose restart postgres
```

**Issue: Model prediction slow**
```bash
# Check model file
ls -lh /app/models/
# Retrain if corrupted
python train_model.py
```

---

**Your NEXIS platform is now production-ready!** 🚀

For support: ops@nexis.example.com
