#!/bin/bash
set -e

echo "Installing CodeCanopy..."

# Check if Python 3.7+ is available
python3 --version >/dev/null 2>&1 || {
    echo "Error: Python 3.7 or higher is required"
    exit 1
}

# Install in development mode
pip install -e .

echo "Installation complete!"
echo ""
echo "Usage:"
echo "  codecanopy tree --focus src --ignore node_modules"
echo "  codecanopy cat \"src/**/*.py\" --exclude \"**/*.test.py\""
echo ""
echo "Run 'codecanopy --help' for more information."