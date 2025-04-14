FROM python:3.13-slim
WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY upload_service/ ./upload_service/
COPY alembic.ini ./
COPY docker.env ./
COPY docker_run.sh ./

RUN chmod +x docker_run.sh

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["./docker_run.sh"]