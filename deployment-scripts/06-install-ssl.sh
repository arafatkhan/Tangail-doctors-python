#!/bin/bash

###############################################################################
# SSL Certificate Installation Script
# Installs Let's Encrypt SSL certificate
# Run this AFTER DNS is pointing to your VPS
###############################################################################

set -e

echo "====================================================================="
echo "  Phase 7: SSL Certificate Installation"
echo "====================================================================="

echo ""
echo "⚠️  IMPORTANT: Before running this script, make sure:"
echo "    1. DNS is pointing to 217.216.73.118"
echo "    2. Domain is accessible via HTTP"
echo "    3. Cloudflare proxy is DISABLED (gray cloud, not orange)"
echo ""

read -p "DNS configured and ready? (y/n): " DNS_READY

if [ "$DNS_READY" != "y" ] && [ "$DNS_READY" != "Y" ]; then
    echo "❌ Exiting. Configure DNS first, then run this script."
    exit 1
fi

# Test domain accessibility
echo "🧪 Testing domain accessibility..."
if curl -Is http://tangaildoctors.com | head -n 1 | grep "HTTP" > /dev/null; then
    echo "✅ Domain is accessible"
else
    echo "❌ Domain is not accessible. Check DNS and Nginx configuration."
    exit 1
fi

# Get email for certificate
read -p "Enter email for SSL certificate notifications: " EMAIL

if [ -z "$EMAIL" ]; then
    echo "❌ Email is required for Let's Encrypt"
    exit 1
fi

# Install SSL certificate
echo "🔒 Installing SSL certificate..."
certbot --nginx \
    -d tangaildoctors.com \
    -d www.tangaildoctors.com \
    --non-interactive \
    --agree-tos \
    --email $EMAIL \
    --redirect

echo ""
echo "✅ SSL certificate installed!"

# Test auto-renewal
echo "🧪 Testing SSL auto-renewal..."
certbot renew --dry-run

# Check certbot timer
echo "⏰ Certbot auto-renewal timer status:"
systemctl status certbot.timer --no-pager -l

echo ""
echo "====================================================================="
echo "  ✅ SSL Certificate Installed Successfully!"
echo "====================================================================="
echo ""
echo "Your website is now secure:"
echo "  https://tangaildoctors.com"
echo "  https://www.tangaildoctors.com"
echo ""
echo "Certificate details:"
certbot certificates
echo ""
echo "Next steps:"
echo "1. Enable Cloudflare proxy (orange cloud) for extra security"
echo "2. Set Cloudflare SSL/TLS to 'Full (strict)'"
echo "3. Test all website features"
echo ""
