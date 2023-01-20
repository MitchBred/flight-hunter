from picamera2 import Picamera2
import boto3

picam2 = Picamera2()


def record():
    # flightFormat = str(flightVideo).lower().strip()
    picam2.start_and_record_video("afr76up.mp4", duration=10)
    # upload_video(flightFormat)


def upload_video(flightFormat):
    client = boto3.client(
        's3',
        aws_access_key_id='AKIAVVEMZPXTG4GJY66G',
        aws_secret_access_key='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',
    )

    # image = 'images/flight.jpg'
    video = r'videos/' + flightFormat
    client.upload_file(video, 'mitch-flights', flightFormat)


if __name__ == '__video__':
    record()
