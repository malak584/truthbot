#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Start the application
echo "🚀 Starting TruthBot AI Server..."
echo "📍 Web UI: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
python3 app.py
