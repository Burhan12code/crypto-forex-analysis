FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir uv && \
    uv pip install --system -r pyproject.toml

# Copy application files
COPY . .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Expose port
EXPOSE 7860

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=app_hf.py

# Run the application
CMD ["python", "app_hf.py"]