#!/bin/bash
echo "===== Starting Fraud Detection System ====="

# Print Python path for debugging
which python
which uvicorn

# Start FastAPI backend with full path
echo "Starting FastAPI backend on port 8000..."
python -m uvicorn app:app --host 0.0.0.0 --port 8000 &

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 8

# Test if backend is running
echo "Testing backend health..."
curl -s http://localhost:8000/health || echo "Backend not responding yet"

# Start Streamlit frontend
echo "Starting Streamlit frontend..."
streamlit run streamlit_app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.headless=true

wait