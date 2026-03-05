#!/bin/bash

# Quick Test Script for Emare AI

BASE_URL="http://localhost:8888"

echo "🧪 Emare AI Quick Test"
echo "======================="
echo ""

# 1. Health Check
echo "1️⃣  Health Check..."
curl -s $BASE_URL/health | python3 -m json.tool
echo ""

# 2. List Models
echo -e "\n2️⃣  List Models..."
curl -s $BASE_URL/v1/models | python3 -m json.tool | head -20
echo ""

# 3. Simple Chat
echo -e "\n3️⃣  Chat Test..."
curl -s -X POST $BASE_URL/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "messages": [
      {"role": "user", "content": "Merhaba! 2+2 kaç eder?"}
    ],
    "max_tokens": 100
  }' | python3 -m json.tool | grep -A 5 '"content"'

echo -e "\n✅ Test completed!"
