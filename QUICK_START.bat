@echo off
echo ========================================
echo NEXIS Platform - Quick Start
echo ========================================
echo.

echo Step 1: Installing Backend Dependencies...
echo ----------------------------------------
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install backend dependencies!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo.
echo ✓ Backend dependencies installed successfully!
echo.

echo Step 2: Installing Frontend Dependencies...
echo ----------------------------------------
cd ..\frontend
call npm install
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install frontend dependencies!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo.
echo ✓ Frontend dependencies installed successfully!
echo.

cd ..
echo ========================================
echo ✓ Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open TWO separate command prompts
echo 2. In first prompt: cd backend ^&^& python -m uvicorn app.main:app --reload
echo 3. In second prompt: cd frontend ^&^& npm run dev
echo 4. Open browser to http://localhost:5173
echo.
echo Or use the START_BACKEND.bat and START_FRONTEND.bat files!
echo.
pause
