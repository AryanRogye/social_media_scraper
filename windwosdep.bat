@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python not found. Downloading and installing...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
    echo Python installed successfully.
)

:: Check if npm is installed
npm --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo npm not found. Downloading and installing...
    curl -o node-installer.msi https://nodejs.org/dist/v20.8.1/node-v20.8.1-x64.msi
    start /wait msiexec /i node-installer.msi /quiet /norestart
    del node-installer.msi
    echo npm installed successfully.
)

:: Check if Cargo (Rust) is installed
cargo --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Cargo not found. Downloading and installing...

    :: Detect system architecture
    wmic os get osarchitecture | find "64-bit" >nul
    if %ERRORLEVEL% equ 0 (
        echo Detected 64-bit OS.
        curl -o rustup-init.exe https://win.rustup.rs/x86_64
    ) else (
        echo Detected 32-bit OS.
        curl -o rustup-init.exe https://win.rustup.rs/i686
    )

    :: Run Rust installer
    start /wait rustup-init.exe -y
    del rustup-init.exe
    echo Rust installed successfully.
)


:: Set up Python virtual environment in the root directory
python -m venv venv
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Error: Failed to create virtual environment.
    exit /b 1
)
pip install -r wrequirements.txt
call venv\Scripts\deactivate.bat

:: Navigate to frontend and install npm packages
cd frontend
if exist package.json (
    npm install
) else (
    echo Error: package.json not found in frontend directory.
    exit /b 1
)
cd ..

:: Set up Python virtual environment in src-tauri directory
cd src-tauri
python -m venv venv
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Error: Failed to create virtual environment in src-tauri.
    exit /b 1
)
pip install -r requirements.txt
call venv\Scripts\deactivate.bat
cd ..

cd ..

echo Setup completed successfully.
pause
exit /b 0
