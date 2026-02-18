@echo off
REM NEXIS Platform - Quick Setup Script for Windows

REM Get script directory
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

echo ==================================
echo NEXIS Platform - Quick Setup
echo ==================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    exit /b 1
)
echo [OK] Python found

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed
    exit /b 1
)
echo [OK] Node.js found

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed
    exit /b 1
)
echo [OK] npm found

echo.
echo ==================================
echo Setting up Backend
echo ==================================
echo.

cd "%PROJECT_ROOT%\backend"

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo [WARNING] Please review backend\.env and update if needed
)

REM Train ML model
echo Training ML model...
python train_model.py

echo [OK] Backend setup complete!

cd "%PROJECT_ROOT%\frontend"

echo.
echo ==================================
echo Setting up Frontend
echo ==================================
echo.

REM Install frontend dependencies
echo Installing Node.js dependencies...
call npm install

REM Create .env if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
)

echo [OK] Frontend setup complete!

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo To start the platform:
echo.
echo 1. Start Backend (Terminal 1):
echo    cd %PROJECT_ROOT%\backend
echo    venv\Scripts\activate
echo    uvicorn app.main:app --reload
echo.
echo 2. Start Frontend (Terminal 2):
echo    cd %PROJECT_ROOT%\frontend
echo    npm run dev
echo.
echo 3. Open browser:
echo    http://localhost:3000
echo.
echo API Documentation:
echo    http://localhost:8000/docs
echo.
echo ==================================

pause
