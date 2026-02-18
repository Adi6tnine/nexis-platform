# NEXIS Platform - Netlify Deployment Guide

## ✅ Pre-Deployment Checklist

Your project is **READY** for Netlify deployment! Here's what's been configured:

### Files Created:
- ✅ `netlify.toml` - Main Netlify configuration
- ✅ `frontend/_redirects` - Client-side routing support
- ✅ Build scripts configured in `package.json`
- ✅ Environment variables documented

---

## 🚀 Deployment Steps

### Option 1: Deploy via Netlify UI (Recommended for First Time)

1. **Push your code to GitHub/GitLab/Bitbucket**
   ```bash
   git add .
   git commit -m "Ready for Netlify deployment"
   git push origin main
   ```

2. **Go to Netlify**
   - Visit https://app.netlify.com/
   - Click "Add new site" → "Import an existing project"
   - Connect your Git provider (GitHub/GitLab/Bitbucket)
   - Select your repository

3. **Configure Build Settings** (Auto-detected from netlify.toml)
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/dist`
   - These should be auto-filled from `netlify.toml`

4. **Set Environment Variables**
   - Go to Site settings → Environment variables
   - Add: `VITE_API_URL` = `YOUR_BACKEND_URL/api/v1`
   - Example: `https://your-backend.herokuapp.com/api/v1`

5. **Deploy!**
   - Click "Deploy site"
   - Wait 2-3 minutes for build to complete
   - Your site will be live at: `https://random-name-12345.netlify.app`

---

### Option 2: Deploy via Netlify CLI

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**
   ```bash
   netlify login
   ```

3. **Initialize and Deploy**
   ```bash
   # From project root
   netlify init
   
   # Follow prompts:
   # - Create & configure a new site
   # - Choose your team
   # - Site name (optional)
   ```

4. **Set Environment Variables**
   ```bash
   netlify env:set VITE_API_URL "YOUR_BACKEND_URL/api/v1"
   ```

5. **Deploy**
   ```bash
   netlify deploy --prod
   ```

---

## 🔧 Important Configuration

### Backend URL
You MUST configure the backend URL as an environment variable:

**For Netlify UI:**
- Site settings → Environment variables → Add variable
- Key: `VITE_API_URL`
- Value: Your backend API URL (e.g., `https://nexis-backend.herokuapp.com/api/v1`)

**For Netlify CLI:**
```bash
netlify env:set VITE_API_URL "https://your-backend-url.com/api/v1"
```

### CORS Configuration
Make sure your backend allows requests from your Netlify domain:

In `backend/app/main.py`, update CORS origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-site-name.netlify.app",  # Add your Netlify URL
        "https://your-custom-domain.com"       # If using custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🌐 Custom Domain (Optional)

1. **Add Custom Domain**
   - Site settings → Domain management → Add custom domain
   - Enter your domain (e.g., `nexis.yourdomain.com`)

2. **Configure DNS**
   - Add CNAME record pointing to your Netlify site
   - Or use Netlify DNS for automatic configuration

3. **Enable HTTPS**
   - Netlify automatically provisions SSL certificate
   - Usually takes 1-2 minutes

---

## 🔍 Post-Deployment Verification

After deployment, test these features:

1. ✅ **Homepage loads** - Check if site is accessible
2. ✅ **Registration works** - Create a test account
3. ✅ **Login works** - Sign in with test account
4. ✅ **Consent screen** - Submit consent
5. ✅ **Dashboard displays** - View credit score
6. ✅ **Navigation works** - Test all pages (Profile, Rules, etc.)
7. ✅ **API calls succeed** - Check browser console for errors

---

## 🐛 Troubleshooting

### Build Fails
**Error:** `npm install` fails
- **Solution:** Check `package.json` for correct dependencies
- Run `npm install` locally first to verify

**Error:** `vite build` fails
- **Solution:** Check for syntax errors in code
- Run `npm run build` locally to test

### Site Loads but API Calls Fail
**Error:** CORS errors in console
- **Solution:** Update backend CORS settings with Netlify URL

**Error:** 404 on API calls
- **Solution:** Verify `VITE_API_URL` environment variable is set correctly

### Routing Issues (404 on refresh)
**Error:** Page refreshes show 404
- **Solution:** Verify `_redirects` file exists in `frontend/` directory
- Check `netlify.toml` has redirect rules

---

## 📊 Monitoring & Analytics

### Netlify Analytics (Optional)
- Enable in Site settings → Analytics
- Track page views, bandwidth, and performance

### Deploy Notifications
- Set up Slack/Discord/Email notifications
- Site settings → Build & deploy → Deploy notifications

---

## 🔄 Continuous Deployment

Netlify automatically deploys when you push to your main branch:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Netlify automatically:
# 1. Detects push
# 2. Runs build
# 3. Deploys new version
# 4. Notifies you
```

---

## 💰 Pricing

**Netlify Free Tier includes:**
- ✅ 100GB bandwidth/month
- ✅ 300 build minutes/month
- ✅ Automatic HTTPS
- ✅ Continuous deployment
- ✅ Form handling
- ✅ Serverless functions (100K requests/month)

This is MORE than enough for a demo/hackathon project!

---

## 🎯 Quick Deploy Checklist

- [ ] Code pushed to Git repository
- [ ] `netlify.toml` exists in project root
- [ ] `frontend/_redirects` exists
- [ ] Backend deployed and accessible
- [ ] Backend CORS configured for Netlify domain
- [ ] Environment variable `VITE_API_URL` ready
- [ ] Test build locally: `cd frontend && npm run build`
- [ ] Deploy via Netlify UI or CLI
- [ ] Set environment variables in Netlify
- [ ] Test deployed site thoroughly

---

## 📞 Need Help?

- Netlify Docs: https://docs.netlify.com/
- Netlify Community: https://answers.netlify.com/
- Vite Deployment: https://vitejs.dev/guide/static-deploy.html

---

## 🎉 You're Ready!

Your NEXIS platform is configured and ready for Netlify deployment. Just follow the steps above and you'll be live in minutes!

**Estimated deployment time:** 3-5 minutes ⚡
