@echo off
echo ======================================================================
echo NEXIS - Install Backend Dependencies
echo ======================================================================
echo.
echo This will install all required Python packages for the backend
echo.
echo ======================================================================
echo.

cd /d "%~dp0backend"

echo Installing dependencies...
echo.

pip install -r requirements.txt

echo.
echo ======================================================================
echo.
echo ✅ Dependencies installed!
echo.
echo Now you can start the backend:
echo   python -m uvicorn app.main:app --reload
echo.
echo Or just run: START_BACKEND.bat
echo.
echo ======================================================================
pause
