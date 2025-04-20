FROM python:3.12-slim

WORKDIR /app

# Install curl for debugging network connectivity
RUN apt-get update && apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Create the downloads directory with proper permissions
RUN mkdir -p downloads && chmod 777 downloads
RUN mkdir -p logs && chmod 777 logs

# Copy the rest of the application
COPY . .

# Make the test script executable
RUN chmod +x test_download.py

# Set environment variables for better logging
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=development

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "-u", "app.py"]