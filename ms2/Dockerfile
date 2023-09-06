# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Set Environment Variables
ENV DEBUG_MODE=INFO
ENV SQS_ENDPOINT=http://localhost:4566
ENV AWS_REGION=us-east-1
ENV QUEUE_URL=https://localhost.localstack.cloud:4566/000000000000/ms1
ENV BUCKET_NAME=messages
ENV POLL_INTERVAL=30

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY app/ /app/

# Expose port for the application
EXPOSE 5000

# Run your application
CMD ["python", "/app/main.py"]

# Howto?
# docker build -t microservice2 .
# docker run -e SQS_ENDPOINT=http://some-other-endpoint -e DEBUG_MODE=DEBUG -p 5000:5000 microservice2