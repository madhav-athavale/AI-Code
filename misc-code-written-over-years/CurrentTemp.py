import requests
import json
import boto3
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "Weather_API_KEY"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId='Weather_API_KEY'
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    print(type(secret))
    print(secret)
    key = json.loads(secret)['Weather_API_KEY']
    print(key)
  
    
    return key


def lambda_handler(event, context):
    print(type(context))
    print(type(event))
    latitude = '40.71427'
    longitude = '-74.00597'
    print(event['latitude'])
    print(event['longitude'])

    query_parameters = {
    "lat": event["latitude"],
    "lon" : event["longitude"],
    "appid" : get_secret()
    }
    

    #api_url = f"https://api.openweathermap.org/data/2.5/weather?lat=40.71427&lon=-74.00597&appid=b5cd2f38a8c37fc39dfc85ce74c1af5c"
    #api_url = f"https://api.openweathermap.org/data/2.5/weather?lat=latitude&lon=longitude&appid=b5cd2f38a8c37fc39dfc85ce74c1af5c"
    api_url = "https://api.openweathermap.org/data/2.5/weather"
   
    response = requests.get(api_url,params=query_parameters)
    json_object = json.loads(response.text)
    print("Hello")
    print(json_object)
    return json_object


if __name__ == '__main--':
    lambda_handler('', '')
