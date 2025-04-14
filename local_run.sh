#!/bin/bash
set -e
PYTHON_CMD="python3"
if ! $PYTHON_CMD --version | grep -q "3.13"; then
    echo "Error: Python 3.13 is required. Please install Python 3.13."
    exit 1
fi
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
fi
echo "Activating virtual environment..."
source .venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Applying database migrations..."
alembic upgrade head
echo "Starting FastAPI server..."
uvicorn upload_service.entrypoints.fastapi_app:get_app --host 0.0.0.0 --port 8000 --reload