# NEXIS Platform - Deployment Checklist

**Use this checklist before deploying to production**

---

## ✅ Pre-Deployment Checklist

### 1. Environment Setup
- [ ] Set `DATABASE_URL` to PostgreSQL connection string
- [ ] Set `SECRET_KEY` to a secure random string (min 32 chars)
- [ ] Set `ENVIRONMENT=production` in backend/.env
- [ ] Set `VITE_API_URL` to production API URL in frontend/.env
- [ ] Verify all environment variables are set
- [ ] Remove any development-only settings

### 2. Database
- [ ] Run Alembic migrations: `alembic upgrade head`
- [ ] Verify all tables created
- [ ] Test database connection
- [ ] Set up database backups
- [ ] Configure connection pooling

### 3. ML Model
- [ ] Train model with production data: `python train_model.py`
- [ ] Verify model files exist in `models/` directory
- [ ] Test model loading on startup
- [ ] Validate prediction accuracy
- [ ] Set up model versioning

### 4. Security
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS for production domains only
- [ ] Set secure cookie settings
- [ ] Enable rate limiting (already configured)
- [ ] Add security headers
- [ ] Implement JWT authentication (optional but recommended)
- [ ] Set up firewall rules
- [ ] Enable audit logging

### 5. Backend
- [ ] Set `reload=False` in uvicorn
- [ ] Configure production ASGI server (gunicorn + uvicorn workers)
- [ ] Set up health check monitoring
- [ ] Configure logging to file/service
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Test all API endpoints
- [ ] Verify rate limits are working
- [ ] Check PII masking in logs

### 6. Frontend
- [ ] Build production bundle: `npm run build`
- [ ] Test production build locally
- [ ] Configure CDN for static assets
- [ ] Set up error tracking
- [ ] Enable analytics (optional)
- [ ] Test on multiple browsers
- [ ] Test on mobile devices
- [ ] Verify API calls use production URL

### 7. Docker (If Using)
- [ ] Build production images
- [ ] Test docker-compose.prod.yml
- [ ] Configure volume persistence
- [ ] Set up container health checks
- [ ] Configure restart policies
- [ ] Test inter-service communication
- [ ] Set resource limits

### 8. Monitoring
- [ ] Set up application monitoring
- [ ] Configure uptime monitoring
- [ ] Set up log aggregation
- [ ] Configure alerts for errors
- [ ] Set up performance monitoring
- [ ] Configure database monitoring
- [ ] Set up API response time tracking

### 9. Testing
- [ ] Run all unit tests
- [ ] Run integration tests
- [ ] Run end-to-end tests
- [ ] Test complete user flow
- [ ] Test lender flow
- [ ] Load test API endpoints
- [ ] Test error scenarios
- [ ] Verify audit trail

### 10. Documentation
- [ ] Update README with production URLs
- [ ] Document deployment process
- [ ] Create runbook for common issues
- [ ] Document backup/restore procedures
- [ ] Create incident response plan
- [ ] Document API rate limits
- [ ] Update architecture diagrams

### 11. Compliance
- [ ] Review GDPR compliance
- [ ] Verify consent flow
- [ ] Check PII handling
- [ ] Verify audit trail
- [ ] Review data retention policies
- [ ] Check "right to explanation" implementation
- [ ] Verify no discriminatory features

### 12. Performance
- [ ] Optimize database queries
- [ ] Add database indexes
- [ ] Configure caching (Redis, etc.)
- [ ] Optimize ML model loading
- [ ] Minimize frontend bundle size
- [ ] Enable gzip compression
- [ ] Configure CDN

---

## 🚀 Deployment Steps

### Option 1: Docker Deployment

```bash
# 1. Build images
docker-compose -f deployment/docker-compose.prod.yml build

# 2. Start services
docker-compose -f deployment/docker-compose.prod.yml up -d

# 3. Check health
curl https://your-domain.com/health

# 4. Monitor logs
docker-compose -f deployment/docker-compose.prod.yml logs -f
```

### Option 2: Manual Deployment

#### Backend
```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Run migrations
alembic upgrade head

# 3. Train model (if needed)
python train_model.py

# 4. Start with gunicorn
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

#### Frontend
```bash
# 1. Install dependencies
cd frontend
npm install

# 2. Build production bundle
npm run build

# 3. Serve with nginx or similar
# Copy dist/ folder to web server
```

---

## 🔍 Post-Deployment Verification

### 1. Health Checks
```bash
# Backend health
curl https://your-domain.com/health

# Model health
curl https://your-domain.com/health/model

