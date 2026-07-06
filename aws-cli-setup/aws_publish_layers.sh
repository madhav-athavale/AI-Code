#!/bin/bash  
aws lambda publish-layer-version \
  --layer-name requests-layer \
  --zip-file fileb://requests-layer.zip \
  --compatible-runtimes python3.13