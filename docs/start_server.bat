@echo off
REM Kill all Python processes
taskkill /F /IM python* 2>nul
timeout /t 3 /nobreak >nul

REM Clear environment
set PYTHONDONTWRITEBYTECODE=1
set PYTHONUNBUFFERED=1

REM Start server from correct directory
cd C:\VS_Code\RWSDBv2.1
echo Starting server from: %CD%
python -B server.py
