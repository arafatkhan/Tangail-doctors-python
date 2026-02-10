#!/usr/bin/env python
"""
Script to create a superuser for Django admin.
NOTE: This script is for DEVELOPMENT/SETUP ONLY. 
In production, use Django's built-in createsuperuser command or environment variables.

Usage:
    export DJANGO_SUPERUSER_USERNAME=your_username
    export DJANGO_SUPERUSER_EMAIL=your_email@example.com
    export DJANGO_SUPERUSER_PASSWORD=your_secure_password
    python create_superuser.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Get credentials from environment variables
# Use weak defaults only for initial local development setup
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not password:
    print("⚠️  WARNING: No password provided via DJANGO_SUPERUSER_PASSWORD environment variable")
    print("   Using default password for local development only!")
    print("   For production, set DJANGO_SUPERUSER_PASSWORD environment variable")
    password = 'changeme123'  # Weak default for local dev only

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f'✅ User "{username}" already exists')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✅ Superuser "{username}" created successfully')
