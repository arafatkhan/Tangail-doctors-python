#!/bin/bash

###############################################################################
# Quick Re-deployment Script
# Use this to update your site after code changes
###############################################################################

set -e

PROJECT_DIR="/var/www/tangail-doctors"

echo "====================================================================="
echo "  Re-deploying Tangail Doctors"
echo "====================================================================="

cd $PROJECT_DIR

# Activate virtual environment
source venv/bin/activate

# Pull latest changes
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Install/update dependencies
echo "📦 Updating dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running migrations..."
python manage.py migrate --noinput

# Compile translations
echo "🌐 Compiling translations..."
python compile_translations.py 2>/dev/null || echo "⚠️  Translation compilation skipped"

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Deactivate venv
deactivate

# Restart Gunicorn
echo "🔄 Restarting Gunicorn..."
systemctl restart gunicorn

# Check status
echo "✅ Checking service status..."
systemctl status gunicorn --no-pager -l | head -n 20

echo ""
echo "====================================================================="
echo "  ✅ Deployment Complete!"
echo "====================================================================="
echo ""
echo "Visit: https://tangaildoctors.com"
echo ""
