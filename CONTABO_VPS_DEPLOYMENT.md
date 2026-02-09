# 🚀 Contabo VPS Deployment Guide - Tangail Doctors Django Project

**Complete Production Deployment on Contabo Cloud VPS**

---

## ⚡ QUICK MIGRATION SUMMARY (Your Specific Case)

**You are migrating from:**
- 🌐 Old Website: HTML/CSS/JavaScript on Namecheap hosting
- 📍 Domain: tangaildoctors.com (Namecheap registration)
- 🔧 DNS: Cloudflare (dahlia.ns.cloudflare.com, ezra.ns.cloudflare.com)

**Migrating to:**
- 🐍 New Website: Django Python application
- 🖥️ Server: Contabo VPS 20 NVMe @ Singapore
- 📡 IP: 217.216.73.118

**Migration Process (13 Phases):**

1. ✅ **Phase 1-6:** Setup VPS, Install software, Deploy Django → Test on IP
2. 🔄 **Phase 7:** **CRITICAL** - Switch DNS from old hosting to new VPS
3. 🔒 **Phase 8:** Install SSL, Enable HTTPS
4. ✨ **Phase 9-13:** Optimization, Security, Monitoring

**Downtime:** ~5-30 minutes (DNS propagation)

**Timeline:**
- Setup VPS: 2-3 hours
- Deploy Django: 1-2 hours
- DNS Switch: 5-30 minutes
- Testing & SSL: 30 minutes
- **Total:** ~4-6 hours

**Safety Net:** Keep old Namecheap hosting for 2-4 weeks (rollback option)

---

## 🎯 Critical Decision Points

Before starting, understand:

1. **DNS Switch = Your Website Changes**
   - Old HTML site → Django app
   - Happens in Phase 7
   - Instant for most users (5-30 min propagation)

2. **Old Hosting**
   - Keep active for 2-4 weeks as backup
   - Can rollback if needed
   - Cancel after new site stable

3. **Email (if using domain email)**
   - If you use yourname@tangaildoctors.com
   - Email hosting might be on Namecheap
   - Don't cancel email hosting! Only web hosting

4. **Domain Registration**
   - Keep domain at Namecheap (expires Sept 2026)
   - Must renew before expiration
   - Never cancel domain registration!

---

## � Migration Flow Diagram

```
BEFORE MIGRATION:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  User Browser                                                   │
│       │                                                         │
│       ├─→ tangaildoctors.com                                    │
│       │                                                         │
│       ▼                                                         │
│  Cloudflare DNS                                                 │
│       │                                                         │
│       ├─→ Points to: 198.xx.xx.xx (Namecheap Hosting)         │
│       │                                                         │
│       ▼                                                         │
│  Old HTML/CSS/JS Website @ Namecheap                           │
│  ✓ Currently Live                                              │
│  ✓ Serving Traffic                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                            ↓ MIGRATION ↓

DURING SETUP (Phases 1-6):
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  User Browser                                                   │
│       │                                                         │
│       ├─→ tangaildoctors.com → Still goes to OLD site          │
│       │                                                         │
│       ├─→ 217.216.73.118 → Can test NEW site                  │
│       │                                                         │
│       ▼                                                         │
│  ┌──────────────────────┐    ┌──────────────────────┐         │
│  │ Namecheap Hosting    │    │ Contabo VPS          │         │
│  │ (Old HTML Site)      │    │ (New Django App)     │         │
│  │ Still serving traffic│    │ Being built & tested │         │
│  │ via domain           │    │ Accessible via IP    │         │
│  └──────────────────────┘    └──────────────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                         ↓ DNS SWITCH (Phase 7) ↓

AFTER MIGRATION:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  User Browser                                                   │
│       │                                                         │
│       ├─→ tangaildoctors.com                                    │
│       │                                                         │
│       ▼                                                         │
│  Cloudflare DNS                                                 │
│       │                                                         │
│       ├─→ Points to: 217.216.73.118 (Contabo VPS) ✓           │
│       │                                                         │
│       ▼                                                         │
│  New Django Website @ Contabo                                  │
│  ✓ Live & Serving Traffic                                      │
│  ✓ HTTPS Enabled                                               │
│  ✓ Bangla/English Support                                      │
│                                                                 │
│  ┌──────────────────────┐                                      │
│  │ Namecheap Hosting    │                                      │
│  │ (Old site)           │                                      │
│  │ Still active but     │                                      │
│  │ NOT receiving traffic│                                      │
│  │ (Safety backup)      │                                      │
│  └──────────────────────┘                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                    ↓ AFTER 2-4 WEEKS (Stable) ↓

FINAL STATE:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  User Browser                                                   │
│       │                                                         │
│       ├─→ https://tangaildoctors.com                           │
│       │                                                         │
│       ▼                                                         │
│  Cloudflare DNS + CDN Proxy (Orange Cloud)                     │
│       │                                                         │
│       ├─→ 217.216.73.118 (Contabo VPS)                         │
│       │                                                         │
│       ▼                                                         │
│  Django App (Optimized & Secured)                              │
│  ✓ HTTPS/SSL                                                   │
│  ✓ CDN Cached                                                  │
│  ✓ Firewall Protected                                          │
│  ✓ Daily Backups                                               │
│  ✓ Monitoring Active                                           │
│                                                                 │
│  Namecheap:                                                    │
│  ✓ Domain Registration (Keep & Renew)                          │
│  ✗ Web Hosting (Cancelled - Not Needed)                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

| Detail | Value |
|--------|-------|
| **Server IP** | `217.216.73.118` |
| **Default User** | `root` |
| **Host System** | 20140 |
| **Server Type** | Cloud VPS 20 NVMe |
| **Location** | Singapore 2 (SIN) |
| **OS** | Ubuntu 22.04 LTS (assumed) |

## 🌐 Domain Information

| Detail | Value |
|--------|-------|
| **Domain** | `tangaildoctors.com` |
| **Registrar** | Namecheap |
| **DNS Provider** | Cloudflare |
| **Nameservers** | dahlia.ns.cloudflare.com, ezra.ns.cloudflare.com |
| **Creation Date** | 03/09/2021 |
| **Expiration Date** | 03/09/2026 |
| **Current Hosting** | HTML/CSS/JavaScript (to be replaced) |

---

## 🎯 Deployment Architecture

```
Internet → Domain → Nginx (Port 80/443) → Gunicorn (Port 8000) → Django Application
                                        ↓
                                   PostgreSQL Database
                                        ↓
                                   Static Files (Nginx)
                                        ↓
                                   Media Files (Nginx)
