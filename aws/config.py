import boto3


def upload_to_s3(flight):
    client = boto3.client(
        's3',
        aws_access_key_id='AKIAVVEMZPXTG4GJY66G',
        aws_secret_access_key='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',
    )

    # image = 'images/flight.jpg'
    client.upload_file(flight, 'mitch-flights', flight)
