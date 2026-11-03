aws lambda invoke \
    --function-name CurrentTemp \
    --cli-binary-format raw-in-base64-out \
    --log-type Tail \
    --payload '{"latitude" : "40.00000",  "longitude" : "-74.00000"}' \
    /dev/stdout