aws rds describe-db-instances \
    --db-instance-identifier northwind-pg-instance-1 \
    --region us-east-1 \
    --query "DBInstances[0].DBInstanceStatus" \
    --output text