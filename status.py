import requests
import os


def run(clouds):
    try:
        clouds = f'The service is currently inactive.\nThe sky is {clouds}% covered with clouds.'
        if clouds < os.getenv('WEATHER_CLOUD_PERCENTAGE'):
            clouds = f"The service is active.\nThe sky is {clouds}% covered with clouds."

        payload = {
            "status": 201,
            "clouds": {clouds}
        }
        response = requests.post(os.getenv('RASPBERRY_PI_STATUS'), data=payload)
    except:
        print('Server down | check request.', response.status_code)
