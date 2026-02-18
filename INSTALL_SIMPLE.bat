@echo off
echo ========================================
echo NEXIS - Simple Installation
echo ========================================
echo.
echo Installing with flexible versions...
echo.

cd backend
pip install --no-cache-dir -r requirements-simple.txt

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✓ Installation Successful!
    echo ========================================
    echo.
    echo Now start the backend:
    echo   cd backend
    echo   python -m uvicorn app.main:app --reload
    echo.
    echo Then in another terminal start frontend:
    echo   cd frontend
    echo   npm install
    echo   npm run dev
    echo.
) else (
    echo.
    echo ========================================
    echo ✗ Installation Failed
    echo ========================================
    echo.
)

pause
