#!/bin/sh
aws iam create-role \
  --role-name BedrockEvalRole \
  --assume-role-policy-document file://trust-policy.json