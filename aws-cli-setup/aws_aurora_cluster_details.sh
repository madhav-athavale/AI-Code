!/bin/bash
aws rds describe-db-clusters \
    --region us-east-1 \
    --query 'DBClusters[*].[DBClusterIdentifier,Status,Engine]' \
    --output table

aws rds describe-db-instances \
    --region us-east-1 \
    --query 'DBInstances[*].[DBInstanceIdentifier,DBClusterIdentifier,Engine,DBInstanceStatus]' \
    --output table