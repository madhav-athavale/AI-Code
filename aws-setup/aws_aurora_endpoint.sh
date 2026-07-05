#!/bin/bash
aws rds describe-db-clusters \
    --db-cluster-identifier my-aurora-cluster \
    --query 'DBClusters[0].Endpoint' \
    --output text