# Frontend
curl https://your-domain.com
```

### 2. API Testing
```bash
# Test consent endpoint
curl -X POST https://your-domain.com/api/v1/consent \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","consent_given":true}'

# Test score endpoint (use returned user_id)
curl -X POST https://your-domain.com/api/v1/score \
  -H "Content-Type: application/json" \
  -d '{"user_id":"NEX-XXX","behavioral_data":{...}}'
```

### 3. Frontend Testing
- [ ] Open production URL in browser
- [ ] Complete consent flow
- [ ] Verify score calculation
- [ ] Check explainability
- [ ] Test improvement plan
- [ ] Test lender portal
- [ ] Verify no console errors

### 4. Performance Testing
```bash
# Load test with Apache Bench
ab -n 1000 -c 10 https://your-domain.com/health

# Expected: < 100ms average response time
```

### 5. Security Testing
- [ ] Verify HTTPS is enforced
- [ ] Check CORS headers
- [ ] Test rate limiting
- [ ] Verify PII masking in logs
- [ ] Check for exposed secrets
- [ ] Test input validation

---

## 🚨 Rollback Plan

### If Deployment Fails

1. **Immediate Actions**
   ```bash
   # Stop new deployment
   docker-compose -f deployment/docker-compose.prod.yml down
   
   # Or stop services manually
   systemctl stop nexis-backend
   systemctl stop nexis-frontend
   ```

2. **Restore Previous Version**
   ```bash
   # Restore from backup
   git checkout <previous-tag>
   
   # Rebuild and deploy
   docker-compose -f deployment/docker-compose.prod.yml up -d
   ```

3. **Database Rollback**
   ```bash
   # Rollback migration
   alembic downgrade -1
   
   # Or restore from backup
   pg_restore -d nexis_db backup.sql
   ```

4. **Notify Stakeholders**
   - Send status update
   - Provide ETA for fix
   - Document issue

---

## 📊 Monitoring Checklist

### Metrics to Track
- [ ] API response times
- [ ] Error rates
- [ ] Request rates
- [ ] Database query times
- [ ] ML prediction times
- [ ] Memory usage
- [ ] CPU usage
- [ ] Disk usage

### Alerts to Configure
- [ ] API errors > 1%
- [ ] Response time > 1s
- [ ] Database connection failures
- [ ] Model loading failures
- [ ] Disk usage > 80%
- [ ] Memory usage > 80%
- [ ] Rate limit violations

---

## 🔐 Security Hardening

### Backend
- [ ] Disable debug mode
- [ ] Remove development endpoints
- [ ] Enable HTTPS only
- [ ] Set secure headers
- [ ] Configure CORS strictly
- [ ] Enable request logging
- [ ] Set up intrusion detection

### Database
- [ ] Use strong passwords
- [ ] Enable SSL connections
- [ ] Restrict network access
- [ ] Enable query logging
- [ ] Set up regular backups
- [ ] Configure replication

### Frontend
- [ ] Enable CSP headers
- [ ] Disable source maps
- [ ] Minify and obfuscate code
- [ ] Use HTTPS only
- [ ] Implement rate limiting
- [ ] Add CSRF protection

---

## 📝 Post-Deployment Tasks

### Week 1
- [ ] Monitor error rates daily
- [ ] Review performance metrics
- [ ] Check user feedback
- [ ] Fix critical bugs
- [ ] Update documentation

### Week 2-4
- [ ] Analyze usage patterns
- [ ] Optimize slow queries
- [ ] Review security logs
- [ ] Plan feature updates
- [ ] Conduct security audit

### Monthly
- [ ] Review system metrics
- [ ] Update dependencies
- [ ] Retrain ML model
- [ ] Backup verification
- [ ] Disaster recovery drill

---

## ✅ Sign-Off

### Deployment Approval

- [ ] Technical Lead: _______________
- [ ] Security Officer: _______________
- [ ] Compliance Officer: _______________
- [ ] Product Manager: _______________

### Deployment Date: _______________
### Deployed By: _______________
### Version: _______________

---

## 📞 Emergency Contacts

- **Technical Lead**: [contact]
- **DevOps**: [contact]
- **Security**: [contact]
- **On-Call**: [contact]

---

## 🎉 Success Criteria

Deployment is successful when:
- [ ] All health checks pass
- [ ] API response time < 500ms
- [ ] Error rate < 0.1%
- [ ] Frontend loads < 2s
- [ ] Complete user flow works
- [ ] Lender flow works
- [ ] No critical errors in logs
- [ ] Monitoring is active
- [ ] Backups are configured

---

**Document Version**: 1.0  
**Last Updated**: February 17, 2026  
**Status**: Ready for Production Deployment
