#!/bin/bash

# Define the virtual environment directory
VENV_DIR="venv"

# Check if the virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
  echo "Virtual environment not found. Setting it up..."
  python3 -m venv $VENV_DIR
  source $VENV_DIR/bin/activate
else
  # If the virtual environment exists, just activate it
  echo "Activating virtual environment..."
  source $VENV_DIR/bin/activate
fi

echo "Installing required packages..."
pip install -r requirements.txt

# Pass any arguments (flags) received by the script to main.py
echo "Running main.py with the provided arguments..."
python main.py "$@"

# Deactivate the virtual environment
deactivate
echo "Virtual environment deactivated."
