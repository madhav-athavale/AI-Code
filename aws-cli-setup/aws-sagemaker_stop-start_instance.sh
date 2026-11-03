#!/bin/bash
aws sagemaker stop-notebook-instance \
  --notebook-instance-name madhav-analysis \
  --region us-east-1
Start it again:

bash
aws sagemaker start-notebook-instance \
  --notebook-instance-name madhav-analysis \
  --region us-east-1