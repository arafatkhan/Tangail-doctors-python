# 🚀 Deployment Scripts - Tangail Doctors

Complete automation scripts for deploying Django project on Contabo VPS.

## 📋 Script Overview

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `01-server-setup.sh` | Install system packages, Python, PostgreSQL, Nginx | First time only |
| `02-database-setup.sh` | Create PostgreSQL database and user | First time only |
| `03-deploy-django.sh` | Deploy Django project from GitHub | First time only |
| `04-setup-gunicorn.sh` | Configure Gunicorn systemd service | First time only |
| `05-setup-nginx.sh` | Configure Nginx reverse proxy | First time only |
| `06-install-ssl.sh` | Install Let's Encrypt SSL certificate | After DNS setup |
| `07-upload-and-deploy.sh` | Quick re-deployment after code changes | Anytime |

---

## 🎯 Quick Start Guide

### Step 1: Upload Scripts to VPS

**From Windows PowerShell:**

```powershell
# Navigate to project directory
cd "D:\My work\htdocs\tangail-doctors-python"

# Upload deployment scripts to VPS
scp -r deployment-scripts root@217.216.73.118:/root/
```

### Step 2: SSH to VPS

```powershell
ssh root@217.216.73.118
```

Enter your Contabo root password when prompted.

### Step 3: Run Scripts in Order

```bash
# Navigate to scripts directory
cd /root/deployment-scripts

# Make all scripts executable
chmod +x *.sh

# Run scripts in order
./01-server-setup.sh       # ~15 minutes
./02-database-setup.sh     # ~1 minute - SAVE THE CREDENTIALS!
./03-deploy-django.sh      # ~10 minutes
./04-setup-gunicorn.sh     # ~2 minutes
./05-setup-nginx.sh        # ~2 minutes

# Test site: http://217.216.73.118

# Configure DNS to point to 217.216.73.118
# Wait for DNS propagation (5-30 minutes)

./06-install-ssl.sh        # ~2 minutes
```

---

## 📝 Detailed Instructions

### Before You Start

**What you need:**
1. ✅ Contabo VPS IP: 217.216.73.118
2. ✅ Root password (from Contabo email)
3. ✅ GitHub repository access
4. ✅ Cloudflare account (for DNS)
5. ⏰ Time: 4-6 hours total

---

### Script 1: Server Setup

**What it does:**
- Updates Ubuntu packages
- Installs Python 3.11
- Installs PostgreSQL 14
- Installs Nginx
- Configures firewall (UFW)
- Sets up swap memory
- Installs Certbot for SSL

**Run:**
```bash
./01-server-setup.sh
```

**Duration:** ~15 minutes

**Output:** Server ready with all required software

---

### Script 2: Database Setup

**What it does:**
- Creates PostgreSQL database: `tangail_doctors`
- Creates database user: `tangail_user`
- Generates secure random password
- Saves credentials to `/root/database-credentials.txt`

**Run:**
```bash
./02-database-setup.sh
```

**Duration:** ~1 minute

**⚠️ CRITICAL:** 
Copy and save the database credentials displayed on screen!
They are also saved in: `/root/database-credentials.txt`

**Output:**
```
Database Name: tangail_doctors
Database User: tangail_user
Database Password: [random-generated-password]
DATABASE_URL: postgresql://tangail_user:password@localhost:5432/tangail_doctors
```

---

### Script 3: Django Deployment

**What it does:**
- Creates project directory: `/var/www/tangail-doctors`
- Clones your GitHub repository
- Creates Python virtual environment
- Installs all dependencies
- Creates `.env` file with database credentials
- Runs database migrations
- Collects static files
- Creates superuser (optional)

**Before running:**
- Make sure your code is pushed to GitHub main branch
- If repository is private, prepare GitHub personal access token

**Run:**
```bash
./03-deploy-django.sh
```

**During execution:**
- Enter GitHub repository URL (or press Enter for default)
- Choose whether to create superuser now

**Duration:** ~10 minutes

**Output:** Django project deployed to `/var/www/tangail-doctors`

---

### Script 4: Gunicorn Setup

**What it does:**
- Creates Gunicorn socket file
- Creates Gunicorn systemd service
- Starts and enables Gunicorn
- Configures logging

**Run:**
```bash
./04-setup-gunicorn.sh
```

**Duration:** ~2 minutes

**Test:**
```bash
sudo systemctl status gunicorn
curl --unix-socket /run/gunicorn.sock http
```

**Output:** Gunicorn running as systemd service

---

### Script 5: Nginx Setup

**What it does:**
- Creates Nginx server block for tangaildoctors.com
- Configures reverse proxy to Gunicorn
- Sets up static and media file serving
- Enables the site and restarts Nginx

**Run:**
```bash
./05-setup-nginx.sh
```

**Duration:** ~2 minutes

**Test:**
```bash
curl http://217.216.73.118
# Should show your Django site HTML
```

**Visit in browser:**
http://217.216.73.118

**Output:** Website accessible via IP address

---

### 🌐 DNS Configuration (Manual Step)

**IMPORTANT: Do this before running script 6**

1. **Login to Cloudflare Dashboard**
   - URL: https://dash.cloudflare.com/
   - Select domain: `tangaildoctors.com`

