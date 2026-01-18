@echo off
REM Activate venv and run training
call venv\Scripts\activate.bat
python src/train.py
pause
