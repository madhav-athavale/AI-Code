#!/bin/bash
aws lambda create-function \
    --function-name stock_quote_lambda \
    --runtime python3.13 \
    --handler stock_quote_lambda.get_quote_handler \
    --zip-file fileb://stock_quote_lambda.zip \
    --role arn:aws:iam::806575638863:role/LambdaExecutionRole