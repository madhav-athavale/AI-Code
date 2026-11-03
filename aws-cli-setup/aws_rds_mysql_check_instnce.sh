#!/bin/bash
aws rds describe-db-instances \
    --db-instance-identifier my-learning-mysql \
    --region us-east-1