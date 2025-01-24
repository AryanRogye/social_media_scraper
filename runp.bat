@echo off
setlocal

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Check if arguments are provided
if "%~1"=="" (
    echo No arguments passed, running 'parse'...
    set PYTHONPATH=.
    venv\Scripts\python.exe main.py parse
) else (
    echo Arguments passed, running 'parse' with arguments...
    set PYTHONPATH=.
    venv\Scripts\python.exe main.py parse %*
)

:: Deactivate the virtual environment
call venv\Scripts\deactivate.bat

pause
