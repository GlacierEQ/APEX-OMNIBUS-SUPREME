FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    httpx \
    python-dotenv \
    pydantic \
    mem0ai \
    neo4j

# Copy application
COPY api.py /app/

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
