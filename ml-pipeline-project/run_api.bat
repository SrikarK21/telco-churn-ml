@echo off
REM Activate venv and run uvicorn
call venv\Scripts\activate.bat
uvicorn app.main:app --reload
pause
