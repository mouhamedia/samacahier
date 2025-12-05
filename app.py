"""
app.py - Flask wrapper for Django WSGI application
This allows Render's default 'gunicorn app:app' to work with Django
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
django.setup()

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Create the WSGI application
app = get_wsgi_application()

if __name__ == '__main__':
    app.run()
