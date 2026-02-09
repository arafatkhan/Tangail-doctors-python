#!/bin/bash

###############################################################################
# Contabo VPS Initial Setup Script
# Tangail Doctors Django Project
# Run this as root user
###############################################################################

set -e  # Exit on error

echo "====================================================================="
echo "  Phase 1: Initial Server Setup & Security"
echo "====================================================================="

# Update system packages
echo "📦 Updating system packages..."
apt update
apt upgrade -y

# Install essential tools
echo "🔧 Installing essential tools..."
apt install -y software-properties-common curl wget vim git ufw build-essential

# Set timezone to Bangladesh
echo "🕐 Setting timezone to Asia/Dhaka..."
timedatectl set-timezone Asia/Dhaka

# Configure firewall
echo "🔥 Configuring firewall (UFW)..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw --force enable

echo "✅ Firewall configured:"
ufw status verbose

# Create swap if not exists
echo "💾 Checking swap memory..."
if [ $(swapon --show | wc -l) -eq 0 ]; then
    echo "Creating 2GB swap file..."
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "✅ Swap created"
else
    echo "✅ Swap already exists"
fi

free -h

echo ""
echo "====================================================================="
echo "  Phase 2: Installing Required Software"
echo "====================================================================="

# Install Python 3.11
echo "🐍 Installing Python 3.11..."
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Set Python 3.11 as default
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

echo "✅ Python version:"
python3 --version

# Install PostgreSQL
echo "🐘 Installing PostgreSQL..."
apt install -y postgresql postgresql-contrib libpq-dev

# Start and enable PostgreSQL
systemctl start postgresql
systemctl enable postgresql

echo "✅ PostgreSQL status:"
systemctl status postgresql --no-pager -l

# Install Nginx
echo "🌐 Installing Nginx..."
apt install -y nginx

# Start and enable Nginx
systemctl start nginx
systemctl enable nginx

echo "✅ Nginx status:"
systemctl status nginx --no-pager -l

# Install additional dependencies
echo "📚 Installing additional dependencies..."
apt install -y libjpeg-dev zlib1g-dev redis-server

# Enable Redis
systemctl enable redis-server

# Install Certbot for SSL
echo "🔒 Installing Certbot for SSL..."
apt install -y certbot python3-certbot-nginx

echo ""
echo "====================================================================="
echo "  ✅ Phase 1 & 2 Complete!"
echo "====================================================================="
echo ""
echo "Next steps:"
echo "1. Create PostgreSQL database (run 02-database-setup.sh)"
echo "2. Create deploy user (optional but recommended)"
echo "3. Upload Django project"
echo ""
echo "Server is ready for Django deployment!"
echo "====================================================================="
