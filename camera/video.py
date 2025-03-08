import os
import time
import boto3
from picamera2 import Picamera2

def record(flightVideo):
    flight = str(flightVideo).lower().strip()

    time.sleep(1)

    picam2 = Picamera2()
    picam2.start_and_record_video(flight, duration=30)

    upload_video(flight)

def upload_video(flight):
    client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        endpoint_url='https://367be3a2035528943240074d0096e0cd.r2.cloudflarestorage.com',
        region_name='auto',
    )

    # Upload file to Cloudflare R2
    bucket_name = 'fls-9e55c72d-5f79-467a-936f-bc2f4a6ea436'
    client.upload_file(flight, bucket_name, flight)

    # Delete the local file after uploading
    os.remove(flight)