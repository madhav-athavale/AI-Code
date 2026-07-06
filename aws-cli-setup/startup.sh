#!/bin/bash

# ----------------------------------------
# Log everything
# ----------------------------------------
LOG_FILE=/var/log/user-data.log
exec > >(tee -a $LOG_FILE) 2>&1
set -euxo pipefail
trap 'echo "❌ ERROR at line $LINENO"' ERR

echo "===== Starting EC2 setup at $(date) ====="

# ----------------------------------------
# Variables
# ----------------------------------------
APP_USER="ec2-user"
APP_DIR="/home/ec2-user/app"
PYTHON_BIN="/usr/bin/python3.11"
S3_REQUIREMENTS="s3://mva-python-code/requirements-core.txt"
VENV_DIR="$APP_DIR/venv"
TMP_PIP_DIR="/home/ec2-user/tmp"

# ----------------------------------------
# 1. Install system dependencies
# ----------------------------------------
dnf update -y
dnf install -y python3.11 python3.11-pip git \
    gcc gcc-c++ make python3-devel libffi-devel openssl-devel

# ----------------------------------------
# 2. Prepare app directory and pip tmp
# ----------------------------------------
mkdir -p "$APP_DIR" "$TMP_PIP_DIR"
chmod 777 "$TMP_PIP_DIR"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

# ----------------------------------------
# 3. Download requirements-core.txt from S3 (retry 5x)
# ----------------------------------------
echo "Downloading requirements-core.txt from S3..."
for i in {1..5}; do
    if aws s3 cp "$S3_REQUIREMENTS" "$APP_DIR/requirements-core.txt"; then
        break
    fi
    echo "Retry $i failed, waiting 5s..."
    sleep 5
done
if [ ! -f "$APP_DIR/requirements-core.txt" ]; then
    echo "❌ Failed to download requirements-core.txt"
    exit 1
fi

# ----------------------------------------
# 4. Setup virtual environment & install packages
# ----------------------------------------
sudo -u "$APP_USER" bash << 'EOF'
set -euxo pipefail

APP_DIR="/home/ec2-user/app"
VENV_DIR="$APP_DIR/venv"
PYTHON_BIN="/usr/bin/python3.11"
TMP_PIP_DIR="/home/ec2-user/tmp"

cd "$APP_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_BIN -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Upgrade pip & tools
pip install --upgrade pip setuptools wheel

# Export TMPDIR for pip builds to avoid /tmp space limits
export TMPDIR="$TMP_PIP_DIR"

# Install packages safely
pip install --no-cache-dir -r requirements-core.txt --upgrade -v 

# Verify key packages
python -c "import numpy; print('numpy OK', numpy.__version__)"
python -c "import pandas; print('pandas OK', pandas.__version__)"
python -c "import torch; print('torch OK', torch.__version__)"

# Clean pip cache after installation
rm -rf "$TMP_PIP_DIR"
rm -rf ~/.cache/pip

EOF

# ----------------------------------------
# 5. Fix ownership
# ----------------------------------------
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

echo "===== EC2 setup complete at $(date) ====="