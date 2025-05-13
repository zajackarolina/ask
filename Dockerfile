# Use an official Python image
FROM python:3.11-slim

# Install system dependencies (nodejs, npm, git for good measure)
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python dependencies first
COPY ./requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY app/ /app/

# Install Node.js dependencies
RUN npm install

# Build Tailwind CSS
RUN npm run build

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Expose Flask port
EXPOSE 5000

# Run the Flask app
ENTRYPOINT ["/app/entrypoint.sh"]