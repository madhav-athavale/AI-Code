import requests
import boto3
from botocore.exceptions import ClientError
import json


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

    # Your code goes here.



def get_weather(city):
    #api_key = "b5cd2f38a8c37fc39dfc85ce74c1af5c"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={get_secret()}"   
    response = requests.get(url)
    weather_data = response.json()
    print(weather_data)
    print(f"Weather in {city}: {weather_data['weather'][0]['description']}")
    print(weather_data['coord']['lat'], weather_data['coord']['lon'])
    print(weather_data['main']['temp'])



get_weather("Mumbai")