from io import BytesIO
import requests
import os
import logging
import boto3
import json

RANDOM_DOG_URL = os.environ[
    "RANDOM_DOG_URL"
]  # "https://dog.ceo/api/breeds/image/random"

AWS_BUCKET_NAME = os.environ["AWS_BUCKET_NAME"]

logger = logging.getLogger()
logger.setLevel("INFO")


s3 = boto3.resource("s3")
bucket = s3.Bucket(AWS_BUCKET_NAME)


def handler(event, context):
    url_res = requests.get(RANDOM_DOG_URL)

    if url_res.status_code != 200:
        logger.error("Did not successfully retrieve a random dog photo url :(")
        return

    json_url_response = json.loads(url_res.content)

    dog_url = json_url_response["message"]

    dog_res = requests.get(dog_url)

    # <dog_breed>/<file_name> for nice structured S3 uploads.
    dog_breed_and_name = "/".join(dog_url.split("/")[-2:])

    if dog_res.status_code != 200:
        logger.error("Did not successfully retrieve a dog photo :(")
        return

    dog_image = dog_res.content

    bucket.upload_fileobj(BytesIO(dog_image), dog_breed_and_name)

    logger.info("Successful upload: {}".format(dog_breed_and_name))
