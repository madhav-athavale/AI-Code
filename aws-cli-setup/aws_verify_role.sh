#!/bin/bash
aws iam get-role --role-name SageMakerRole --query 'Role.Arn' --output text