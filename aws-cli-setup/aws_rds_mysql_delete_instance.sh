#!/bin/bash
aws rds delete-db-instance \
    --db-instance-identifier my-learning-mysql \
    --skip-final-snapshot \
    --delete-automated-backups \
    --region us-east-1

## Wait until deletion completes
aws rds wait db-instance-deleted \
    --db-instance-identifier my-learning-mysql \
    --region us-east-1