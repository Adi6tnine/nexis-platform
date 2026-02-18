@echo off
echo Installing email-validator...
cd backend
pip install email-validator
echo.
echo Done! Now start backend:
echo   python -m uvicorn app.main:app --reload
pause
