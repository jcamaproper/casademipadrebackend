# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
# Add these environment variables to the Dockerfile
ENV PGUSER=devocasademipadre_user
ENV PGPASSWORD=1Oegrjyg9wOSxa3mH8tswFl74BSciK0w
ENV PGHOST=dpg-cme997mn7f5s73fomd50-a.oregon-postgres.render.com
ENV PGPORT=5432
ENV PGDATABASE=devocasademipadre

# Run app.py when the container launches
CMD ["python", "app.py"]