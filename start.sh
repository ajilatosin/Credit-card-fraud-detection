#!/bin/bash

# Start FastAPI backend
echo "Starting FastAPI backend..."
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Wait for backend to start
echo "Waiting for backend to be ready..."
sleep 5

# Start Streamlit frontend
echo "Starting Streamlit frontend..."
streamlit run streamlit_app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.headless=true