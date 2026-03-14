#!/bin/bash
# 🚀 خزانتي الرقمية - Startup Script

cd "$(dirname "$0")"

echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

echo "🚀 Starting server..."
echo "📍 Open: http://localhost:8000"
echo "🛑 Press Ctrl+C to stop"
echo ""

python -m app.main
