@echo off
echo ======================================================================
echo NEXIS - EMERGENCY START
echo ======================================================================
echo.
echo This will start BOTH backend and frontend in separate windows
echo.
echo ======================================================================
echo.

echo Starting Backend...
start "NEXIS Backend" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --reload"

echo Waiting 3 seconds...
timeout /t 3 /nobreak >nul

echo Starting Frontend...
start "NEXIS Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ======================================================================
echo.
echo ✅ Started!
echo.
echo Two new windows opened:
echo   1. NEXIS Backend (port 8000)
echo   2. NEXIS Frontend (port 5173)
echo.
echo Wait 10 seconds, then open: http://localhost:5173
echo.
echo ======================================================================
echo.
pause
