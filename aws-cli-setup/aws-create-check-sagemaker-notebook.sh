aws sagemaker create-notebook-instance \
  --notebook-instance-name madhav-analysis \
  --instance-type ml.t3.medium \
  --role-arn arn:aws:iam::${ACCOUNT_ID}:role/SageMakerRole \
  --volume-size-in-gb 30 \
  --region us-east-1
Step 5 — Wait for it to start (takes 3-5 minutes):

bash
# Check status
aws sagemaker describe-notebook-instance \
  --notebook-instance-name madhav-analysis \
  --query 'NotebookInstanceStatus' \
  --output text \
  --region us-east-1