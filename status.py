import requests
import os


def run():
    try:
        payload = {
            "status": 200
        }
        response = requests.post(os.getenv('RASPBERRY_PI_STATUS'), data=payload)
    except:
        print('Server down | check request.', response.status_code)
