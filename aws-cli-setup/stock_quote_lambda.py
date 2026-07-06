import boto3
from botocore.exceptions import ClientError
import json
import requests


def get_secret():

    secret_name = "ALPHA_VANTAGE"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    return get_secret_value_response['SecretString']

print(get_secret())
    
def get_quote_handler(event,context):
    url = "https://www.alphavantage.co/query"
    query_parameters = {
                "function": "GLOBAL_QUOTE",
                "symbol": event["ticker"],
                "apikey": get_secret() 
        } 
    
    
    response = requests.get(url,params=query_parameters)
    print(response)
    json_object = json.loads(response.text)
    print(json_object)
    print(json_object['Global Quote']['05. price'])   
    return json_object 



