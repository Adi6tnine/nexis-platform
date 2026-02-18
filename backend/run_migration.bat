@echo off
echo Running database migration...
call venv\Scripts\activate.bat
alembic upgrade head
echo Migration complete!
pause
