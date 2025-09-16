# Get official base image
FROM python:3.12.2-slim

# Set working directory
WORKDIR /usr/src/app

# Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends netcat-openbsd gcc postgresql \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Install Playwright and its browsers
RUN pip install playwright \
 && playwright install --with-deps

# Add application
COPY . .

