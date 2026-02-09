#!/bin/bash

###############################################################################
# Gunicorn Service Setup Script
# Configures Gunicorn as systemd service
# Run this as root user
###############################################################################

set -e

echo "====================================================================="
echo "  Phase 5: Gunicorn Configuration"
echo "====================================================================="

PROJECT_DIR="/var/www/tangail-doctors"

# Create log directory
echo "📁 Creating log directory..."
mkdir -p /var/log/gunicorn
chown -R www-data:www-data /var/log/gunicorn

# Create Gunicorn socket file
echo "🔌 Creating Gunicorn socket..."
cat > /etc/systemd/system/gunicorn.socket <<'EOF'
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

# Create Gunicorn service file
echo "⚙️  Creating Gunicorn service..."
cat > /etc/systemd/system/gunicorn.service <<EOF
[Unit]
Description=gunicorn daemon for Tangail Doctors
Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
EnvironmentFile=$PROJECT_DIR/.env
ExecStart=$PROJECT_DIR/venv/bin/gunicorn \\
          --workers 3 \\
          --timeout 120 \\
          --bind unix:/run/gunicorn.sock \\
          --access-logfile /var/log/gunicorn/access.log \\
          --error-logfile /var/log/gunicorn/error.log \\
          --log-level info \\
          config.wsgi:application

ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload

# Start and enable Gunicorn socket
echo "🚀 Starting Gunicorn socket..."
systemctl start gunicorn.socket
systemctl enable gunicorn.socket

# Check socket status
echo "✅ Gunicorn socket status:"
systemctl status gunicorn.socket --no-pager -l

# Test socket
echo ""
echo "🧪 Testing Gunicorn socket..."
curl --unix-socket /run/gunicorn.sock http || echo "Socket test: waiting for service"

# Start Gunicorn service
echo ""
echo "🚀 Starting Gunicorn service..."
systemctl start gunicorn
systemctl enable gunicorn

# Wait a moment
sleep 2

# Check service status
echo "✅ Gunicorn service status:"
systemctl status gunicorn --no-pager -l

echo ""
echo "====================================================================="
echo "  ✅ Gunicorn Configured!"
echo "====================================================================="
echo ""
echo "Commands to manage Gunicorn:"
echo "  sudo systemctl restart gunicorn"
echo "  sudo systemctl status gunicorn"
echo "  sudo journalctl -u gunicorn -f"
echo ""
echo "Logs location:"
echo "  /var/log/gunicorn/access.log"
echo "  /var/log/gunicorn/error.log"
echo ""
