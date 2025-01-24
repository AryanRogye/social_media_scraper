@echo off
setlocal

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Run the Python script with the correct environment
set PYTHONPATH=.
venv\Scripts\python.exe main.py gui

:: Deactivate the virtual environment
call venv\Scripts\deactivate.bat

pause
