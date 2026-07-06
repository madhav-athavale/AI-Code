#!/bin/bash
aws lambda update-function-configuration \
  --function-name stock_quote_lambda \
  --layers arn:aws:lambda:us-east-1:806575638863:layer:requests-layer:2