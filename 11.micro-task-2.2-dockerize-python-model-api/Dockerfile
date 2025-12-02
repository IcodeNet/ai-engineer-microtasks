# Dockerfile for Python FastAPI Model API

# 1. Base image
FROM python:3.11-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy requirements file first (better caching)
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application files
COPY main.py .
COPY registry.py .
COPY text_utils.py .

# 6. Copy registry directory with model files
COPY registry/ ./registry/

# 7. Expose port 8000 for FastAPI
EXPOSE 8000

# 8. Start the API using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]