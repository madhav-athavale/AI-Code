#!/bin/bash
aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=my-server" \
  --query 'Reservations[*].Instances[*].PublicIpAddress' \
  --output text \
  --region us-east-1