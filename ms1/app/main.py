from flask import Flask, request, jsonify
import boto3
import json
import logging
import os

# Consume Environment Variables and Assign to Local Variables
DEBUG_MODE = os.environ.get("DEBUG_MODE", "INFO")
SQS_ENDPOINT = os.environ.get("SQS_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
QUEUE_NAME = os.environ.get("QUEUE_NAME", "my-queue")
VALID_TOKEN = os.environ.get("VALID_TOKEN", "$DJISA<$#45ex3RtYr")
PORT = int(os.environ.get("PORT", 5000))

# Initialize Logging
logging.basicConfig(level=getattr(logging, DEBUG_MODE.upper()))

# Initialize Flask app
app = Flask(__name__)

# Initialize SQS client
try:
    sqs = boto3.client('sqs', endpoint_url=SQS_ENDPOINT, region_name=AWS_REGION)
except Exception as e:
    logging.error(f"Failed to initialize SQS client: {e}")
    raise

# Auto-create queue if not exists
try:
    response = sqs.create_queue(QueueName=QUEUE_NAME)
    queue_url = response['QueueUrl']
    logging.info(f"Queue {queue_url} created or already exists")
except Exception as e:
    logging.error(f"Failed to create SQS queue: {e}")
    raise

@app.route('/process', methods=['POST'])
def process_request():
    try:
        payload = request.json

        # Validate the token
        token = payload.get('token', "")
        if token != VALID_TOKEN:
            logging.warning("Invalid token received.")
            return jsonify({"error": "Invalid token"}), 401

        # Validate payload has the required fields under 'data'
        data = payload.get('data', {})
        if all(k in data for k in ("email_subject", "email_sender", "email_timestream", "email_content")):
            # Publish to SQS
            response = sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(payload)
            )
            return jsonify({"success": True, "messageId": response['MessageId']})
        else:
            logging.warning("Invalid payload received.")
            return jsonify({"error": "Invalid payload"}), 400

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": f"An internal error occurred {e}"}), 500

if __name__ == '__main__':
    app.run(port=PORT, debug=(DEBUG_MODE.lower() == 'debug'))
