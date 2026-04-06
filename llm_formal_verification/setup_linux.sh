#!/bin/bash
set -e

echo "======================================================"
echo "  LLM Formal Verification - Linux/WSL Setup script"
echo "======================================================"

# 1. System Dependencies (Informative)
echo "[1/4] Checking for system dependencies..."
if ! command -v why3 &> /dev/null; then
    echo "[WARNING] 'why3' not found in PATH."
    echo "[INFO] Try: sudo apt-get update && sudo apt-get install -y why3 alt-ergo"
fi

# 2. Virtual Environment
echo "[2/4] Creating virtual environment (venv)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
else
    echo "[INFO] venv already exists."
fi

# 3. Python Dependencies
echo "[3/4] Installing Python requirements..."
source venv/bin/activate
pip install --upgrade pip > /dev/null
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install requirements."
    exit 1
fi

# 4. Finalizing
echo "[4/4] Creating log directories..."
mkdir -p les_cours logs

echo ""
echo "======================================================"
echo "  SUCCESS! Setup is complete."
echo "  To run: source venv/bin/activate && python3 main.py"
echo "======================================================"
chmod +x main.py 2>/dev/null || true
