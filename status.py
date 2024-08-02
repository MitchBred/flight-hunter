import requests
import os


def run(clouds):
    try:
        cloudText = f'The service is currently inactive.\nThe sky is {clouds}% covered with clouds.'
        if clouds <= int(os.getenv('WEATHER_CLOUD_PERCENTAGE')):
            cloudText = f"The service is active.\nThe sky is {clouds}% covered with clouds."

        payload = {
            "status": 201,
            "clouds": cloudText,
        }
        response = requests.post(os.getenv('RASPBERRY_PI_STATUS'), data=payload)
    except:
        print('Server down | wrong request or have no license.', response.status_code)
