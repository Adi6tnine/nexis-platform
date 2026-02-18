@echo off
echo ========================================
echo Reset Database
echo ========================================
echo.
echo This will delete the old database and create a new one
echo with the correct schema for the rule-based system.
echo.
pause

del nexis.db 2>nul

echo.
echo Database deleted. The backend will create a new one on next startup.
echo.
echo Now restart the backend:
echo   python -m uvicorn app.main:app --reload
echo.
pause