2. **Update DNS Records**
   - Go to: DNS → Records
   - Update A record `@` → `217.216.73.118`
   - Update A record `www` → `217.216.73.118`
   - Set Proxy Status: **DNS only** (gray cloud)

3. **Verify DNS**
   ```powershell
   nslookup tangaildoctors.com
   # Should show: 217.216.73.118
   ```

4. **Wait for propagation** (5-30 minutes)

5. **Test domain**
   ```bash
   curl http://tangaildoctors.com
   # Should show your site
   ```

---

### Script 6: SSL Certificate

**What it does:**
- Verifies domain is accessible
- Installs Let's Encrypt SSL certificate
- Configures auto-renewal
- Updates Nginx to redirect HTTP → HTTPS

**Prerequisites:**
- ✅ DNS pointing to VPS
- ✅ Domain accessible via HTTP
- ✅ Cloudflare proxy disabled (gray cloud)

**Run:**
```bash
./06-install-ssl.sh
```

**During execution:**
- Confirm DNS is ready
- Enter email for certificate notifications

**Duration:** ~2 minutes

**Test:**
```bash
curl https://tangaildoctors.com
# Should show secure connection
```

**Visit in browser:**
https://tangaildoctors.com

**Output:** Website secured with HTTPS

---

### Script 7: Quick Re-deployment

**Use this anytime you update your code.**

**What it does:**
- Pulls latest code from GitHub
- Updates dependencies
- Runs migrations
- Compiles translations
- Collects static files
- Restarts Gunicorn

**Run:**
```bash
cd /root/deployment-scripts
./07-upload-and-deploy.sh
```

**Duration:** ~2 minutes

**When to use:**
- After pushing code changes to GitHub
- After updating dependencies
- After database model changes
- After updating static files

---

## 🐛 Troubleshooting

### Issue: Script permission denied

**Error:** `bash: ./01-server-setup.sh: Permission denied`

**Solution:**
```bash
chmod +x *.sh
```

---

### Issue: Git clone fails (private repository)

**Error:** `fatal: could not read Username for 'https://github.com'`

**Solution:**
Use personal access token:
```bash
git clone https://YOUR_TOKEN@github.com/username/repo.git .
```

Or configure the script manually to use correct URL.

---

### Issue: PostgreSQL connection failed

**Error:** `FATAL: password authentication failed`

**Solution:**
Check database credentials:
```bash
cat /root/database-credentials.txt
cat /var/www/tangail-doctors/.env | grep DATABASE_URL
```

Make sure they match!

---

### Issue: Gunicorn service failed

**Error:** `systemctl status gunicorn` shows failed

**Solution:**
Check logs:
```bash
sudo journalctl -u gunicorn -n 50 --no-pager
sudo tail -f /var/log/gunicorn/error.log
```

Common fixes:
```bash
# Fix permissions
sudo chown -R www-data:www-data /var/www/tangail-doctors

# Restart service
sudo systemctl restart gunicorn
```

---

### Issue: Nginx 502 Bad Gateway

**Error:** Website shows 502 error

**Solution:**
1. Check Gunicorn is running:
   ```bash
   sudo systemctl status gunicorn
   ```

2. Check socket exists:
   ```bash
   ls -la /run/gunicorn.sock
   ```

3. Restart both services:
   ```bash
   sudo systemctl restart gunicorn nginx
   ```

---

### Issue: SSL certificate fails

**Error:** `Failed authorization procedure`

**Solution:**
1. Verify DNS is correct:
   ```bash
   nslookup tangaildoctors.com
   ```

2. Ensure Cloudflare proxy is disabled (gray cloud)

3. Test domain accessibility:
   ```bash
   curl -I http://tangaildoctors.com
   ```

4. Retry SSL installation

---

## 📊 Verify Deployment

**After all scripts complete, verify:**

```bash
# Check all services
sudo systemctl status postgresql nginx gunicorn

# Check website
curl https://tangaildoctors.com

# Check SSL
sudo certbot certificates

# Check firewall
sudo ufw status

# Check disk space
df -h

# Check memory
free -h
```

**Visit in browser:**
- https://tangaildoctors.com
- https://www.tangaildoctors.com
- https://tangaildoctors.com/admin/

---

## 🔄 Useful Commands

```bash
# View Gunicorn logs
sudo tail -f /var/log/gunicorn/error.log

# View Nginx logs
sudo tail -f /var/log/nginx/tangail-doctors-error.log

# Restart services
sudo systemctl restart gunicorn nginx

# Django management
cd /var/www/tangail-doctors
source venv/bin/activate
python manage.py shell
python manage.py createsuperuser

# Database access
psql -U tangail_user -d tangail_doctors -h localhost
```

---

## 📞 Support

If you encounter issues:

1. Check script output for errors
2. Review logs: `/var/log/gunicorn/`, `/var/log/nginx/`
3. Verify all services are running
4. Check firewall settings
5. Verify DNS configuration

---

**Created:** February 9, 2026  
**Project:** Tangail Doctors Django Application  
**Target:** Contabo VPS 20 NVMe (Singapore)

**Good luck with your deployment! 🚀**
