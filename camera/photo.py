from picamera2 import Picamera2, Preview
import time

from aws.config import upload_to_s3

picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start_preview(Preview.NULL)


def capture():
    flight = r'images/flight.jpg'
    picam2.start()
    time.sleep(2)
    picam2.capture_file(flight)
    picam2.stop()
    upload_to_s3(flight)
