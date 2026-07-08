#!/bin/bash
aws rds create-db-instance \
    --region us-east-1 \
    --db-instance-identifier my-learning-mysql \
    --db-name learningdb \
    --db-instance-class db.t4g.micro \
    --engine mysql \
    --engine-version 8.0 \
    --master-username admin \
    --master-user-password 'Pma94029#' \
    --allocated-storage 20 \
    --storage-type gp3 \
    --backup-retention-period 1 \
    --no-multi-az \
    --publicly-accessible