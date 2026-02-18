@echo off
echo ========================================
echo NEXIS Platform - Netlify Deployment
echo ========================================
echo.

echo Step 1: Testing local build...
cd frontend
call npm run build
if errorlevel 1 (
    echo.
    echo ERROR: Build failed! Fix errors before deploying.
    pause
    exit /b 1
)

echo.
echo SUCCESS: Build completed successfully!
echo.
echo Next steps:
echo 1. Push your code to GitHub/GitLab/Bitbucket
echo 2. Go to https://app.netlify.com/
echo 3. Click "Add new site" and import your repository
echo 4. Set environment variable: VITE_API_URL = your-backend-url/api/v1
echo 5. Deploy!
echo.
echo OR use Netlify CLI:
echo   npm install -g netlify-cli
echo   netlify login
echo   netlify init
echo   netlify deploy --prod
echo.
echo See NETLIFY_DEPLOYMENT_GUIDE.md for detailed instructions
echo.
pause
