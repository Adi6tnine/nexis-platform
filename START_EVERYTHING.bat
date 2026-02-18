@echo off
echo ======================================================================
echo NEXIS Platform - Complete Startup Guide
echo ======================================================================
echo.
echo This will help you start both backend and frontend
echo.
echo ======================================================================
echo.

echo STEP 1: Starting Backend...
echo.
echo Opening new terminal for backend...
start cmd /k "cd /d "%~dp0backend" && echo Starting NEXIS Backend... && echo. && python -m uvicorn app.main:app --reload"

timeout /t 3 /nobreak >nul

echo.
echo STEP 2: Starting Frontend...
echo.
echo Opening new terminal for frontend...
start cmd /k "cd /d "%~dp0frontend" && echo Starting NEXIS Frontend... && echo. && npm run dev"

echo.
echo ======================================================================
echo.
echo ✅ Both terminals opened!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Wait 5-10 seconds for both to start, then:
echo 1. Open browser: http://localhost:5173
echo 2. Register a new account
echo 3. Start using NEXIS!
echo.
echo ======================================================================
pause
