#!/bin/sh
aws iam put-role-policy \
  --role-name BedrockEvalRole \
  --policy-name $1 \
  --policy-document file://$2