```

---

## 📦 Technology Stack

- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Framework**: Django 4.2
- **Database**: PostgreSQL 14
- **Python**: 3.11
- **SSL**: Let's Encrypt (Certbot)
- **Process Manager**: Systemd
- **Languages**: Bangla (bn) + English (en)

---

# PHASE 1: Initial Server Setup & Security

## Step 1.1: Connect to VPS via SSH

### Windows (PowerShell/CMD):
```powershell
ssh root@217.216.73.118
```

### Enter password when prompted
(Password should be provided by Contabo in your email)

---

## Step 1.2: Update System Packages

```bash
# Update package list
apt update

# Upgrade all packages
apt upgrade -y

# Install essential tools
apt install -y software-properties-common curl wget vim git ufw
```

---

## Step 1.3: Create Sudo User (Security Best Practice)

```bash
# Create new user (replace 'deploy' with your preferred username)
adduser deploy

# Add to sudo group
usermod -aG sudo deploy

# Test sudo access
su - deploy
sudo whoami  # Should output: root
exit
```

---

## Step 1.4: Setup SSH Key Authentication (Recommended)

### On your local Windows machine:

```powershell
# Generate SSH key (if not already exists)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy public key content
Get-Content $env:USERPROFILE\.ssh\id_rsa.pub | clip
```

### Back on VPS (as deploy user):

```bash
su - deploy

# Create SSH directory
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add your public key
nano ~/.ssh/authorized_keys
# Paste the copied public key, save (Ctrl+X, Y, Enter)

chmod 600 ~/.ssh/authorized_keys
exit
```

### Test SSH key login from Windows:
```powershell
ssh deploy@217.216.73.118
```

---

## Step 1.5: Configure Firewall (UFW)

```bash
# Allow SSH (IMPORTANT: Do this BEFORE enabling firewall!)
sudo ufw allow OpenSSH
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow PostgreSQL (only from localhost)
sudo ufw allow from 127.0.0.1 to any port 5432

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status verbose
```

---

## Step 1.6: Configure Timezone

```bash
# Set timezone to Bangladesh
sudo timedatectl set-timezone Asia/Dhaka

# Verify
timedatectl
```

---

## Step 1.7: Setup Swap Memory (if not present)

```bash
# Check current swap
sudo swapon --show

# Create 2GB swap file (adjust based on VPS RAM)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make swap permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Verify
free -h
```

---

# PHASE 2: Install Required Software

## Step 2.1: Install Python 3.11

```bash
# Add deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.11 and dependencies
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Set Python 3.11 as default
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Verify
python3 --version  # Should show: Python 3.11.x
```

---

## Step 2.2: Install PostgreSQL

```bash
# Install PostgreSQL 14
sudo apt install -y postgresql postgresql-contrib

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Check status
sudo systemctl status postgresql
```

---

## Step 2.3: Install Nginx

```bash
# Install Nginx
sudo apt install -y nginx

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx

# Test (should see Nginx welcome page)
curl http://217.216.73.118
```

---

## Step 2.4: Install Additional Dependencies

```bash
# Install build tools
sudo apt install -y build-essential libpq-dev python3-dev

# Install image processing libraries (for Pillow)
sudo apt install -y libjpeg-dev zlib1g-dev

# Install Redis (optional, for caching)
sudo apt install -y redis-server
sudo systemctl enable redis-server
```

---

# PHASE 3: PostgreSQL Database Setup

## Step 3.1: Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# Inside PostgreSQL shell, run:
```

```sql
-- Create database
CREATE DATABASE tangail_doctors;

-- Create user with strong password
CREATE USER tangail_user WITH PASSWORD 'YourStrongPassword123!';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE tangail_doctors TO tangail_user;

-- Grant additional privileges (PostgreSQL 15+)
\c tangail_doctors
GRANT ALL ON SCHEMA public TO tangail_user;

-- Exit
\q
```

---

## Step 3.2: Configure PostgreSQL for Django

```bash
# Edit PostgreSQL configuration
sudo nano /etc/postgresql/14/main/postgresql.conf

# Find and modify:
# listen_addresses = 'localhost'  # Already correct
# max_connections = 100           # Keep default

# Save and exit (Ctrl+X, Y, Enter)

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

## Step 3.3: Test Database Connection

```bash
# Test connection
psql -U tangail_user -d tangail_doctors -h localhost

# If successful, you'll see:
# tangail_doctors=>

# Exit
\q
```

---

# PHASE 4: Project Deployment

## Step 4.1: Create Project Directory

```bash
# Create application directory
sudo mkdir -p /var/www/tangail-doctors
sudo chown -R deploy:deploy /var/www/tangail-doctors

