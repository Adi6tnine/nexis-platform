@echo off
echo ======================================================================
echo NEXIS Platform - Clear Users and Restart Backend
echo ======================================================================
echo.
echo This will:
echo 1. Clear all existing users (they had slow password hashing)
echo 2. Allow you to register new users with FAST authentication
echo.
echo ======================================================================
echo.

cd /d "%~dp0"

echo Step 1: Clearing users...
echo.
python clear_users.py

echo.
echo ======================================================================
echo.
echo Users cleared! Now restart your backend:
echo.
echo   python -m uvicorn app.main:app --reload
echo.
echo Then register a new user - sign-in will be INSTANT!
echo.
echo ======================================================================
pause
