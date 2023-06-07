from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start_preview(Preview.NULL)


def capture():
    picam2.start()
    time.sleep(2)
    picam2.capture_file("test.jpg")
    picam2.stop()
    print("done")
