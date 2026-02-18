@echo off
echo ============================================================
echo NEXIS Backend Startup
echo ============================================================
echo.

cd /d "%~dp0backend"

echo Starting Backend Server...
echo.
echo Backend will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
