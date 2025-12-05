#!/bin/bash
# Direct build and deployment script for Render
# This ensures migrations and static files are ready

set -e

echo "=== SamaCahier Render Deployment ==="
echo ""

echo "📦 Step 1: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependencies installed"
echo ""

echo "📁 Step 2: Preparing Django application..."
python manage.py collectstatic --noinput --clear

echo "✅ Static files collected"
echo ""

echo "🔄 Step 3: Running database migrations..."
python manage.py migrate --noinput

echo "✅ Migrations applied"
echo ""

echo "🚀 Build complete - Ready for deployment!"
echo "   Server will start with: gunicorn app:app"
