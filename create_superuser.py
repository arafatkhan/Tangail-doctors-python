#!/usr/bin/env python
"""Script to create a superuser for Django admin"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'arafat'
email = 'arafat@example.com'
password = 'arafat18843'

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f'✅ User "{username}" already exists')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✅ Superuser "{username}" created successfully')
