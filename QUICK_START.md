# ⚡ QUICK START - Contabo VPS Deployment

## 📌 পরবর্তী পদক্ষেপ (Next Steps)

### ✅ সম্পন্ন হয়েছে (Completed):
- ✅ 7টি deployment scripts তৈরি
- ✅ settings.py production-ready
- ✅ requirements.txt updated
- ✅ সব configuration files ready

---

## 🚀 এখন যা করতে হবে

### Step 1: GitHub এ Push করুন

```powershell
# Project directory তে যান
cd "D:\My work\htdocs\tangail-doctors-python"

# Changes দেখুন
git status

# সব files add করুন
git add .

# Commit করুন
git commit -m "Add Contabo VPS deployment configuration and scripts"

# Push করুন
git push origin main
```

---

### Step 2: Scripts VPS এ Upload করুন

```powershell
# Scripts folder VPS এ upload করুন
scp -r deployment-scripts root@217.216.73.118:/root/

# Password দিতে হবে (Contabo email এ পাবেন)
```

**Alternative (যদি SCP কাজ না করে):**

Manual upload via FileZilla/WinSCP:
- Host: 217.216.73.118
- Username: root
- Password: [Contabo password]
- Upload: `deployment-scripts` folder to `/root/`

---

### Step 3: VPS এ SSH Connect করুন

```powershell
# SSH connection
ssh root@217.216.73.118

# Password দিন
```

---

### Step 4: Scripts Run করুন (VPS তে)

```bash
# Scripts directory তে যান
cd /root/deployment-scripts

# সব scripts executable করুন
chmod +x *.sh

# Scripts একটার পর একটা run করুন:

# 1. Server Setup (15 minutes)
./01-server-setup.sh

# 2. Database Setup (1 minute) - CREDENTIALS SAVE করবেন!
./02-database-setup.sh

# 3. Django Deploy (10 minutes)
#    - GitHub repository URL দিতে হবে
#    - Superuser create করতে বলবে
./03-deploy-django.sh

# 4. Setup Gunicorn (2 minutes)
./04-setup-gunicorn.sh

# 5. Setup Nginx (2 minutes)
./05-setup-nginx.sh

# Test করুন: http://217.216.73.118
```

---

### Step 5: DNS Configure করুন (Cloudflare)

**Login to Cloudflare:**
- URL: https://dash.cloudflare.com/
- Domain: tangaildoctors.com

**Update DNS Records:**

1. Click "DNS" → "Records"
2. Edit A record `@`:
   - Content: `217.216.73.118`
   - Proxy: **DNS only** (gray cloud)
3. Edit/Create A record `www`:
   - Content: `217.216.73.118`
   - Proxy: **DNS only** (gray cloud)
4. Save changes

**Verify DNS:**
```powershell
nslookup tangaildoctors.com
# Should show: 217.216.73.118
```

Wait 5-30 minutes for DNS propagation.

---

### Step 6: Install SSL Certificate (VPS তে)

```bash
# DNS ready থাকলে SSL install করুন
cd /root/deployment-scripts
./06-install-ssl.sh

# Email address দিতে হবে
```

Test: https://tangaildoctors.com

---

## 📋 Command Cheatsheet

### GitHub Commands (Windows PowerShell)
```powershell
# Push to GitHub
git add .
git commit -m "message"
git push origin main

# Upload to VPS
scp -r deployment-scripts root@217.216.73.118:/root/

# Connect to VPS
ssh root@217.216.73.118
```

### VPS Management Commands (After SSH)
```bash
# Check all services
sudo systemctl status postgresql nginx gunicorn

# Restart services
sudo systemctl restart gunicorn nginx

# View logs
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/nginx/tangail-doctors-error.log

# Django commands
cd /var/www/tangail-doctors
source venv/bin/activate
python manage.py createsuperuser
python manage.py shell

# Database access
psql -U tangail_user -d tangail_doctors -h localhost
# Password: check /root/database-credentials.txt
```

### Quick Redeploy (After code changes)
```bash
cd /root/deployment-scripts
./07-upload-and-deploy.sh
```

---

## 🔍 Verification Checklist

### After Setup Complete:

```bash
# On VPS - Check services
sudo systemctl status postgresql
sudo systemctl status nginx
sudo systemctl status gunicorn

# Test website
curl http://217.216.73.118
```

### After DNS & SSL:

**Browser Tests:**
- [ ] http://217.216.73.118 → Works
- [ ] http://tangaildoctors.com → Redirects to HTTPS
- [ ] https://tangaildoctors.com → Works
- [ ] https://www.tangaildoctors.com → Works
- [ ] https://tangaildoctors.com/admin/ → Admin panel
- [ ] Language switcher → Bangla ↔ English

---

## 🚨 যদি সমস্যা হয়

### Problem: SSH connection refused
```powershell
# Check IP again
ping 217.216.73.118

# Wait and retry
ssh root@217.216.73.118
```

### Problem: Scripts permission denied
```bash
chmod +x *.sh
```

### Problem: Git clone fails
Script will ask for repository URL.
Provide: `https://github.com/yourusername/Tangail-doctors-python.git`

If private repo:
`https://YOUR_TOKEN@github.com/username/repo.git`

### Problem: Service failed
```bash
# Check logs
sudo journalctl -u gunicorn -n 50
sudo journalctl -u nginx -n 50

# Restart services
sudo systemctl restart gunicorn nginx
```

---

## 📞 প্রয়োজনে

**Documentation:**
- Full Guide: `CONTABO_VPS_DEPLOYMENT.md`
- Scripts README: `deployment-scripts/README.md`
- Settings Guide: `deployment-scripts/SETTINGS_UPDATE_GUIDE.py`

**Log Files:**
- Gunicorn: `/var/log/gunicorn/error.log`
- Nginx: `/var/log/nginx/tangail-doctors-error.log`
- Database: `/root/database-credentials.txt`

---

## 🎯 Ready to Deploy?

1. ✅ GitHub push
2. ✅ Upload scripts to VPS
3. ✅ SSH to VPS
4. ✅ Run scripts
5. ✅ Configure DNS
6. ✅ Install SSL

**Total Time: ~4-6 hours**

**Let's deploy! 🚀**
