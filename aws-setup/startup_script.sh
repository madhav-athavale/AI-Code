#!/bin/bash

# ─── Log everything ──────────────────────────────────────────
exec > /var/log/setup.log 2>&1
echo "Setup started at $(date)"

# ─── System Update ───────────────────────────────────────────
yum update -y
yum install -y tmux git curl unzip gcc gcc-c++ make

# ─── Install AWS CLI v2 ───────────────────────────────────────
echo "Installing AWS CLI v2..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf awscliv2.zip aws/

# Verify
aws --version
echo "AWS CLI v2 installed"

# ─── Install Miniconda as ec2-user ───────────────────────────
echo "Installing Miniconda..."
sudo -u ec2-user bash << 'EOF'
cd /home/ec2-user

# Download Miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install silently
bash Miniconda3-latest-Linux-x86_64.sh -b -p /home/ec2-user/miniconda3

# Remove installer
rm Miniconda3-latest-Linux-x86_64.sh

# Add conda to PATH
echo 'export PATH=/home/ec2-user/miniconda3/bin:$PATH' >> /home/ec2-user/.bashrc
echo 'source /home/ec2-user/miniconda3/etc/profile.d/conda.sh' >> /home/ec2-user/.bashrc

export PATH=/home/ec2-user/miniconda3/bin:$PATH
source /home/ec2-user/miniconda3/etc/profile.d/conda.sh

# Accept conda ToS
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Add conda-forge channel
conda config --add channels conda-forge
conda config --set channel_priority strict

echo "Miniconda installed"
EOF

# ─── Create Python 3.13 environment ──────────────────────────
echo "Creating Python 3.13 environment..."
sudo -u ec2-user bash << 'EOF'
export PATH=/home/ec2-user/miniconda3/bin:$PATH
source /home/ec2-user/miniconda3/etc/profile.d/conda.sh

# Create environment
conda create --name py313 --yes python=3.13 pip

echo "Python 3.13 environment created"
EOF

# ─── Download requirements.txt from S3 ───────────────────────
echo "Downloading requirements.txt from S3..."
aws s3 cp s3://mva-python-code/requirements.txt /home/ec2-user/requirements.txt \
  --region us-east-1

# Strip version numbers and fix common issues
sed -i 's/==[0-9].*//' /home/ec2-user/requirements.txt   # remove ==x.x.x
sed -i 's/>=[0-9].*//' /home/ec2-user/requirements.txt   # remove >=x.x.x
sed -i 's/<=[0-9].*//' /home/ec2-user/requirements.txt   # remove <=x.x.x

echo "requirements.txt downloaded and cleaned"
cat /home/ec2-user/requirements.txt

# ─── Install Python packages ──────────────────────────────────
echo "Installing Python packages..."
sudo -u ec2-user bash << 'EOF'
export PATH=/home/ec2-user/miniconda3/bin:$PATH
source /home/ec2-user/miniconda3/etc/profile.d/conda.sh
conda activate py313

# Install from requirements.txt
pip install --prefer-binary -r /home/ec2-user/requirements.txt

# Install essential packages not in requirements.txt
pip install --prefer-binary \
  boto3 \
  anthropic \
  python-dotenv \
  ipykernel

echo "Python packages installed"
EOF

# ─── Fetch API keys from Secrets Manager ─────────────────────
echo "Fetching API keys..."
AWS_REGION="us-east-1"

WEATHER_KEY=$(aws secretsmanager get-secret-value \
  --secret-id "Weather_API_KEY" \
  --region $AWS_REGION \
  --query 'SecretString' \
  --output text 2>/dev/null)

if [ ! -z "$WEATHER_KEY" ]; then
  # Extract key from JSON
  WEATHER_KEY_VALUE=$(echo $WEATHER_KEY | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['Weather_API_KEY'])")
  echo "export WEATHER_API_KEY=$WEATHER_KEY_VALUE" >> /home/ec2-user/.bashrc
  echo "Weather API key fetched"
else
  echo "WARNING: Could not fetch Weather API key"
fi

# ─── Create project folder structure ─────────────────────────
sudo -u ec2-user bash << 'EOF'
mkdir -p /home/ec2-user/projects
mkdir -p /home/ec2-user/data
mkdir -p /home/ec2-user/scripts
echo "Folder structure created"
EOF

# ─── Auto activate py313 on login ────────────────────────────
echo 'conda activate py313' >> /home/ec2-user/.bashrc

# ─── Verify installations ─────────────────────────────────────
echo "─── Verifying installations ───"
sudo -u ec2-user bash << 'EOF'
export PATH=/home/ec2-user/miniconda3/bin:$PATH
source /home/ec2-user/miniconda3/etc/profile.d/conda.sh
conda activate py313

echo "Python version:"
python --version

echo "Installed packages:"
python -c "
import importlib
packages = ['boto3', 'anthropic', 'requests', 'dotenv']
for pkg in packages:
    try:
        importlib.import_module(pkg)
        print(f'  ✓ {pkg}')
    except ImportError:
        print(f'  ✗ {pkg} MISSING')
"
EOF

echo "─── Setup complete at $(date) ───"