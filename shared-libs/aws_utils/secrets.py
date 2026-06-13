import boto3
import json
from botocore.exceptions import ClientError
from functools import lru_cache

@lru_cache(maxsize=None)
def get_secret(secret_name, key=None, region_name='us-east-1'):
    """
    Fetch a secret from AWS Secrets Manager.
    
    Args:
        secret_name: name of the secret in AWS
        key: specific key to extract from JSON secret.
             If None, returns the full dict
        region_name: AWS region (default us-east-1)
    
    Returns:
        secret value as string, or full dict if key is None
    
    Example:
        get_secret("Weather_API_KEY", "Weather_API_KEY")
        get_secret("my_app_secrets")  # returns full dict
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])
        
        if key is None:
            return secret          # return full dict
        return secret[key]         # return specific key

    except ClientError as e:
        raise e
    except KeyError:
        raise KeyError(f"Key '{key}' not found in secret '{secret_name}'")
    except json.JSONDecodeError:
        # secret is plain text, not JSON
        return response['SecretString']