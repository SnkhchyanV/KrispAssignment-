# Generator Service Dockerfile
FROM python:3.10.11

WORKDIR /app

COPY generator.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn generator:app  --host 0.0.0.0 --port 5000
