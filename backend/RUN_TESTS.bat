@echo off
echo ======================================================================
echo NEXIS Platform - Rule-Based System Test Suite
echo ======================================================================
echo.

cd /d "%~dp0"

echo Running tests...
echo.

python -m pytest tests/ -v --tb=short --color=yes -ra

echo.
echo ======================================================================
echo Test run complete!
echo ======================================================================
pause