# Navigate to directory
cd /var/www/tangail-doctors
```

---

## Step 4.2: Clone Project from GitHub

```bash
# Clone repository
git clone https://github.com/yourusername/Tangail-doctors-python.git .

# If private repository, setup SSH key or use HTTPS with token
# For HTTPS with token:
# git clone https://<token>@github.com/yourusername/Tangail-doctors-python.git .

# Check files
ls -la
```

**Alternative: Upload via SCP from Windows:**

```powershell
# From your Windows machine
scp -r "D:\My work\htdocs\tangail-doctors-python" deploy@217.216.73.118:/var/www/tangail-doctors/
```

---

## Step 4.3: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

---

## Step 4.4: Install Python Dependencies

```bash
# Install requirements
pip install -r requirements.txt

# Install production dependencies
pip install gunicorn psycopg2-binary python-decouple whitenoise
```

---

## Step 4.5: Create Production .env File

```bash
# Create .env file
nano .env
```

Add this content:

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this-to-random-string
ALLOWED_HOSTS=217.216.73.118,tangaildoctors.com,www.tangaildoctors.com

# Database Configuration
DATABASE_URL=postgresql://tangail_user:YourStrongPassword123!@localhost:5432/tangail_doctors

# Static and Media Files
STATIC_URL=/static/
MEDIA_URL=/media/
STATIC_ROOT=/var/www/tangail-doctors/staticfiles
MEDIA_ROOT=/var/www/tangail-doctors/media

# Language Settings
LANGUAGE_CODE=bn
USE_I18N=True
USE_L10N=True

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Generate SECRET_KEY:
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## Step 4.6: Update Django Settings for Production

```bash
nano config/settings.py
```

Add at the top (after imports):

```python
from decouple import config, Csv
import dj_database_url
import os

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(BASE_DIR, 'staticfiles'))
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'doctors', 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'))

# WhiteNoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Production Security Settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

---

## Step 4.7: Compile Translations

```bash
# Compile translation files
python compile_translations.py

# Or if you have gettext:
# python manage.py compilemessages
```

---

## Step 4.8: Run Migrations

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Username: admin
# Email: your-email@example.com
# Password: (enter secure password)

# Collect static files
python manage.py collectstatic --noinput
```

---

## Step 4.9: Test Django Application

```bash
# Test with development server (temporary)
python manage.py runserver 0.0.0.0:8000

# From your Windows machine, test:
# http://217.216.73.118:8000

# Stop with Ctrl+C
```

---

# PHASE 5: Gunicorn Setup

## Step 5.1: Test Gunicorn

```bash
# Test Gunicorn
gunicorn --bind 0.0.0.0:8000 config.wsgi:application

# Test from browser: http://217.216.73.118:8000
# Stop with Ctrl+C
```

---

## Step 5.2: Create Gunicorn Socket File

```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Add:

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

---

## Step 5.3: Create Gunicorn Service File

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:

```ini
[Unit]
Description=gunicorn daemon for Tangail Doctors
Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
User=deploy
Group=www-data
WorkingDirectory=/var/www/tangail-doctors
Environment="PATH=/var/www/tangail-doctors/venv/bin"
EnvironmentFile=/var/www/tangail-doctors/.env
ExecStart=/var/www/tangail-doctors/venv/bin/gunicorn \
          --workers 3 \
          --timeout 120 \
          --bind unix:/run/gunicorn.sock \
          --access-logfile /var/log/gunicorn/access.log \
          --error-logfile /var/log/gunicorn/error.log \
          --log-level info \
          config.wsgi:application

ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

## Step 5.4: Create Log Directory

```bash
# Create log directory
sudo mkdir -p /var/log/gunicorn
sudo chown -R deploy:www-data /var/log/gunicorn
```

---

## Step 5.5: Start Gunicorn

```bash
# Start and enable Gunicorn socket
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

# Check socket status
sudo systemctl status gunicorn.socket

# Test socket
curl --unix-socket /run/gunicorn.sock http

# Start Gunicorn service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Check status
sudo systemctl status gunicorn

# Check logs if error
sudo journalctl -u gunicorn
```

---

# PHASE 6: Nginx Configuration

## Step 6.1: Create Nginx Server Block

```bash
sudo nano /etc/nginx/sites-available/tangail-doctors
```

Add this configuration:

```nginx
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
```

---

## Step 6.2: Enable Nginx Configuration

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/tangail-doctors /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# If successful, restart Nginx
sudo systemctl restart nginx

# Check status
sudo systemctl status nginx
```

---

## Step 6.3: Set Proper Permissions

```bash
# Set ownership
sudo chown -R deploy:www-data /var/www/tangail-doctors

# Set directory permissions
sudo find /var/www/tangail-doctors -type d -exec chmod 755 {} \;

# Set file permissions
sudo find /var/www/tangail-doctors -type f -exec chmod 644 {} \;

# Make manage.py executable
sudo chmod +x /var/www/tangail-doctors/manage.py

# Set media directory permissions (writable by www-data)
sudo chmod -R 775 /var/www/tangail-doctors/media
sudo chown -R deploy:www-data /var/www/tangail-doctors/media
```

---

# PHASE 7: Migrate from Old Website & DNS Configuration

## Step 7.0: Pre-Migration Strategy

**Your Current Setup:**
- Old Website: HTML/CSS/JavaScript on Namecheap hosting
- Domain: tangaildoctors.com (registered on Namecheap)
- DNS: Managed by Cloudflare
- New Setup: Django app on Contabo VPS (217.216.73.118)

**Migration Strategy Options:**

