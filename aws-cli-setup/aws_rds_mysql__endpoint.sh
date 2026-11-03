aws rds describe-db-instances \
    --db-instance-identifier my-learning-mysql \
    --region us-east-1 \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text