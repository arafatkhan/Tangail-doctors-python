#!/usr/bin/env python
"""
Script to create a superuser for Django admin.
NOTE: This script is for DEVELOPMENT/SETUP ONLY. 
In production, use Django's built-in createsuperuser command or environment variables.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# WARNING: These credentials are for initial setup only. Change them immediately!
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'arafat')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'arafat@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'arafat18843')

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f'✅ User "{username}" already exists')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✅ Superuser "{username}" created successfully')
