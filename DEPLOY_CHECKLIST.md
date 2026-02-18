# 🚀 Netlify Deployment Checklist

## ✅ Pre-Deployment (Complete)

- [x] Project is working locally
- [x] `netlify.toml` configuration created
- [x] `frontend/_redirects` file created
- [x] Build scripts configured
- [x] Documentation organized
- [x] README.md updated
- [x] .gitignore configured

## 📋 Deployment Steps

### 1. Test Build Locally
```bash
cd frontend
npm run build
```
✅ Build should complete without errors

### 2. Commit and Push to Git
```bash
git add .
git commit -m "Ready for Netlify deployment"
git push origin main
```

### 3. Deploy on Netlify

1. Go to https://app.netlify.com/
2. Click "Add new site" → "Import an existing project"
3. Connect your Git provider (GitHub/GitLab/Bitbucket)
4. Select your repository
5. Build settings (auto-detected from netlify.toml):
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/dist`
6. Click "Deploy site"

### 4. Configure Environment Variables

In Netlify dashboard:
- Go to: Site settings → Environment variables
- Click "Add a variable"
- Key: `VITE_API_URL`
- Value: `YOUR_BACKEND_URL/api/v1`
- Click "Save"

### 5. Redeploy (if needed)

If you added environment variables after first deploy:
- Go to: Deploys tab
- Click "Trigger deploy" → "Deploy site"

## ⚠️ Important Notes

### Backend Deployment
Your backend needs to be deployed separately:
- **Recommended:** Render.com, Railway.app, or Heroku
- Get backend URL after deployment
- Use that URL in `VITE_API_URL`

### CORS Configuration
Update backend CORS to allow your Netlify domain:

In `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-site-name.netlify.app",  # ← Add this
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🧪 Post-Deployment Testing

Test these features on your live site:

- [ ] Homepage loads correctly
- [ ] Registration works
- [ ] Login works
- [ ] Consent screen displays
- [ ] Dashboard shows credit score
- [ ] Rule breakdown page works
- [ ] Rule completion path displays
- [ ] Profile page shows data
- [ ] All navigation works
- [ ] No console errors

## 📊 Expected Results

- **Build time:** 2-3 minutes
- **Site URL:** `https://random-name-12345.netlify.app`
- **Auto-deploy:** Enabled (deploys on git push)
- **HTTPS:** Automatic
- **CDN:** Global distribution

## 🆘 Troubleshooting

### Build Fails
- Run `npm run build` locally to catch errors
- Check build logs in Netlify dashboard

### API Calls Fail
- Verify `VITE_API_URL` is set correctly
- Check backend CORS settings
- Ensure backend is running and accessible

### 404 on Page Refresh
- Already fixed! `_redirects` file handles this
- Verify file exists in `frontend/` directory

## 📚 Documentation

- **Detailed Guide:** [docs/deployment/NETLIFY_DEPLOYMENT_GUIDE.md](docs/deployment/NETLIFY_DEPLOYMENT_GUIDE.md)
- **Quick Start:** [docs/deployment/DEPLOYMENT_READY.md](docs/deployment/DEPLOYMENT_READY.md)

---

## ✨ You're Ready to Deploy!

Everything is configured. Just follow the steps above and you'll be live in minutes!

**Good luck! 🚀**
