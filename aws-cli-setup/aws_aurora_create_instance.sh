#!/bin/bash
aws rds create-db-instance \
    --db-instance-identifier my-aurora-serverless-instance \
    --db-cluster-identifier my-aurora-serverless \
    --db-instance-class db.serverless \
    --engine aurora-mysql