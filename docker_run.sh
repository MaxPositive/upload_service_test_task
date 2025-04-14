#!/bin/bash
set -e

echo "Applying database migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
uvicorn upload_service.entrypoints.fastapi_app:get_app --host 0.0.0.0 --port 8000 --reload