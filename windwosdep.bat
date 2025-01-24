@echo off
setlocal enabledelayedexpansion

:: Exit if any command fails (simulate "set -e" behavior)
call :check_error

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python3 not found. Installing...
    powershell -Command "Start-Process -Verb RunAs -FilePath 'cmd.exe' -ArgumentList '/c winget install Python.Python.3'"
    exit /b 1
)

:: Check if npm is installed
npm --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo npm not found. Installing...
    powershell -Command "Start-Process -Verb RunAs -FilePath 'cmd.exe' -ArgumentList '/c winget install OpenJS.NodeJS'"
    exit /b 1
)

:: Check if Cargo (Rust) is installed
cargo --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Cargo not found. Installing...
    powershell -Command "Invoke-WebRequest -Uri 'https://sh.rustup.rs' -OutFile 'rustup-init.exe' && .\rustup-init.exe -y"
    del rustup-init.exe
)

:: Set up Python virtual environment
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
call venv\Scripts\deactivate

:: Navigate to frontend and install npm packages
cd frontend
npm install

:: Set up Python virtual environment in src-tauri
cd src-tauri
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
call venv\Scripts\deactivate

cd ..
cd ..

echo Script completed successfully.
pause
exit /b 0

:: Function to check for errors and exit if necessary
:check_error
if %ERRORLEVEL% neq 0 (
    echo An error occurred. Exiting script.
    exit /b 1
)
