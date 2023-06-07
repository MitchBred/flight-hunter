import os

import boto3
from picamera2 import Picamera2


def record(flightVideo):
    flight = str(flightVideo).lower().strip()

    picam2 = Picamera2()
    picam2.start_and_record_video(flight, duration=20)

    upload_video(flight)


def upload_video(flight):
    client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )
    client.upload_file(flight, 'mitch-flights', flight)
