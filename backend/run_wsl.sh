#!/bin/bash
# Run the RWSDB backend server from WSL/Ubuntu

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR/backend"

echo "=================================="
echo "Starting RWSDB backend server in WSL"
echo "=================================="

# Prefer python3 if available
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    PYTHON=python
fi

echo "Using interpreter: $(command -v "$PYTHON")"

# Activate virtual environment if present
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Running server..."
$PYTHON __main__.py
