#!/bin/bash
# Script to activate the virtual environment

echo "Activating virtual environment..."
export VIRTUAL_ENV="$(pwd)/venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"

echo "Virtual environment activated!"
echo "You can now run Python scripts with the installed packages."
echo ""
echo "To deactivate, run: deactivate"
echo ""
echo "Available packages:"
pip list
