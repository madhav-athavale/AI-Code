##!/bin/bash
aws ec2 describe-security-groups \
    --region us-east-1 \
    --query "SecurityGroups[*].[GroupId,GroupName]" \
    --output table