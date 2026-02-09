#!/bin/bash

###############################################################################
# Django Project Deployment Script
# Deploys Tangail Doctors from GitHub and configures it
# Run this as root user
###############################################################################

set -e

echo "====================================================================="
echo "  Phase 4: Django Project Deployment"
echo "====================================================================="

# Variables
PROJECT_DIR="/var/www/tangail-doctors"
REPO_URL="https://github.com/yourusername/Tangail-doctors-python.git"
DB_PASSWORD=$(grep "Database Password:" /root/database-credentials.txt | cut -d: -f2 | xargs)

# Create project directory
echo "📁 Creating project directory..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Check if .env file exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists. Skipping git clone."
    echo "📥 Pulling latest changes..."
    git pull origin main || echo "⚠️  Git pull failed. Manual sync may be needed."
else
    echo "📥 Cloning project from GitHub..."
    echo ""
    echo "⚠️  If repository is private, you'll need to provide credentials"
    echo "    Or use: git clone https://TOKEN@github.com/user/repo.git"
    echo ""
    read -p "Enter GitHub repository URL (or press Enter for default): " USER_REPO
    
    if [ ! -z "$USER_REPO" ]; then
        REPO_URL=$USER_REPO
    fi
    
    git clone $REPO_URL .
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install production dependencies
echo "📦 Installing production packages..."
pip install gunicorn psycopg2-binary python-decouple whitenoise dj-database-url

# Generate SECRET_KEY
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    
    cat > .env <<EOF
# Django Settings
DEBUG=False
SECRET_KEY=$SECRET_KEY
ALLOWED_HOSTS=217.216.73.118,tangaildoctors.com,www.tangaildoctors.com

# Database Configuration
DATABASE_URL=postgresql://tangail_user:$DB_PASSWORD@localhost:5432/tangail_doctors

# Static and Media Files
STATIC_URL=/static/
MEDIA_URL=/media/
STATIC_ROOT=$PROJECT_DIR/staticfiles
MEDIA_ROOT=$PROJECT_DIR/media

# Language Settings
LANGUAGE_CODE=bn
USE_I18N=True
USE_L10N=True

# Security (Production)
CSRF_TRUSTED_ORIGINS=https://tangaildoctors.com,https://www.tangaildoctors.com
EOF

    echo "✅ .env file created"
else
    echo "⚠️  .env file already exists. Skipping creation."
    echo "    Please verify settings manually."
fi

# Create directories
echo "📁 Creating media and staticfiles directories..."
mkdir -p media staticfiles

# Set permissions
echo "🔐 Setting permissions..."
chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
chmod -R 775 $PROJECT_DIR/media

# Compile translations
echo "🌐 Compiling translations..."
if [ -f "compile_translations.py" ]; then
    python compile_translations.py
else
    echo "⚠️  compile_translations.py not found. Skipping."
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (interactive)
echo ""
echo "👤 Create Django superuser..."
echo "    (You can skip this and create later with: python manage.py createsuperuser)"
read -p "Create superuser now? (y/n): " CREATE_SUPER

if [ "$CREATE_SUPER" = "y" ] || [ "$CREATE_SUPER" = "Y" ]; then
    python manage.py createsuperuser
fi

# Deactivate venv
deactivate

echo ""
echo "====================================================================="
echo "  ✅ Django Project Deployed!"
echo "====================================================================="
echo ""
echo "Project location: $PROJECT_DIR"
echo ".env file: $PROJECT_DIR/.env"
echo ""
echo "Next steps:"
echo "1. Configure Gunicorn (run 04-setup-gunicorn.sh)"
echo "2. Configure Nginx (run 05-setup-nginx.sh)"
echo ""
