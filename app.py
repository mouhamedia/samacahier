"""
app.py - Django WSGI application
This exposes the Django application as 'app' for gunicorn
Render's default command: gunicorn app:app
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
django.setup()

# Import and export Django WSGI application
from django.core.wsgi import get_wsgi_application

# This is what gunicorn will use
app = get_wsgi_application()
