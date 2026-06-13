#!/bin/bash
aws s3 sync s3://mva-python-code s3://mva-python-code-east --source-region us-west-2 --region us-east-1
