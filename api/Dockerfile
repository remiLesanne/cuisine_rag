FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY api/requirements.txt api_requirements.txt
COPY rag_engine/requirements.txt rag_requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r rag_requirements.txt
RUN pip install --no-cache-dir -r api_requirements.txt

# Copy code
COPY rag_engine /app/rag_engine
COPY api /app/api
COPY .env /app/.env

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
