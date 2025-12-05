#!/bin/bash
# Build script for Render deployment

set -e

echo "Step 1: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Step 2: Collecting static files..."
python manage.py collectstatic --noinput

echo "Step 3: Running migrations..."
python manage.py migrate

echo "Step 4: Creating superuser if doesn't exist..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Admin user created!")
else:
    print("Admin user already exists!")
END

echo "✅ Build complete!"