### Option A: Direct Switch (Recommended - Clean Cut)
1. Backup old website
2. Point DNS to new VPS
3. Old site goes offline, new site goes live
4. **Downtime:** 5-30 minutes (DNS propagation)

### Option B: Gradual Migration (Zero Downtime)
1. Keep old hosting active
2. Test new site on IP (http://217.216.73.118)
3. When ready, switch DNS
4. Monitor for 24 hours
5. Cancel old hosting

**We'll use Option A (faster, simpler).**

---

## Step 7.1: Backup Old Website

**IMPORTANT:** Backup your current website before DNS switch!

### Method 1: Download via FTP/cPanel

If you have FTP access to your Namecheap hosting:

**Windows (FileZilla):**
1. Download FileZilla: https://filezilla-project.org/
2. Connect to your Namecheap hosting
   - Host: ftp.yourhostingserver.com (check Namecheap email)
   - Username: your-ftp-username
   - Password: your-ftp-password
3. Download entire `public_html` or `www` folder to your computer

**Backup Location:**
```
D:\Backups\tangaildoctors-old-site\
```

### Method 2: Download via Browser (before DNS switch)

```powershell
# From Windows PowerShell
cd "D:\Backups\"
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://tangaildoctors.com -P tangaildoctors-old-site
```

### Method 3: Keep Hosting Active (Safest)

Don't cancel Namecheap hosting for 1-2 weeks. This way:
- If something goes wrong, you can revert DNS
- You have time to test new site
- Old site remains accessible via hosting control panel

---

## Step 7.2: Test New Site on IP Address

Before DNS switch, test your new Django site:

```bash
# Make sure services are running on VPS
sudo systemctl status gunicorn nginx

# Test from your Windows machine
curl -I http://217.216.73.118
```

**Test in Browser:**
1. Open: http://217.216.73.118
2. Check all pages work
3. Test language switching
4. Verify doctor listings
5. Test admin panel: http://217.216.73.118/admin/

**If everything works, proceed to DNS switch.**

---

## Step 7.2: Configure Cloudflare DNS (CRITICAL STEP)

**This is the main step that switches your website from old hosting to new VPS.**

### Access Cloudflare Dashboard:

1. **Login to Cloudflare:** https://dash.cloudflare.com/login
2. **Select Domain:** Click on `tangaildoctors.com`
3. **Go to DNS Settings:** Click "DNS" in the left sidebar

---

### Current DNS Records (Before Change):

Your current DNS probably points to Namecheap hosting. You'll see something like:

| Type | Name | Content | Proxy | TTL |
|------|------|---------|-------|-----|
| A | @ | 198.xx.xx.xx (old hosting IP) | Proxied | Auto |
| CNAME | www | tangaildoctors.com | Proxied | Auto |

---

### Update DNS Records (New Configuration):

**Step-by-step changes:**

#### 1. Update Root Domain (@):

- **Find:** A record with Name = `@` or `tangaildoctors.com`
- **Click:** "Edit" button
- **Change:**
  - Type: `A` (keep same)
  - Name: `@` (keep same)
  - IPv4 address: `217.216.73.118` ⬅️ **CHANGE THIS**
  - Proxy status: Click cloud icon to make it **DNS only** (gray cloud) ⬅️ **IMPORTANT**
  - TTL: `Auto` (keep same)
- **Click:** "Save"

#### 2. Update WWW Subdomain:

**Option A:** If you have `CNAME` record for `www`:
- **Find:** CNAME record with Name = `www`
- **Delete it** (click Delete)

**Option B:** Create new A record for `www`:
- **Click:** "+ Add record"
- Type: `A`
- Name: `www`
- IPv4 address: `217.216.73.118`
- Proxy status: **DNS only** (gray cloud) ⬅️ **CRITICAL**
- TTL: `Auto`
- **Click:** "Save"

---

### Final DNS Configuration Should Look Like:

```
┌──────┬──────┬─────────────────┬──────────────┬──────┐
│ Type │ Name │ Content         │ Proxy Status │ TTL  │
├──────┼──────┼─────────────────┼──────────────┼──────┤
│ A    │ @    │ 217.216.73.118  │ DNS only     │ Auto │
│ A    │ www  │ 217.216.73.118  │ DNS only     │ Auto │
└──────┴──────┴─────────────────┴──────────────┴──────┘
```

**⚠️ IMPORTANT NOTES:**

1. **Proxy Status = "DNS only" (Gray Cloud)** initially
   - This is REQUIRED for Let's Encrypt SSL certificate
   - After SSL works, you can enable "Proxied" (Orange Cloud)

2. **Delete old DNS records:**
   - Remove any old A records pointing to Namecheap hosting
   - Remove conflicting CNAME records
   - Keep only the 2 records shown above

3. **Don't touch other records:**
   - Leave MX records (email) as they are
   - Leave TXT records (verification) as they are

---

### Verify DNS Propagation:

**From Windows PowerShell:**

```powershell
# Check root domain
nslookup tangaildoctors.com

# Should show:
# Name:    tangaildoctors.com
# Address:  217.216.73.118

# Check www subdomain
nslookup www.tangaildoctors.com

# Should also show:
# Address:  217.216.73.118
```

**Online DNS Checker:**
- Visit: https://dnschecker.org/
- Enter: `tangaildoctors.com`
- Check if all locations show: `217.216.73.118`

**Propagation Time:**
- **With Cloudflare:** Usually 2-5 minutes ⚡ (very fast!)
- **Maximum:** Up to 24 hours (rare)
- **Typical:** 10-30 minutes

**While waiting, test direct IP:**
```powershell
curl http://217.216.73.118
# Should show your new Django site
```

---

### ⏱️ IMMEDIATELY AFTER DNS SWITCH - Quick Actions

**Within first 5 minutes:**

```powershell
# 1. Clear your local DNS cache
ipconfig /flushdns

# 2. Check DNS resolution
nslookup tangaildoctors.com
# Should show: 217.216.73.118

# 3. Test in browser (use Incognito/Private mode)
# - https://tangaildoctors.com
# - https://www.tangaildoctors.com
```

**Expected Results:**
- ✅ HTTP works (shows Django site)
- ⚠️ HTTPS will show warning (certificate not installed yet)
- ✅ Your new Django site loads
- ❌ Old HTML site no longer accessible via domain

**If you see old site:**
- Browser cache: Clear cache & cookies
- DNS cache: `ipconfig /flushdns`
- Wait 5-10 more minutes
- Try incognito browser window
- Check different device (mobile phone)

**Proceed to Step 7.3 for SSL certificate installation.**

---

**In Cloudflare Dashboard:**

1. Go to **SSL/TLS** section
2. Set SSL/TLS encryption mode to: **Full** (not Full Strict yet)
3. Enable **Always Use HTTPS**: ON
4. Enable **Automatic HTTPS Rewrites**: ON
5. Minimum TLS Version: 1.2

---

## Step 7.4: Install Certbot

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx
```

---

## Step 7.5: Obtain SSL Certificate

**IMPORTANT:** Before running this, verify:
1. DNS is pointing to 217.216.73.118 (check: `nslookup tangaildoctors.com`)
2. Nginx is running and accessible via HTTP
3. Cloudflare proxy is **disabled** (gray cloud)

```bash
# Test if domain is accessible
curl -I http://tangaildoctors.com

# Get certificate for your domain
sudo certbot --nginx -d tangaildoctors.com -d www.tangaildoctors.com

# Follow prompts:
# - Enter email: your-email@example.com
# - Agree to terms: Yes
# - Share email with EFF: Your choice
# - Redirect HTTP to HTTPS: Yes (recommended)
```

**If you get an error:**
- Make sure Nginx config has `server_name tangaildoctors.com www.tangaildoctors.com;`
- Ensure port 80 and 443 are open in firewall
- Verify Cloudflare proxy is disabled temporarily

---

## Step 7.6: Test Auto-Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot will auto-renew via systemd timer
sudo systemctl status certbot.timer
```

---

## Step 7.8: What Happens to Old Website?

### Immediately After DNS Switch:

**Old Namecheap Hosting:**
- ✅ Still active and running
- ❌ No longer receiving traffic (DNS points to VPS now)
- 💰 Still being charged (if active subscription)
- 📁 Old files still exist there

**New Contabo VPS:**
- ✅ Receiving all traffic via tangaildoctors.com
- ✅ Serving Django application
- ✅ New database (PostgreSQL)

---

### Recommended Timeline:

**Week 1 (Testing Period):**
- ✅ Keep both hosting active
- 🔍 Monitor new site for issues
- 🐛 Fix any bugs that appear
- 📊 Check analytics and traffic
- **Action:** Keep paying for Namecheap hosting

**Week 2-3 (Stability Check):**
- ✅ New site running smoothly
- ✅ All features working
- ✅ No major issues
- 📧 Email still working (if using domain email)
- **Action:** Still keep Namecheap hosting as backup

**Week 4+ (Migration Complete):**
- ✅ Confident new site is stable
- ✅ Backups configured on VPS
- ✅ All data migrated successfully
- ✅ Users happy with new site
- **Action:** Safe to cancel Namecheap hosting

---

### How to Cancel Namecheap Hosting:

**Before canceling, make sure:**
1. ✅ Downloaded backup of old website files
2. ✅ Exported any old databases (if any)
3. ✅ Saved old hosting credentials (for records)
4. ✅ Email forwarding configured (if using domain email)
5. ✅ New site has been stable for 2+ weeks

**Cancellation Steps:**
1. Login to Namecheap account
2. Go to "Hosting List" or "Products"
3. Find your hosting package
4. Click "Manage" → "Cancel Hosting"
5. **Important:** Domain registration is separate! Don't cancel domain!
6. Keep domain active and renew in September 2026

**What to Keep at Namecheap:**
- ✅ **Domain Registration** (tangaildoctors.com)
- ❌ **Web Hosting** (not needed, using Contabo now)
- ✅ **Email Hosting** (if using Namecheap email)

**Note:** Domain and hosting are separate services. You can:
- Keep domain at Namecheap (just keep renewing it)
- Cancel hosting service (since using Contabo now)
- DNS managed by Cloudflare (already configured)

---

### Rollback Plan (In Case of Emergency):

**If new site has critical issues:**

1. **Quick Rollback (10 minutes):**
   ```
   - Go to Cloudflare DNS
   - Change A records back to old Namecheap IP
   - Wait 5-10 minutes
   - Old site is back online
   ```

2. **Find Old Namecheap IP:**
   - Check Namecheap hosting control panel
   - Or check your backup/notes
   - Usually something like: 198.xx.xx.xx

3. **Keep This Info Handy:**
   - Old hosting IP address
   - Old hosting login credentials
   - DNS records before change (screenshot)

**This is why we keep old hosting for 2-4 weeks!**

---

**After SSL is working:**

1. Go back to Cloudflare Dashboard → DNS
2. Click on the cloud icon next to your A records
3. Change from "DNS only" (gray) to "Proxied" (orange)
4. This enables:
   - DDoS protection
   - CDN (faster loading worldwide)
   - Web Application Firewall (WAF)
   - Analytics

**Update Cloudflare SSL/TLS to "Full (Strict)":**
1. SSL/TLS → Overview
2. Change to: **Full (strict)**
3. This ensures end-to-end encryption

**Configure Cloudflare Page Rules (Optional):**
- Redirect www to non-www (or vice versa)
- Enable caching rules
- Set security levels

---

# PHASE 8: Final Domain Configuration

## Step 8.1: Verify Domain Configuration

Your domain is already using Cloudflare DNS (configured in Phase 7), verify:

```bash
# Check DNS resolution
dig tangaildoctors.com
dig www.tangaildoctors.com

# Test website access
curl -I https://tangaildoctors.com
curl -I https://www.tangaildoctors.com
```

Both should return 200 OK and redirect to HTTPS.

---

## Step 8.2: Update Django Settings

```bash
nano .env
```

Update ALLOWED_HOSTS:
```env
ALLOWED_HOSTS=217.216.73.118,tangaildoctors.com,www.tangaildoctors.com
```

**For Cloudflare Proxy (if enabled):**
Add Cloudflare IPs to trusted origins in `config/settings.py`:

```python
# Add this to settings.py
CSRF_TRUSTED_ORIGINS = [
    'https://tangaildoctors.com',
    'https://www.tangaildoctors.com',
]

# Get real IP behind Cloudflare proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

Restart Gunicorn:
```bash
sudo systemctl restart gunicorn
```

---

## Step 8.3: Test Everything

```bash
# Test HTTP (should redirect to HTTPS)
curl -I http://tangaildoctors.com

# Test HTTPS
curl -I https://tangaildoctors.com

# Test www subdomain
curl -I https://www.tangaildoctors.com

# Test admin panel
curl -I https://tangaildoctors.com/admin/
```

All should return 200 OK or 301/302 redirects.

---

# PHASE 9: Deployment Automation

## Step 9.1: Create Deployment Script

```bash
nano /var/www/tangail-doctors/deploy.sh
```

Add:

```bash
#!/bin/bash

# Tangail Doctors Deployment Script

set -e

echo "🚀 Starting deployment..."

# Navigate to project directory
cd /var/www/tangail-doctors

# Activate virtual environment
source venv/bin/activate

# Pull latest changes
echo "📥 Pulling latest code..."
git pull origin main

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running migrations..."
python manage.py migrate --noinput

# Compile translations
echo "🌐 Compiling translations..."
python compile_translations.py

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Restart Gunicorn
echo "🔄 Restarting application..."
sudo systemctl restart gunicorn

# Check status
echo "✅ Checking service status..."
sudo systemctl status gunicorn --no-pager

echo "✅ Deployment complete!"
echo "🌐 Visit: https://tangaildoctors.com"
```

Make executable:
```bash
chmod +x /var/www/tangail-doctors/deploy.sh
```

---

## Step 9.2: Run Deployment

```bash
./deploy.sh
```

---

# PHASE 10: Import Existing Data

## Step 10.1: Transfer SQLite Data to PostgreSQL

### Option 1: Via Django Dumpdata/Loaddata

**On your local Windows machine:**

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Export data
python manage.py dumpdata doctors --indent 2 > doctors_data.json

# Upload to VPS
scp doctors_data.json deploy@217.216.73.118:/var/www/tangail-doctors/
```

**On VPS:**

```bash
cd /var/www/tangail-doctors
source venv/bin/activate

# Load data
python manage.py loaddata doctors_data.json
```

---

### Option 2: Direct Database Import

**On Windows:**

```powershell
# Copy db.sqlite3 to VPS
scp "D:\My work\htdocs\tangail-doctors-python\db.sqlite3" deploy@217.216.73.118:/tmp/
```

**On VPS:**

```bash
# Install sqlite3
sudo apt install -y sqlite3

# Export to SQL
sqlite3 /tmp/db.sqlite3 .dump > /tmp/data.sql

# Import to PostgreSQL (carefully!)
# First, create backup
sudo -u postgres pg_dump tangail_doctors > /tmp/backup.sql

# Then import (may need manual adjustment)
# psql -U tangail_user -d tangail_doctors -h localhost < /tmp/data.sql
```

---

## Step 10.2: Transfer Media Files

```powershell
# From Windows
scp -r "D:\My work\htdocs\tangail-doctors-python\media" deploy@217.216.73.118:/var/www/tangail-doctors/
```

Set permissions:
```bash
sudo chown -R deploy:www-data /var/www/tangail-doctors/media
sudo chmod -R 775 /var/www/tangail-doctors/media
```

---

# PHASE 11: Monitoring & Maintenance

## Step 11.1: Setup Logging

```bash
# View Gunicorn logs
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/gunicorn/access.log

# View Nginx logs
sudo tail -f /var/log/nginx/tangail-doctors-error.log
sudo tail -f /var/log/nginx/tangail-doctors-access.log

# View systemd logs
sudo journalctl -u gunicorn -f
sudo journalctl -u nginx -f
```

---

## Step 11.2: Create Backup Script

```bash
sudo nano /usr/local/bin/backup-tangail.sh
```

Add:

```bash
#!/bin/bash

# Backup script for Tangail Doctors

BACKUP_DIR="/var/backups/tangail-doctors"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
sudo -u postgres pg_dump tangail_doctors > $BACKUP_DIR/db_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/tangail-doctors/media

# Backup code (optional)
tar -czf $BACKUP_DIR/code_$DATE.tar.gz /var/www/tangail-doctors --exclude='venv' --exclude='media'

# Remove backups older than 7 days
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
```

Make executable:
```bash
sudo chmod +x /usr/local/bin/backup-tangail.sh
```

Setup cron job (daily at 2 AM):
```bash
sudo crontab -e

# Add this line:
0 2 * * * /usr/local/bin/backup-tangail.sh >> /var/log/backup.log 2>&1
```

---

## Step 11.3: Monitor System Resources

```bash
# Install htop
sudo apt install -y htop

# Monitor resources
htop

# Check disk usage
df -h

# Check memory
free -h

# Check PostgreSQL connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"
```

---

# PHASE 12: Performance Optimization

## Step 12.1: Enable Gzip Compression

```bash
sudo nano /etc/nginx/nginx.conf
```

Add inside `http` block:

```nginx
# Gzip compression
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/rss+xml font/truetype font/opentype application/vnd.ms-fontobject image/svg+xml;
```

Restart Nginx:
```bash
sudo systemctl restart nginx
```

---

## Step 12.2: Setup Redis Caching (Optional)

```bash
# Install Redis
sudo apt install -y redis-server

# Install Python Redis
source /var/www/tangail-doctors/venv/bin/activate
pip install django-redis
```

Update `config/settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session engine
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

---

## Step 12.3: Database Optimization

```bash
sudo -u postgres psql tangail_doctors
```

```sql
-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_doctor_name ON doctors_doctor(name);
CREATE INDEX IF NOT EXISTS idx_doctor_specialty ON doctors_doctor(specialty);
CREATE INDEX IF NOT EXISTS idx_doctor_emergency ON doctors_doctor(is_emergency);
CREATE INDEX IF NOT EXISTS idx_category_name ON doctors_category(name);

-- Analyze tables
ANALYZE doctors_doctor;
ANALYZE doctors_category;

\q
```

---

# PHASE 13: Security Hardening

## Step 13.1: Disable Root SSH Login

```bash
sudo nano /etc/ssh/sshd_config
```

Find and change:
```
PermitRootLogin no
PasswordAuthentication no  # If using SSH keys
```

Restart SSH:
```bash
sudo systemctl restart sshd
```

---

## Step 13.2: Install Fail2Ban

```bash
# Install Fail2Ban
sudo apt install -y fail2ban

# Configure
sudo nano /etc/fail2ban/jail.local
```

Add:

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = 22

[nginx-http-auth]
enabled = true

[nginx-noscript]
enabled = true

[nginx-botsearch]
enabled = true
```

Start Fail2Ban:
```bash
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
sudo fail2ban-client status
```

---

## Step 13.3: Configure PostgreSQL Password Policy

```bash
sudo -u postgres psql
```

```sql
-- Enforce password expiration (optional)
ALTER ROLE tangail_user VALID UNTIL 'infinity';

-- Limit connections
ALTER ROLE tangail_user CONNECTION LIMIT 20;

\q
```

---

# 🔧 TROUBLESHOOTING

## Issue 1: Gunicorn Not Starting

```bash
# Check logs
sudo journalctl -u gunicorn -n 50 --no-pager

# Check socket
sudo systemctl status gunicorn.socket

# Restart both
sudo systemctl restart gunicorn.socket
sudo systemctl restart gunicorn
```

---

## Issue 2: Static Files Not Loading

```bash
# Recollect static files
cd /var/www/tangail-doctors
source venv/bin/activate
python manage.py collectstatic --clear --noinput

# Check permissions
sudo chown -R deploy:www-data /var/www/tangail-doctors/staticfiles
sudo chmod -R 755 /var/www/tangail-doctors/staticfiles

# Restart services
sudo systemctl restart gunicorn nginx
```

---

## Issue 3: 502 Bad Gateway

```bash
# Check if Gunicorn is running
sudo systemctl status gunicorn

# Check socket file exists
ls -la /run/gunicorn.sock

# Check Nginx error logs
sudo tail -f /var/log/nginx/tangail-doctors-error.log

# Restart everything
sudo systemctl restart gunicorn nginx
```

---

## Issue 4: Database Connection Errors

```bash
# Test database connection
psql -U tangail_user -d tangail_doctors -h localhost

# Check PostgreSQL status
sudo systemctl status postgresql

# Check credentials in .env file
cat /var/www/tangail-doctors/.env | grep DATABASE_URL

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

## Issue 5: Media Upload Issues

```bash
# Check media directory permissions
ls -la /var/www/tangail-doctors/media

# Fix permissions
sudo chown -R deploy:www-data /var/www/tangail-doctors/media
sudo chmod -R 775 /var/www/tangail-doctors/media

# Check Django settings
python manage.py shell
>>> from django.conf import settings
>>> print(settings.MEDIA_ROOT)
>>> print(settings.MEDIA_URL)
```

---

# 📊 USEFUL COMMANDS

## Service Management

```bash
# Restart all services
sudo systemctl restart gunicorn nginx postgresql

# Check all service status
sudo systemctl status gunicorn nginx postgresql

# View logs in real-time
sudo journalctl -f
```

---

## Django Management

```bash
# Shell
cd /var/www/tangail-doctors
source venv/bin/activate
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Collect static
python manage.py collectstatic --noinput
```

---

## Quick Redeploy

```bash
cd /var/www/tangail-doctors
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

---

# 📝 POST-DEPLOYMENT CHECKLIST

## Migration from Old HTML Site to New Django Site

### Pre-Migration (Before DNS Switch)

- [ ] ✅ Backup old HTML website from Namecheap hosting
- [ ] ✅ Test new Django site on IP: http://217.216.73.118
- [ ] ✅ All pages working on VPS (doctors, emergency, categories)
- [ ] ✅ Language switcher working (Bangla ↔ English)
- [ ] ✅ Admin panel accessible: http://217.216.73.118/admin/
- [ ] ✅ Static files loading correctly (CSS, JS, images)
- [ ] ✅ Database populated with doctor data
- [ ] ✅ Media files uploaded (doctor images)
- [ ] ✅ SSL certificate ready to install (certbot installed)
- [ ] ✅ Screenshot old DNS records (for rollback)

### During Migration (DNS Switch)

- [ ] ✅ Cloudflare DNS updated to 217.216.73.118
- [ ] ✅ Proxy status set to "DNS only" (gray cloud)
- [ ] ✅ Both @ and www records updated
- [ ] ✅ DNS propagation verified (nslookup)
- [ ] ✅ Old website backup saved locally

### Post-Migration (After DNS Switch)

- [ ] ✅ Website accessible via domain: https://tangaildoctors.com
- [ ] ✅ Website accessible via www: https://www.tangaildoctors.com
- [ ] ✅ SSL certificate installed (Let's Encrypt)
- [ ] ✅ HTTPS redirect working (HTTP → HTTPS)
- [ ] ✅ Cloudflare SSL/TLS set to "Full (strict)"
- [ ] ✅ Admin panel: https://tangaildoctors.com/admin/
- [ ] ✅ Static files loading via HTTPS
- [ ] ✅ Media uploads working via admin
- [ ] ✅ Search functionality working
- [ ] ✅ Emergency doctors page working
- [ ] ✅ Hospital list showing correctly
- [ ] ✅ Category filtering functional
- [ ] ✅ Mobile responsive design working
- [ ] ✅ Language switching functional
- [ ] ✅ All doctor data visible
- [ ] ✅ Favicon showing
- [ ] ✅ Performance acceptable (loading speed)

### Security & Monitoring

- [ ] ✅ Firewall configured (UFW)
- [ ] ✅ SSH key authentication enabled
- [ ] ✅ Root login disabled
- [ ] ✅ Fail2Ban active
- [ ] ✅ Database backup cron job running
- [ ] ✅ SSL auto-renewal working (certbot timer)
- [ ] ✅ Gunicorn service enabled
- [ ] ✅ Nginx running properly
- [ ] ✅ PostgreSQL secure
- [ ] ✅ Log rotation configured

### Optional Enhancements

- [ ] 🔶 Cloudflare proxy enabled (orange cloud)
- [ ] 🔶 Cloudflare WAF rules configured
- [ ] 🔶 Redis caching enabled
- [ ] 🔶 CDN configured for media files
- [ ] 🔶 Google Analytics added
- [ ] 🔶 SEO meta tags added
- [ ] 🔶 Sitemap.xml generated
- [ ] 🔶 Robots.txt configured
- [ ] 🔶 Email notifications working
- [ ] 🔶 Uptime monitoring (UptimeRobot)

### Old Hosting Cleanup (After 2-4 Weeks)

- [ ] ⏰ New site stable for 2+ weeks
- [ ] ⏰ No major issues reported
- [ ] ⏰ All features verified working
- [ ] ⏰ Backups tested and working
- [ ] ⏰ Cancel Namecheap web hosting (keep domain!)
- [ ] ⏰ Remove old website files (after backup)
- [ ] ⏰ Update any external links/bookmarks
- [ ] ⏰ Notify regular users (if any)

---

## 🎯 Quick Verification Commands

```bash
# Check all services
sudo systemctl status gunicorn nginx postgresql

# Check website response
curl -I https://tangaildoctors.com

# Check SSL certificate
sudo certbot certificates

# Check disk space
df -h

# Check memory
free -h

# Check logs
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/nginx/tangaildoctors-error.log

# Check firewall
sudo ufw status verbose

# Check open ports
sudo netstat -tulpn | grep LISTEN
```

---

## 🚨 Common Post-Deployment Issues

### Issue: Old site still showing
**Cause:** DNS cache on your device  
**Solution:**
```powershell
# Windows - Flush DNS cache
ipconfig /flushdns

# Then test in incognito browser window
```

### Issue: Mixed content warnings (HTTP/HTTPS)
**Cause:** Some resources loading via HTTP  
**Solution:** Check all static files use HTTPS or relative URLs

### Issue: Admin panel won't open
**Cause:** ALLOWED_HOSTS not updated  
**Solution:** Check .env has `tangaildoctors.com`

### Issue: Static files not loading after DNS switch
**Cause:** Cloudflare caching old files  
**Solution:**
1. Cloudflare Dashboard → Caching
2. Click "Purge Everything"
3. Wait 30 seconds, reload page

### Issue: SSL certificate won't install
**Cause:** Cloudflare proxy enabled (orange cloud)  
**Solution:** Temporarily disable proxy (gray cloud) for SSL installation

---

# 🎯 NEXT STEPS

1. **Domain Setup**: Point your domain to 217.216.73.118
2. **SSL Certificate**: Install Let's Encrypt after domain setup
3. **Email Configuration**: Configure SMTP for notifications
4. **Monitoring**: Setup Uptime monitoring (UptimeRobot, etc.)
5. **CDN**: Consider Cloudflare for performance and security
6. **Backup Strategy**: Setup automated off-site backups
7. **Google Analytics**: Add tracking code
8. **SEO**: Setup meta tags, sitemap, robots.txt

---

# 📞 SUPPORT

If you encounter issues:

1. Check logs: `/var/log/gunicorn/`, `/var/log/nginx/`
2. Review this guide step-by-step
3. Search Django/Nginx/PostgreSQL docs
4. Ask AI assistant for specific errors

---

**Created:** February 9, 2026  
**Project:** Tangail Doctors Django Application  
**Server:** Contabo VPS 20 NVMe (Singapore)  
**Version:** 1.0

---

**Good luck with your deployment! 🚀**
