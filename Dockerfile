# Start from an official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scraper code into the container
COPY ./scraper /app/scraper

# Tell Docker the command to run when the container starts
# We will override this in docker-compose, but it's good practice
CMD ["python", "scraper/main.py"]