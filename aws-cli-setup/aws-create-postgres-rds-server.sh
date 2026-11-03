#/bin/sh
aws rds create-db-instance \
    --db-instance-identifier northwind-pg-instance-1 \
    --db-cluster-identifier northwind-pg-cluster \
    --engine aurora-postgresql \
    --db-instance-class db.t4g.medium \
    --region us-east-1