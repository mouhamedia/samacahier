#!/usr/bin/env python
"""
Démarrer le serveur Django sans reloadeur
"""
import os
import sys
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samacahier.settings')
    
    # Démarrer sans reloadeur et sans threading
    sys.argv = ['manage.py', 'runserver', '--noreload', '--nothreading', '127.0.0.1:8000']
    execute_from_command_line(sys.argv)
