@echo off
echo ======================================================================
echo NEXIS Platform - Fix Account Creation Loading Issue
echo ======================================================================
echo.
echo This will fix the "stuck loading" issue by:
echo 1. Clearing old users with slow password hashes
echo 2. Instructions to restart backend with fast hashing
echo.
echo ======================================================================
echo.

cd backend

echo Step 1: Clearing old users...
echo.
python clear_users.py

echo.
echo ======================================================================
echo.
echo Step 2: RESTART YOUR BACKEND
echo.
echo 1. Go to the terminal where backend is running
echo 2. Press Ctrl+C to stop it
echo 3. Run this command:
echo.
echo    python -m uvicorn app.main:app --reload
echo.
echo 4. Then try registering again - it will be INSTANT!
echo.
echo ======================================================================
echo.
echo After restarting backend:
echo - Registration: Less than 1 second
echo - Login: Less than 1 second
echo - Everything else: Works normally
echo.
echo ======================================================================
pause
