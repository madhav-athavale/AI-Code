from aws_utils import get_secret
import requests




def get_weather(city):
    #api_key = "b5cd2f38a8c37fc39dfc85ce74c1af5c"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={get_secret("Weather_API_KEY", "Weather_API_KEY")}"   
    response = requests.get(url)
    weather_data = response.json()
    print(response)
    print(f"Weather in {city}: {weather_data['weather'][0]['description']}")
    print(weather_data['coord']['lat'], weather_data['coord']['lon'])
    print(weather_data['main']['temp'])
    


get_weather("Mumbai")
