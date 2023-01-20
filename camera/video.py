from picamera2 import Picamera2
import boto3

picam2 = Picamera2()


def record(flightVideo):
    flight = str(flightVideo).lower().strip()
    print(flight)
    picam2.start_and_record_video(flight, duration=10)
