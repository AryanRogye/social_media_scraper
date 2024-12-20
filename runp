#!/bin/bash

# Activate the virtual environment
source ./venv/bin/activate

# Check if additional arguments are provided
if [ $# -eq 0 ]; then
    # No arguments passed, just run 'parse'
    PYTHONPATH=. ./venv/bin/python3 main.py parse
else
    # Arguments passed, include them with 'parse'
    PYTHONPATH=. ./venv/bin/python3 main.py parse "$@"
fi
