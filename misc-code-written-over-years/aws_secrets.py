import boto3
import json
from botocore.exceptions import ClientError 

class AWSSecrets:
    def __init__(self):
        pass
    def get_secret(self, SecretName):
          
        region_name = "us-east-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=SecretName
            )
        except ClientError as e:
            raise e

        secret = get_secret_value_response['SecretString']
        api_key = json.loads(secret)[SecretName]
        
    
        
        return api_key