#!/bin/bash

# Script to run the Trip Planner with Phoenix observability

echo "🔥 Starting Trip Planner with Arize Phoenix Observability..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import phoenix" 2>/dev/null; then
    echo "📦 Installing Phoenix dependencies..."
    pip install -r requirements.txt
fi

echo "🚀 Starting backend server with Phoenix tracing..."
echo ""
echo "The following will be available:"
echo "  - Backend API: http://localhost:8000"
echo "  - Phoenix UI: http://localhost:6006 (will be shown on startup)"
echo ""

# Run the application
python main.py