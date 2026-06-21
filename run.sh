#!/bin/bash

cd "$(dirname "$0")"

echo "Checking virtual environment..."

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."

    python3 -m venv venv

    source venv/bin/activate

    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Using existing virtual environment..."

    source venv/bin/activate
fi

echo "Starting FastAPI..."
uvicorn backend.app.main:app --reload &

sleep 3

echo "Starting Streamlit..."
streamlit run frontend/streamlit_app.py &

echo ""
echo "Project is running!"
echo "FastAPI: http://127.0.0.1:8000/docs"
echo "Streamlit: http://localhost:8501"

wait