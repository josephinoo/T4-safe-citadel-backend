# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Expose port 8000 (adjust if your application runs on a different port)
EXPOSE 8000

# Start the backend application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
