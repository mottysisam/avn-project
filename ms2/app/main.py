import boto3
import json
import time
import logging
import os

# Consume Environment Variables and Assign to Local Variables
DEBUG_MODE = os.environ.get("DEBUG_MODE", "INFO")
SQS_ENDPOINT = os.environ.get("SQS_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
QUEUE_URL = os.environ.get("QUEUE_URL", "https://localhost.localstack.cloud:4566/000000000000/my-queue")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "my-bucket")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", 30))

# Initialize logging
logging.basicConfig(level=getattr(logging, DEBUG_MODE.upper()))

def create_s3_bucket_if_not_exists(s3_client, bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logging.info(f"S3 bucket {bucket_name} already exists.")
    except Exception as e:
        logging.info(f"S3 bucket {bucket_name} does not exist. Creating now.")
        s3_client.create_bucket(Bucket=bucket_name)

# Initialize SQS and S3 clients
try:
    sqs = boto3.client('sqs', endpoint_url=SQS_ENDPOINT, region_name=AWS_REGION)
    s3 = boto3.client('s3', endpoint_url=SQS_ENDPOINT, region_name=AWS_REGION)
    create_s3_bucket_if_not_exists(s3, BUCKET_NAME)
except Exception as e:
    logging.error(f"Failed to initialize SQS or S3 client: {e}")
    raise

def poll_sqs_and_upload_to_s3():
    while True:
        try:
            # Poll SQS for messages
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=0
            )

            # If a message is received, process it
            if 'Messages' in response:
                message = response['Messages'][0]
                receipt_handle = message['ReceiptHandle']

                # Upload message to S3
                s3.put_object(
                    Bucket=BUCKET_NAME,
                    Key=f"message-{message['MessageId']}.json",
                    Body=json.dumps(message)
                )

                logging.info(f"Uploaded message {message['MessageId']} to S3")

                # Delete the message from SQS
                sqs.delete_message(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=receipt_handle
                )
            else:
                logging.debug("No messages in the queue")

            # Wait for a given interval before polling again
            time.sleep(POLL_INTERVAL)

        except Exception as e:
            logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    poll_sqs_and_upload_to_s3()
