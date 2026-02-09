#!/bin/bash

###############################################################################
# Nginx Configuration Script
# Configures Nginx as reverse proxy for Django
# Run this as root user
###############################################################################

set -e

echo "====================================================================="
echo "  Phase 6: Nginx Configuration"
echo "====================================================================="

PROJECT_DIR="/var/www/tangail-doctors"

# Create Nginx server block
echo "⚙️  Creating Nginx configuration..."
cat > /etc/nginx/sites-available/tangail-doctors <<'EOF'
upstream tangail_doctors {
    server unix:/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    listen [::]:80;
    
    server_name 217.216.73.118 tangaildoctors.com www.tangaildoctors.com;
    
    client_max_body_size 10M;
    
    # Logging
    access_log /var/log/nginx/tangail-doctors-access.log;
    error_log /var/log/nginx/tangail-doctors-error.log;
    
    # Static files
    location /static/ {
        alias /var/www/tangail-doctors/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /var/www/tangail-doctors/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://tangail_doctors;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Favicon
    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }
    
    # Robots.txt
    location = /robots.txt {
        access_log off;
        log_not_found off;
    }
}
EOF

# Enable site
echo "🔗 Enabling Nginx site..."
ln -sf /etc/nginx/sites-available/tangail-doctors /etc/nginx/sites-enabled/

# Remove default site
echo "🗑️  Removing default Nginx site..."
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
nginx -t

# Restart Nginx
echo "🔄 Restarting Nginx..."
systemctl restart nginx

# Check Nginx status
echo "✅ Nginx status:"
systemctl status nginx --no-pager -l

echo ""
echo "====================================================================="
echo "  ✅ Nginx Configured!"
echo "====================================================================="
echo ""
echo "Test your site:"
echo "  http://217.216.73.118"
echo ""
echo "If DNS is configured:"
echo "  http://tangaildoctors.com"
echo ""
echo "Next step: Install SSL certificate (run 06-install-ssl.sh after DNS setup)"
echo ""
