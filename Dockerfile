# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the Flask app runs
EXPOSE 5000

# Define environment variable for Flask to run in production
ENV FLASK_ENV=production

# Command to run the Flask application
CMD ["python", "app.py"]
