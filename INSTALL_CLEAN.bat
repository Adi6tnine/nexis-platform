@echo off
echo ========================================
echo NEXIS - Clean Installation
echo ========================================
echo.
echo This will clear pip cache and install fresh packages
echo.
pause

cd backend

echo Step 1: Clearing pip cache...
pip cache purge
echo.

echo Step 2: Installing dependencies...
pip install --no-cache-dir -r requirements.txt
echo.

if %errorlevel% equ 0 (
    echo ========================================
    echo ✓ Installation Successful!
    echo ========================================
    echo.
    echo Now start the backend:
    echo   python -m uvicorn app.main:app --reload
    echo.
) else (
    echo ========================================
    echo ✗ Installation Failed
    echo ========================================
    echo.
    echo Please share the error message above.
    echo.
)

pause
