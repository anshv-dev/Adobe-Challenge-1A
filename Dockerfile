# Adobe Hackathon Challenge 1a - PDF Processing Docker Container
# Optimized for AMD64 architecture with performance constraints

FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the processing script
COPY process_pdfs.py .

# Set environment variables for optimal performance
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Run the PDF processor
CMD ["python", "process_pdfs.py"]