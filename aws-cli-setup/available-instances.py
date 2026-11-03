import boto3

sm_client = boto3.client('sagemaker', region_name='us-east-1')

# List available instance types
response = boto3.client('service-quotas', region_name='us-east-1').list_service_quotas(
    ServiceCode='sagemaker'
)
print(response)

# Filter for training instances with quota > 0
for quota in response['Quotas']:
    if 'training' in quota['QuotaName'].lower() and quota['Value'] > 0:
        print(f"{quota['QuotaName']}: {quota['Value']}")