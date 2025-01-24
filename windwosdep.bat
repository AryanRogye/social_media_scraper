@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python not found. Downloading and installing...
    :: Download Python installer
    curl -o python-installer.exe https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe

    :: Install Python silently (Prepend path, install for all users)
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    :: Cleanup installer
    del python-installer.exe

    echo Python installed successfully.
)

:: Check if npm is installed
npm --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo npm not found. Downloading and installing...

    :: Download and install Node.js
    curl -o node-installer.msi https://nodejs.org/dist/v20.8.1/node-v20.8.1-x64.msi
    start /wait msiexec /i node-installer.msi /quiet /norestart
    del node-installer.msi

    echo npm installed successfully.
)

:: Check if Cargo (Rust) is installed
cargo --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Cargo not found. Downloading and installing...

    :: Download and install Rust
    curl -o rustup-init.exe https://sh.rustup.rs
    start /wait rustup-init.exe -y
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

echo Setup completed successfully.
pause
exit /b 0
