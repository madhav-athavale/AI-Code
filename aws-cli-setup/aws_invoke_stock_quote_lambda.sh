aws lambda invoke \
    --function-name stock_quote_lambda \
    --cli-binary-format raw-in-base64-out \
    --log-type Tail \
    --payload '{"ticker" : "msft"}' \
    /dev/stdout | jq -r '.LogResult'|base64 --decode