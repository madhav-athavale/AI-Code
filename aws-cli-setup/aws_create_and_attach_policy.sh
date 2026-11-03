#!/bin/sh
# Create the policy
aws iam create-policy \
  --policy-name BedrockEvalUserPolicy \
  --policy-document file://bedrock-eval-user-policy.json

# Attach to your user (replace YOUR_USERNAME)
aws iam attach-user-policy \
  --user-name admin \
  --policy-arn arn:aws:iam::806575638863:policy/BedrockEvalUserPolicy