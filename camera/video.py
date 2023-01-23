from picamera2 import Picamera2
import boto3

from aws.config import upload_to_s3

picam2 = Picamera2()


def record(flightVideo):
    flight = str(flightVideo).lower().strip()
    picam2.start_and_record_video(flight, duration=10)
    upload_to_s3(flight)
