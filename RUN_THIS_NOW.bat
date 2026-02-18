@echo off
echo ========================================
echo NEXIS - Fixed Installation
echo ========================================
echo.
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
echo.
echo Done! Now run QUICK_START.bat
pause
