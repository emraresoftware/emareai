#!/bin/bash

# Emare AI - Start Script

echo "🚀 Starting Emare AI v1.0.0..."

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running!"
    echo "Please start Ollama first:"
    echo "  ollama serve"
    exit 1
fi

echo "✅ Ollama is running"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Create logs directory
mkdir -p logs

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found, copying from .env.example"
    cp .env.example .env
fi

# Start the server
echo "🌟 Starting Emare AI API server..."
echo "📡 API will be available at: http://localhost:8888"
echo "📚 API docs: http://localhost:8888/docs"
echo ""

python -m uvicorn api.main:app --host 0.0.0.0 --port 8888 --reload
