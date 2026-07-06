#!/bin/bash
aws rds delete-db-instance \
    --db-instance-identifier my-aurora-instance \
    --skip-final-snapshot \
    --region us-east-1

aws rds delete-db-cluster \
    --db-cluster-identifier my-aurora-cluster \
    --skip-final-snapshot \
    --delete-automated-backups \
    --region us-east-1

    #if deletion protection enabled
    aws rds modify-db-cluster \
    --db-cluster-identifier my-aurora-cluster \
    --no-deletion-protection \
    --apply-immediately \
    --region us-east-1