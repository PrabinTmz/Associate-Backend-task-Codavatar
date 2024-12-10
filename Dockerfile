FROM python:3.12-slim

ENV PYTHONPATH=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential libpq-dev \
    && pip install --no-cache-dir --upgrade pip
    
WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

EXPOSE 8000

CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "8000", "--reload"]