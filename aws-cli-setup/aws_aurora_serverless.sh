#!/bin/bash
aws rds create-db-cluster \
    --db-cluster-identifier my-aurora-serverless \
    --engine aurora-mysql \
    --engine-version 8.0.mysql_aurora.3.08.0 \
    --master-username admin \
    --master-user-password "MySecurePassword123!" \
    --db-subnet-group-name my-db-subnet-group \
    --vpc-security-group-ids sg-0123456789abcdef0 \
    --serverless-v2-scaling-configuration MinCapacity=0.5,MaxCapacity=2