#!/bin/bash

# Exit if any command fails
set -e

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Installing..."
    sudo apt update && sudo apt install python3 python3-venv python3-pip -y
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm not found. Installing..."
    sudo apt install npm -y
fi

# Check if Cargo (Rust) is installed
if ! command -v cargo &> /dev/null; then
    echo "Cargo not found. Installing..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
fi

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd frontend
npm install
cd src-tauri
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..
cd ..
