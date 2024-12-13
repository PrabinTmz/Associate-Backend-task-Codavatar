FROM python:3.12-slim

ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential libpq-dev \
    && pip install --no-cache-dir --upgrade pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create a non-root user with ID 1000
RUN groupadd -g 1000 appgroup && \
    useradd -m -u 1000 -g appgroup appuser


# Set ownership of the app directory
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code with correct permission
COPY --chown=appuser:appgroup ./app ./   

# Ensure `uvicorn` is available in PATH
ENV PATH="/home/appuser/.local/bin:$PATH"

# Expose the application port
EXPOSE 8000

# run application in reload mode for development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 

#  For production, use multiple workers to handle concurrency
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
