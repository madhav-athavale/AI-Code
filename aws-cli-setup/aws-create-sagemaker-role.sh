#!/bin/bash
aws iam create-role \
  --role-name SageMakerRole \
  --assume-role-policy-document file:///tmp/sagemaker-trust-policy.json

# Attach required policies
aws iam attach-role-policy \
  --role-name SageMakerRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess

aws iam attach-role-policy \
  --role-name SageMakerRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

aws iam attach-role-policy \
  --role-name SageMakerRole \
  --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite
