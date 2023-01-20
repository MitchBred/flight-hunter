from picamera2 import Picamera2
import boto3

picam2 = Picamera2()


def record():
    # flightFormat = str(flightVideo).lower().strip()
    picam2.start_and_record_video("afr76up.mp4", duration=10)
    # upload_video(flightFormat)
