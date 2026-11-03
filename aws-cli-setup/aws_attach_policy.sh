#bin/bash
aws iam put-role-policy \
  --role-name LambdaExecutionRole \
  --policy-name ReadAlphaVantageSecret \
  --policy-document file://secrets-policy.json