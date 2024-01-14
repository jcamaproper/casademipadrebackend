# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /casa_de_mi_padre

# Set the PYTHONPATH environment variable
ENV PYTHONPATH /casa_de_mi_padre

# Set the Google Cloud credentials environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS /etc/secrets/gcp-service-account.json

# Copy the current directory contents into the container at /casa_de_mi_padre
COPY . /casa_de_mi_padre

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 10000

# Set environment variables from .env file
ARG ENV_FILE=.env
ENV ENV_FILE_PATH=/casa_de_mi_padre/$ENV_FILE
RUN if [ -f "$ENV_FILE_PATH" ]; then export $(cat $ENV_FILE_PATH | xargs); fi

# Run app.py when the container launches
CMD ["python", "app/main.py"]