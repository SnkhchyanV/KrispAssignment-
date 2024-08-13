# Invoker Service Dockerfile
FROM python:3.10.11

WORKDIR /app

COPY invoker.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn invoker:app --host 0.0.0.0 --port 5001
