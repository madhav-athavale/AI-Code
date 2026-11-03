!/bin/sh
aws rds describe-db-clusters \
    --db-cluster-identifier northwind-pg-cluster \
    --region us-east-1 \
    --query "DBClusters[0].[Status,Endpoint]" \
    --output table