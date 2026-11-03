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


# ─── Log completion ───────────────────────────────────────────
echo "Python setup complete at $(date)" >> /var/log/setup-complete.log