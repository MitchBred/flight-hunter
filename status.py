import requests
import os


def run():
    payload = {
        "status": 200
    }
    requests.post(os.getenv('RASPBERRY_PI_STATUS'), data=payload)
