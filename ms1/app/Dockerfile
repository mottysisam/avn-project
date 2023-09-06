# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Set Environment Variables
ENV DEBUG_MODE=INFO
ENV SQS_ENDPOINT=http://localhost:4566
ENV AWS_REGION=us-east-1
ENV QUEUE_URL=https://localhost.localstack.cloud:4566/000000000000/ms1
ENV VALID_TOKEN=$DJISA<$#45ex3RtYr
ENV PORT=5000

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

# how to run
# docker build -t microservice1 .
# docker run -p 5000:5000 \
#   -e DEBUG_MODE=INFO \
#   -e SQS_ENDPOINT=http://localhost:4566 \
#   -e AWS_REGION=us-east-1 \
#   -e QUEUE_URL=https://localhost.localstack.cloud:4566/000000000000/ms1 \
#   -e VALID_TOKEN=$DJISA<$#45ex3RtYr \
#   my_python_app