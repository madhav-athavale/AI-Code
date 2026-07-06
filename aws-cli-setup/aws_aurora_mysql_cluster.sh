#!/bin/bash
aws rds create-db-cluster \
    --db-cluster-identifier my-aurora-cluster \
    --engine aurora-mysql \
    --engine-version 8.0.mysql_aurora.3.08.0 \
    --master-username admin \
    --master-user-password "MySecurePassword123!" \
    --db-subnet-group-name my-db-subnet-group \
    --vpc-security-group-ids sg-0123456789abcdef0 \
    --backup-retention-period 7 \
    --storage-encrypted

#my-db-subnet-group with your DB subnet group
#sg-0123456789abcdef0 with your security group ID
#Password with your own secure password