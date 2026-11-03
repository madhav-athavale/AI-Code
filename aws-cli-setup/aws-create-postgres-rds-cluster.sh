#/bin/sh
aws rds create-db-cluster \
    --db-cluster-identifier northwind-pg-cluster \
    --engine aurora-postgresql \
    --master-username postgres \
    --manage-master-user-password \
    --db-subnet-group-name default \
    --vpc-security-group-ids sg-0e99c800c745a0db6 \
    --region us-east-1