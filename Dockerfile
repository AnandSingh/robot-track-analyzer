# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY uploads uploads

WORKDIR /app
EXPOSE 5000

CMD ["python", "main.py"]
