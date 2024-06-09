#FROM python:3.11-slim
#
## Set the working directory in the container
#WORKDIR /data
#
## Copy only the files we need for the build
#COPY requirements.txt .
#COPY run.py .
#COPY config.py .
#COPY .env .
#COPY app/ ./app/
#
#
## Install any needed packages specified in requirements.txt
## RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install -r requirements.txt
#
#EXPOSE 5000
#
## Run flask when the container launches
#CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# Use an official Python runtime as a parent image
FROM python:3.11-slim as base

# Set the working directory in the container
WORKDIR /data

## Install system dependencies
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    poppler-utils \
    tesseract-ocr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .
COPY run.py .
COPY config.py .
COPY .env .
COPY app/ ./app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "unstructured[pdf]"

# Final stage
FROM base as final

# Set the working directory in the container
WORKDIR /data

# Expose port
EXPOSE 5002

# Default command
CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]

