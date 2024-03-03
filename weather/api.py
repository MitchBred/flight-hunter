import os
import requests
from dotenv import find_dotenv, load_dotenv
import json

load_dotenv(find_dotenv())


def clouds():
    global response
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={os.getenv('LAT')}&lon={os.getenv('LON')}&exclude=minutely,hourly,daily,alerts&appid={os.getenv('WEATHER_APP_ID')}"
    print(url)
    try:
        request = requests.get(url)
        response = json.loads(request.text)

        return response['current']['clouds']

    except:
        return response['current']['clouds']
