# Adobe Hackathon Challenge 1a - PDF Title and Heading Extraction
# Optimized for AMD64 architecture with performance constraints

FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies directly (no requirements.txt needed)
RUN pip install --no-cache-dir PyMuPDF==1.23.26

# Copy the processing script
COPY challenge_processor.py .

# Set environment variables for optimal performance
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Run the PDF processor
CMD ["python", "challenge_processor.py"]