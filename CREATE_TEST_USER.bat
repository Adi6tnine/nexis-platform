@echo off
echo ============================================================
echo Creating Test User for NEXIS Platform
echo ============================================================
echo.
echo This will create a test user account:
echo Email: test@nexis.in
echo Password: Test123!
echo Name: Test User
echo.
echo Starting backend server and creating user...
echo.

cd backend

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Create test user using Python
python -c "import requests; import json; response = requests.post('http://localhost:8000/api/v1/auth/register', json={'name': 'Test User', 'email': 'test@nexis.in', 'phone': '+91 98765 43210', 'password': 'Test123!'}); print('✅ Test user created!' if response.status_code == 200 else f'❌ Error: {response.text}')"

echo.
echo ============================================================
echo Test User Credentials:
echo Email: test@nexis.in
echo Password: Test123!
echo ============================================================
echo.
echo You can now login with these credentials!
echo.
pause
