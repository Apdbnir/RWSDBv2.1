#!/bin/bash
# BerkeleyDB Setup Script for WSL/Ubuntu
# This script installs BerkeleyDB C library and Python bindings

set -e  # Exit on error

echo "=================================="
echo "BerkeleyDB Setup for WSL/Ubuntu"
echo "=================================="
echo ""

# Update package list
echo "Step 1: Updating package list..."
sudo apt-get update

# Install BerkeleyDB C library
echo ""
echo "Step 2: Installing BerkeleyDB C library..."
sudo apt-get install -y libdb-dev libdb5.3 libdb5.3-dev

# Install Python dependencies
echo ""
echo "Step 3: Installing Python dependencies..."

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install bsddb3 (Python bindings for BerkeleyDB)
echo "Installing bsddb3 Python package..."
pip install bsddb3

# Install other project dependencies
echo "Installing other project dependencies..."
pip install -r backend/requirements.txt

# Verify installation
echo ""
echo "=================================="
echo "Verifying installation..."
echo "=================================="

python3 -c "
try:
    from berkeleydb import db
    print('✓ berkeleydb Python package: INSTALLED')
except ImportError:
    try:
        import bsddb3
        print('✓ bsddb3 Python package: INSTALLED')
    except ImportError:
        print('✗ BerkeleyDB Python package: NOT FOUND')
        exit(1)
"

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "You can now run the BerkeleyDB converter:"
echo "  python backend/berkeleydb_converter.py"
echo ""
