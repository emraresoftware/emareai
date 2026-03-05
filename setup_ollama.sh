#!/bin/bash

# Ollama Setup Script for Emare AI

echo "🔧 Ollama Setup for Emare AI"
echo "=============================="
echo ""

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed"
    ollama --version
else
    echo "📥 Ollama not found. Installing..."
    curl -fsSL https://ollama.ai/install.sh | sh
    echo "✅ Ollama installed"
fi

echo ""
echo "🚀 Starting Ollama service..."
# Start Ollama in background (if not running)
if ! pgrep -x "ollama" > /dev/null; then
    ollama serve &
    sleep 3
    echo "✅ Ollama service started"
else
    echo "✅ Ollama is already running"
fi

echo ""
echo "📦 Downloading recommended models..."
echo ""

# LLaMA 3.1 8B (recommended)
echo "1. LLaMA 3.1 8B (4.7GB) - Recommended"
if ollama list | grep -q "llama3.1:8b"; then
    echo "   ✅ Already downloaded"
else
    echo "   📥 Downloading..."
    ollama pull llama3.1:8b
fi

echo ""
read -p "Do you want to download additional models? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "2. Mistral 7B (4.1GB) - Good for code"
    ollama pull mistral:7b
    
    echo ""
    echo "3. Qwen 2.5 7B (4.7GB) - Better Turkish support"
    ollama pull qwen2.5:7b
fi

echo ""
echo "✅ Setup completed!"
echo ""
echo "Available models:"
ollama list

echo ""
echo "🎯 Next steps:"
echo "  1. Start Emare AI: ./start.sh"
echo "  2. Test API: ./test.sh"
echo "  3. Check docs: http://localhost:8888/docs"
