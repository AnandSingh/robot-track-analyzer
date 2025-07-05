# Use official Ubuntu base image
FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip and system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv python3-dev \
                       build-essential libfreetype6-dev libpng-dev \
                       libopenblas-dev git curl && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application
COPY app app
COPY uploads uploads

# Set workdir to where app runs
WORKDIR /app/app

EXPOSE 5000

CMD ["python3", "main.py"]
