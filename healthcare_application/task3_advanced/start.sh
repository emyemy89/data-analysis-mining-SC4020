#!/bin/bash

# Quick start script - runs everything needed
# Use this after setup is complete

set -e

echo "============================================"
echo "  Health Assistant - Quick Start"
echo "============================================"
echo ""

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "Port $1 is already in use"
        return 1
    fi
    return 0
}

# Check if models exist
if [ ! -d "models" ] || [ -z "$(ls -A models 2>/dev/null)" ]; then
    echo "Models not found. Running training..."
    python train-models-script.py
fi

# Check ports
echo "Checking ports..."
if ! check_port 5000; then
    echo "Please stop the service using port 5000 first"
    exit 1
fi

# Start backend
echo "Starting backend server..."
source venv/bin/activate || source venv/Scripts/activate
python app.py &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"

echo ""
echo "============================================"
echo "  Health Assistant is Running!"
echo "============================================"
echo ""
echo "Backend API: http://localhost:5000"
echo "API Docs: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Wait for interrupt
trap "kill $BACKEND_PID 2>/dev/null; echo 'Server stopped'; exit" INT TERM

wait $BACKEND_PID
