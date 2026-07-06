#!/bin/bash
aws rds create-db-instance \
    --db-instance-identifier my-aurora-writer \
    --db-cluster-identifier my-aurora-cluster \
    --engine aurora-mysql \
    --db-instance-class db.t3.medium