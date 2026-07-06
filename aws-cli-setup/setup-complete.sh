#!/bin/bash

# ─── System Update ───────────────────────────────────────────
yum update -y

# ─── Install Python & pip ────────────────────────────────────
yum install -y python3 python3-pip tmux git

# ─── Install Python packages ─────────────────────────────────
pip3 install \
  jupyter \
  pandas \
  numpy \
  matplotlib \
  seaborn \
  scikit-learn \
  boto3 \
  anthropic \
  requests \
  python-dotenv

# ─── Configure Jupyter ───────────────────────────────────────
sudo -u ec2-user bash << 'EOF'

# Generate config
jupyter notebook --generate-config

# Set password and config
python3 -c "
from jupyter_server.auth import passwd
pw = passwd('mypassword')
with open('/home/ec2-user/.jupyter/jupyter_notebook_config.py', 'a') as f:
    f.write(f\"c.NotebookApp.password = '{pw}'\n\")
    f.write(\"c.NotebookApp.ip = 'localhost'\n\")
    f.write(\"c.NotebookApp.open_browser = False\n\")
    f.write(\"c.NotebookApp.port = 8888\n\")
"

# Create folder structure
mkdir -p /home/ec2-user/notebooks
mkdir -p /home/ec2-user/data
mkdir -p /home/ec2-user/scripts

EOF

# ─── Fetch API Keys from Secrets Manager ─────────────────────
AWS_REGION="us-east-1"

# Anthropic key
ANTHROPIC_KEY=$(aws secretsmanager get-secret-value \
  --secret-id "ANTHROPIC_API_KEY" \
  --region $AWS_REGION \
  --query 'SecretString' \
  --output text)
echo "export ANTHROPIC_API_KEY=$ANTHROPIC_KEY" >> /home/ec2-user/.bashrc

# OpenWeather key
WEATHER_KEY=$(aws secretsmanager get-secret-value \
  --secret-id "Weather_API_KEY" \
  --region $AWS_REGION \
  --query 'SecretString' \
  --output text)
echo "export WEATHER_API_KEY=$WEATHER_KEY" >> /home/ec2-user/.bashrc

# ─── Create a sample starter notebook ────────────────────────
sudo -u ec2-user python3 -c "
import json

notebook = {
    'nbformat': 4,
    'nbformat_minor': 5,
    'metadata': {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        }
    },
    'cells': [
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': ['# Welcome to your EC2 Jupyter Notebook\n']
        },
        {
            'cell_type': 'code',
            'metadata': {},
            'source': [
                'import os\n',
                'import boto3\n',
                'import pandas as pd\n',
                'import numpy as np\n',
                'import matplotlib.pyplot as plt\n',
                'print(\"All packages loaded!\")\n',
                'print(\"Anthropic key set:\", bool(os.environ.get(\"ANTHROPIC_API_KEY\")))'
            ],
            'outputs': [],
            'execution_count': None
        },
        {
            'cell_type': 'code',
            'metadata': {},
            'source': [
                '# Test Anthropic API\n',
                'import anthropic\n',
                'client = anthropic.Anthropic()\n',
                'response = client.messages.create(\n',
                '    model=\"claude-sonnet-4-20250514\",\n',
                '    max_tokens=100,\n',
                '    messages=[{\"role\": \"user\", \"content\": \"Say hello in one sentence\"}]\n',
                ')\n',
                'print(response.content[0].text)'
            ],
            'outputs': [],
            'execution_count': None
        }
    ]
}

with open('/home/ec2-user/notebooks/starter.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)
"

# ─── Start Jupyter in tmux ────────────────────────────────────
sudo -u ec2-user tmux new-session -d -s jupyter \
  "jupyter notebook --notebook-dir=/home/ec2-user/notebooks"

# ─── Log completion ───────────────────────────────────────────
echo "Python setup complete at $(date)" >> /var/log/setup-complete.log