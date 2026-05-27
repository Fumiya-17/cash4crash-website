@echo off
echo Starting Cash4Crash Backend API...
call venv\Scripts\activate.bat
uvicorn main:app --reload --port 8000
pause
