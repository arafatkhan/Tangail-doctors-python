# টাঙ্গাইল ডাক্তার তালিকা - Django Migration Instructions
## Complete Step-by-Step Guide

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Initial Setup](#phase-1-initial-setup)
4. [Phase 2: Database Design](#phase-2-database-design)
5. [Phase 3: Data Migration](#phase-3-data-migration)
6. [Phase 4: Views & URLs](#phase-4-views--urls)
7. [Phase 5: Templates](#phase-5-templates)
8. [Phase 6: Admin Panel](#phase-6-admin-panel)
9. [Phase 7: Static Files](#phase-7-static-files)
10. [Phase 8: Testing](#phase-8-testing)
11. [Phase 9: Deployment](#phase-9-deployment)
12. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

### Current State
- **Data Source**: `data.json` (380+ doctor records)
- **Frontend**: Pure HTML/CSS/JavaScript
- **Views**: 3 types (Card Grid, Table, Category-based)
- **Language**: Bengali (Bangla)

### Target State
- **Backend**: Django 4.2+
- **Database**: SQLite3 (upgradable to PostgreSQL)
- **Frontend**: Django Templates (Jinja2-like)
- **Features**: Search, Filter, Admin Panel, CRUD operations

---

## 🔧 Prerequisites

### Required Software
```bash
# Check Python version (must be 3.8+)
python --version

# Check pip
pip --version

# Check Git (optional)
git --version
```

### Recommended Tools
- **Code Editor**: VS Code, PyCharm
- **Browser**: Chrome/Firefox (for testing)
- **Database Viewer**: DB Browser for SQLite (optional)

---

## 📦 Phase 1: Initial Setup

### Step 1.1: Create Project Directory
```powershell
# Navigate to your work directory
cd "d:\My work\htdocs\"

# Create project folder
mkdir tangail-doctors-django
cd tangail-doctors-django
```

### Step 1.2: Create Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If execution policy error occurs, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 1.3: Install Django
```powershell
# Install Django and dependencies
pip install django==4.2
pip install pillow

# Create requirements.txt
pip freeze > requirements.txt
```

### Step 1.4: Create Django Project
```powershell
# Create Django project
django-admin startproject config .

# Create doctors app
python manage.py startapp doctors

# Verify installation
python manage.py --version
```

### Step 1.5: Initial Configuration

**Edit `config/settings.py`:**
```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'doctors',  # Add this line
]

# Language and timezone
LANGUAGE_CODE = 'bn'  # Bengali
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'doctors' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (if needed later)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Step 1.6: Test Initial Setup
```powershell
# Run development server
python manage.py runserver

# Open browser: http://127.0.0.1:8000/
# You should see Django welcome page
```

---

## 🗄️ Phase 2: Database Design

### Step 2.1: Create Doctor Model

**Edit `doctors/models.py`:**
```python
from django.db import models
from django.utils.html import strip_tags
import re

class Doctor(models.Model):
    """Doctor model for storing doctor information"""
    
    name = models.CharField(
        max_length=200, 
        verbose_name='নাম',
        help_text='ডাক্তারের পূর্ণ নাম'
    )
    qualification = models.TextField(
        verbose_name='যোগ্যতা',
        help_text='শিক্ষাগত যোগ্যতা (HTML tags allowed)'
    )
    specialty = models.CharField(
        max_length=200, 
        verbose_name='বিশেষত্ব',
        help_text='বিশেষজ্ঞতার ক্ষেত্র'
    )
    schedule = models.TextField(
        verbose_name='সময়সূচী',
        help_text='চেম্বার সময়সূচী (HTML tags allowed)'
    )
    hospital = models.CharField(
        max_length=200, 
        verbose_name='হাসপাতাল',
        help_text='হাসপাতাল/ক্লিনিকের নাম'
    )
    contact = models.CharField(
        max_length=200, 
        verbose_name='যোগাযোগ',
        help_text='ফোন নম্বর'
    )
    
    # Auto-generated fields
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='তৈরির সময়'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='সর্বশেষ আপডেট'
    )
    
    # For future use
    is_active = models.BooleanField(
        default=True, 
        verbose_name='সক্রিয়',
        help_text='ডাক্তার তালিকায় দেখানো হবে কিনা'
    )
    
    class Meta:
        verbose_name = 'ডাক্তার'
        verbose_name_plural = 'ডাক্তারগণ'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['specialty']),
            models.Index(fields=['hospital']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_clean_hospital(self):
        """Get hospital name without HTML tags"""
        return self.clean_text(self.hospital)
    
    def get_clean_specialty(self):
        """Get specialty without HTML tags"""
        return self.clean_text(self.specialty)
    
    @staticmethod
    def clean_text(text):
        """Remove HTML tags and normalize whitespace"""
        if not text:
            return ''
        text = re.sub(r'<br\s*/?>', ' ', text, flags=re.IGNORECASE)
        text = strip_tags(text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def get_category(self):
        """
        Determine main category based on specialty keywords
        Returns: Category name in Bengali
        """
        categories = {
            'প্রসূতি ও স্ত্রীরোগ বিশেষজ্ঞ': [
                'প্রসূতি', 'স্ত্রী', 'গাইনী', 'গাইনি', 'অবস', 'গাইনোলজি'
            ],
            'সার্জারি বিশেষজ্ঞ': [
                'সার্জন', 'সার্জারি', 'শল্য', 'অপারেশন', 'ল্যাপারোস্কপিক'
            ],
            'শিশু বিশেষজ্ঞ': [
                'শিশু', 'নবজাতক', 'পেডিয়াট্রিক', 'কিশোর'
            ],
            'হৃদরোগ বিশেষজ্ঞ': [
                'হৃদরোগ', 'হার্ট', 'কার্ডিও', 'বাতজ্বর', 'হৃদ'
            ],
            'চর্মরোগ বিশেষজ্ঞ': [
                'চর্ম', 'ত্বক', 'যৌন', 'এলার্জি', 'স্কিন'
            ],
            'মেডিসিন বিশেষজ্ঞ': [
                'মেডিসিন', 'চিকিৎসক', 'ডায়াবেটিস', 'অভ্যন্তরীণ', 'বক্ষব্যাধি'
            ],
            'চক্ষু বিশেষজ্ঞ': [
                'চক্ষু', 'চোখ', 'অপথালমো', 'কেটারেক্ট', 'ছানি'
            ],
            'দাঁতের চিকিৎসক': [
                'দাঁত', 'ডেন্টাল', 'দন্ত', 'মুখ'
            ],
            'হাড় ও জয়েন্ট বিশেষজ্ঞ': [
                'হাড়', 'অর্থো', 'জয়েন্ট', 'ফিজিও', 'বাত', 'ব্যথা', 'পঙ্গু'
            ],
            'নাক-কান-গলা বিশেষজ্ঞ': [
                'নাক', 'কান', 'গলা', 'ইএনটি', 'ই এন টি', 'হেড নেক'
            ],
            'কিডনি রোগ বিশেষজ্ঞ': [
                'কিডনি', 'বৃক্ক', 'ডায়ালাইসিস', 'নেফ্রো', 'মূত্র'
            ],
            'মানসিক রোগ বিশেষজ্ঞ': [
                'মানসিক', 'সাইকিয়াট্রি', 'মনোরোগ'
            ],
            'নিউরো বিশেষজ্ঞ': [
                'নিউরো', 'স্নায়ু', 'মস্তিষ্ক', 'ব্রেইন'
            ],
            'আল্ট্রাসনোগ্রাম বিশেষজ্ঞ': [
                'আল্ট্রা', 'সনো', 'রেডিও', 'ইমেজিং'
            ],
        }
        
        specialty_lower = self.specialty.lower()
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in specialty_lower:
                    return category
        
        return 'অন্যান্য বিশেষজ্ঞ'
```

### Step 2.2: Create and Run Migrations
```powershell
# Create migration files
python manage.py makemigrations

# Check migration SQL (optional)
python manage.py sqlmigrate doctors 0001

# Apply migrations
python manage.py migrate

# Verify database
python manage.py dbshell
# Then run: .tables (to see tables)
# Exit: .quit
```

---

## 📥 Phase 3: Data Migration

### Step 3.1: Copy data.json to Project Root
```powershell
# Copy your existing data.json file to project root
Copy-Item "..\tangail-doctors-python\data.json" "."
```

### Step 3.2: Create Import Script

**Create `doctors/management/commands/import_data.py`:**
```powershell
# Create directories
New-Item -ItemType Directory -Path "doctors\management\commands" -Force

# Create __init__.py files
New-Item -ItemType File -Path "doctors\management\__init__.py"
New-Item -ItemType File -Path "doctors\management\commands\__init__.py"
```

**Edit `doctors/management/commands/import_data.py`:**
```python
import json
import os
from django.core.management.base import BaseCommand
from doctors.models import Doctor

class Command(BaseCommand):
    help = 'Import doctors from data.json'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before import',
        )
    
    def handle(self, *args, **options):
        # Find data.json
        json_path = os.path.join(os.getcwd(), 'data.json')
        
        if not os.path.exists(json_path):
            self.stdout.write(
                self.style.ERROR(f'❌ data.json not found at {json_path}')
            )
            return
        
        # Load JSON data
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                doctors_data = json.load(f)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error reading JSON: {e}')
            )
            return
        
        # Clear existing data if requested
        if options['clear']:
            Doctor.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('⚠️  Cleared existing doctor data')
            )
        
        # Import data
        success_count = 0
        error_count = 0
        
        for data in doctors_data:
            try:
                doctor, created = Doctor.objects.update_or_create(
                    name=data.get('name', '').strip(),
                    defaults={
                        'qualification': data.get('qualification', ''),
                        'specialty': data.get('specialty', ''),
                        'schedule': data.get('schedule', ''),
                        'hospital': data.get('hospital', ''),
                        'contact': data.get('contact', ''),
                        'is_active': True,
                    }
                )
                success_count += 1
                
                if created:
                    self.stdout.write(f'✅ Created: {doctor.name}')
                else:
                    self.stdout.write(f'🔄 Updated: {doctor.name}')
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Error importing {data.get("name", "Unknown")}: {e}'
                    )
                )
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Import complete!'
                f'\n   Success: {success_count}'
                f'\n   Errors: {error_count}'
                f'\n   Total in DB: {Doctor.objects.count()}'
            )
        )
```

### Step 3.3: Run Import
```powershell
# Import data (keep existing if any)
python manage.py import_data

# OR clear and import fresh
python manage.py import_data --clear

# Verify import
python manage.py shell
>>> from doctors.models import Doctor
>>> Doctor.objects.count()
>>> Doctor.objects.first().name
>>> exit()
```

---

## 🎨 Phase 4: Views & URLs

### Step 4.1: Create Views

**Edit `doctors/views.py`:**
```python
from django.shortcuts import render
from django.db.models import Q
from .models import Doctor
from collections import defaultdict

def index(request):
    """
    Card grid view with search and dual filters
    """
    # Get all active doctors
    doctors = Doctor.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        doctors = doctors.filter(
            Q(name__icontains=search_query) |
            Q(specialty__icontains=search_query) |
            Q(hospital__icontains=search_query)
        )
    
    # Category filter
    category_filter = request.GET.get('category', '').strip()
    
    # Hospital filter
    hospital_filter = request.GET.get('hospital', '').strip()
    if hospital_filter:
        doctors = doctors.filter(hospital__icontains=hospital_filter)
    
    # Apply category filter (done after DB query since it's computed)
    doctors_list = list(doctors)
    if category_filter:
        doctors_list = [d for d in doctors_list if d.get_category() == category_filter]
    
    # Get unique hospitals and categories
    all_doctors = Doctor.objects.filter(is_active=True)
    hospitals = sorted(set(
        d.get_clean_hospital() 
        for d in all_doctors 
        if d.get_clean_hospital()
    ))
    
    categories = [
        'প্রসূতি ও স্ত্রীরোগ বিশেষজ্ঞ',
        'সার্জারি বিশেষজ্ঞ',
        'শিশু বিশেষজ্ঞ',
        'হৃদরোগ বিশেষজ্ঞ',
        'চর্মরোগ বিশেষজ্ঞ',
        'মেডিসিন বিশেষজ্ঞ',
        'চক্ষু বিশেষজ্ঞ',
        'দাঁতের চিকিৎসক',
        'হাড় ও জয়েন্ট বিশেষজ্ঞ',
        'নাক-কান-গলা বিশেষজ্ঞ',
        'কিডনি রোগ বিশেষজ্ঞ',
        'মানসিক রোগ বিশেষজ্ঞ',
        'নিউরো বিশেষজ্ঞ',
        'আল্ট্রাসনোগ্রাম বিশেষজ্ঞ',
        'অন্যান্য বিশেষজ্ঞ',
    ]
    
    context = {
        'doctors': doctors_list,
        'hospitals': hospitals,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
        'selected_hospital': hospital_filter,
        'total_count': len(doctors_list),
    }
    
    return render(request, 'doctors/index.html', context)


def table_view(request):
    """
    Table view with hospital filter
    """
    doctors = Doctor.objects.filter(is_active=True)
    
    # Hospital filter
    hospital_filter = request.GET.get('hospital', '').strip()
    if hospital_filter:
        doctors = doctors.filter(hospital__icontains=hospital_filter)
    
    # Get unique hospitals
    all_doctors = Doctor.objects.filter(is_active=True)
    hospitals = sorted(set(
        d.get_clean_hospital() 
        for d in all_doctors 
        if d.get_clean_hospital()
    ))
    
    context = {
        'doctors': doctors,
        'hospitals': hospitals,
        'selected_hospital': hospital_filter,
        'total_count': doctors.count(),
    }
    
    return render(request, 'doctors/table.html', context)


def category_view(request):
    """
    Category-based view with drill-down
    """
    doctors = Doctor.objects.filter(is_active=True)
    
    # Group doctors by category
    categories_data = defaultdict(list)
    
    for doctor in doctors:
        category = doctor.get_category()
        categories_data[category].append(doctor)
    
    # Sort categories by count (descending)
    sorted_categories = sorted(
        categories_data.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    context = {
        'categories': sorted_categories,
        'total_doctors': doctors.count(),
    }
    
    return render(request, 'doctors/category.html', context)


def doctor_detail(request, pk):
    """
    Individual doctor detail page (optional)
    """
    from django.shortcuts import get_object_or_404
    
    doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
    
    # Get related doctors (same specialty or hospital)
    related = Doctor.objects.filter(
        Q(specialty__icontains=doctor.get_clean_specialty()[:20]) |
        Q(hospital__icontains=doctor.get_clean_hospital()[:20])
    ).exclude(pk=doctor.pk).filter(is_active=True)[:5]
    
    context = {
        'doctor': doctor,
        'related_doctors': related,
    }
    
    return render(request, 'doctors/detail.html', context)
```

### Step 4.2: Create URLs

**Create `doctors/urls.py`:**
```python
from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.index, name='index'),
    path('table/', views.table_view, name='table'),
    path('categories/', views.category_view, name='categories'),
    path('doctor/<int:pk>/', views.doctor_detail, name='detail'),
]
```

**Edit `config/urls.py`:**
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('doctors.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## 🎭 Phase 5: Templates

### Step 5.1: Create Template Structure
```powershell
# Create templates directory
New-Item -ItemType Directory -Path "doctors\templates\doctors" -Force
```

### Step 5.2: Create Base Template

**Create `doctors/templates/doctors/base.html`:**
```html
{% load static %}
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="টাঙ্গাইল জেলার ডাক্তারদের সম্পূর্ণ তালিকা - বিশেষজ্ঞ ডাক্তার খুঁজুন">
    <meta name="keywords" content="টাঙ্গাইল, ডাক্তার, হাসপাতাল, চিকিৎসক, বিশেষজ্ঞ">
    <title>{% block title %}টাঙ্গাইল ডাক্তার তালিকা{% endblock %}</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="header-content">
                <h1 class="site-title">🏥 টাঙ্গাইল ডাক্তার তালিকা</h1>
                <nav class="nav">
                    <a href="{% url 'doctors:index' %}" 
                       class="nav-link {% if request.resolver_match.url_name == 'index' %}active{% endif %}">
                        হোম
                    </a>
                    <a href="{% url 'doctors:table' %}" 
                       class="nav-link {% if request.resolver_match.url_name == 'table' %}active{% endif %}">
                        টেবিল ভিউ
                    </a>
                    <a href="{% url 'doctors:categories' %}" 
                       class="nav-link {% if request.resolver_match.url_name == 'categories' %}active{% endif %}">
                        ক্যাটাগরি
                    </a>
                </nav>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <p>&copy; ২০২৬ টাঙ্গাইল ডাক্তার তালিকা। সর্বস্বত্ব সংরক্ষিত।</p>
                <p class="footer-meta">
                    <small>মোট ডাক্তার: <strong>{{ total_doctors|default:"380+" }}</strong></small>
                </p>
            </div>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="{% static 'js/script.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Step 5.3: Create Index Template

**Create `doctors/templates/doctors/index.html`:**
```html
{% extends 'doctors/base.html' %}

{% block title %}হোম - টাঙ্গাইল ডাক্তার তালিকা{% endblock %}

{% block content %}
<div class="container">
    <!-- Search and Filters Section -->
    <section class="search-section">
        <form method="get" action="{% url 'doctors:index' %}" class="search-form">
            <!-- Search Input -->
            <div class="search-box">
                <input 
                    type="text" 
                    name="search" 
                    id="searchInput"
                    class="search-input" 
                    placeholder="ডাক্তারের নাম, বিশেষত্ব বা হাসপাতাল খুঁজুন..."
                    value="{{ search_query }}"
                >
                <button type="submit" class="search-btn">🔍 খুঁজুন</button>
            </div>
            
            <!-- Filters -->
            <div class="filters">
                <div class="filter-group">
                    <label for="categoryFilter">ক্যাটাগরি:</label>
                    <select name="category" id="categoryFilter" class="filter-select">
                        <option value="">সকল ক্যাটাগরি</option>
                        {% for category in categories %}
                        <option value="{{ category }}" 
                                {% if category == selected_category %}selected{% endif %}>
                            {{ category }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="filter-group">
                    <label for="hospitalFilter">হাসপাতাল:</label>
                    <select name="hospital" id="hospitalFilter" class="filter-select">
                        <option value="">সকল হাসপাতাল</option>
                        {% for hospital in hospitals %}
                        <option value="{{ hospital }}" 
                                {% if hospital == selected_hospital %}selected{% endif %}>
                            {{ hospital }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                
                {% if search_query or selected_category or selected_hospital %}
                <a href="{% url 'doctors:index' %}" class="btn-reset">🔄 রিসেট</a>
                {% endif %}
            </div>
            
            <!-- Results Count -->
            <div class="results-info">
                <p>মোট <strong>{{ total_count }}</strong> জন ডাক্তার পাওয়া গেছে</p>
            </div>
        </form>
    </section>

    <!-- Doctors Grid -->
    <section class="doctors-grid">
        {% if doctors %}
            {% for doctor in doctors %}
            <div class="doctor-card">
                <div class="card-header">
                    <h3 class="doctor-name">{{ doctor.name }}</h3>
                    <span class="doctor-category">{{ doctor.get_category }}</span>
                </div>
                
                <div class="card-body">
                    <p class="doctor-specialty">
                        <strong>বিশেষত্ব:</strong> {{ doctor.specialty }}
                    </p>
                    
                    <div class="doctor-details">
                        <p><strong>যোগ্যতা:</strong></p>
                        <div class="detail-content">{{ doctor.qualification|safe }}</div>
                        
                        <p><strong>সময়সূচী:</strong></p>
                        <div class="detail-content">{{ doctor.schedule|safe }}</div>
                        
                        <p><strong>হাসপাতাল:</strong> {{ doctor.hospital|safe }}</p>
                        
                        <p><strong>যোগাযোগ:</strong></p>
                        <div class="contact-info">{{ doctor.contact|safe }}</div>
                    </div>
                </div>
                
                <div class="card-footer">
                    <a href="{% url 'doctors:detail' doctor.pk %}" class="btn-details">
                        বিস্তারিত দেখুন →
                    </a>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div class="no-results">
                <p>😔 কোনো ডাক্তার পাওয়া যায়নি</p>
                <a href="{% url 'doctors:index' %}" class="btn-reset">সব ডাক্তার দেখুন</a>
            </div>
        {% endif %}
    </section>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Auto-submit form on filter change
    document.getElementById('categoryFilter').addEventListener('change', function() {
        this.form.submit();
    });
    
    document.getElementById('hospitalFilter').addEventListener('change', function() {
        this.form.submit();
    });
</script>
{% endblock %}
```

### Step 5.4: Create Table Template

**Create `doctors/templates/doctors/table.html`:**
```html
{% extends 'doctors/base.html' %}

{% block title %}টেবিল ভিউ - টাঙ্গাইল ডাক্তার তালিকা{% endblock %}

{% block content %}
<div class="container">
    <!-- Filter Section -->
    <section class="filter-section">
        <form method="get" action="{% url 'doctors:table' %}" class="filter-form">
            <div class="filter-group">
                <label for="hospitalFilter">হাসপাতাল ফিল্টার করুন:</label>
                <select name="hospital" id="hospitalFilter" class="filter-select" onchange="this.form.submit()">
                    <option value="">সকল হাসপাতাল</option>
                    {% for hospital in hospitals %}
                    <option value="{{ hospital }}" 
                            {% if hospital == selected_hospital %}selected{% endif %}>
                        {{ hospital }}
                    </option>
                    {% endfor %}
                </select>
                
                {% if selected_hospital %}
                <a href="{% url 'doctors:table' %}" class="btn-reset">🔄 রিসেট</a>
                {% endif %}
            </div>
            
            <div class="results-info">
                <p>মোট <strong>{{ total_count }}</strong> জন ডাক্তার</p>
            </div>
        </form>
    </section>

    <!-- Table Section -->
    <section class="table-section">
        <div class="table-wrapper">
            <table class="doctors-table">
                <thead>
                    <tr>
                        <th>নাম</th>
                        <th>যোগ্যতা</th>
                        <th>বিশেষত্ব</th>
                        <th>সময়সূচী</th>
                        <th>হাসপাতাল</th>
                        <th>যোগাযোগ</th>
                    </tr>
                </thead>
                <tbody>
                    {% if doctors %}
                        {% for doctor in doctors %}
                        <tr>
                            <td data-label="নাম">
                                <a href="{% url 'doctors:detail' doctor.pk %}" class="doctor-link">
                                    {{ doctor.name }}
                                </a>
                            </td>
                            <td data-label="যোগ্যতা">{{ doctor.qualification|safe }}</td>
                            <td data-label="বিশেষত্ব">{{ doctor.specialty }}</td>
                            <td data-label="সময়সূচী">{{ doctor.schedule|safe }}</td>
                            <td data-label="হাসপাতাল">{{ doctor.hospital|safe }}</td>
                            <td data-label="যোগাযোগ">{{ doctor.contact|safe }}</td>
                        </tr>
                        {% endfor %}
                    {% else %}
                        <tr>
                            <td colspan="6" class="no-data">
                                😔 কোনো ডাক্তার পাওয়া যায়নি
                            </td>
                        </tr>
                    {% endif %}
                </tbody>
            </table>
        </div>
    </section>
</div>
{% endblock %}
```

### Step 5.5: Create Category Template

**Create `doctors/templates/doctors/category.html`:**
```html
{% extends 'doctors/base.html' %}

{% block title %}ক্যাটাগরি - টাঙ্গাইল ডাক্তার তালিকা{% endblock %}

{% block content %}
<div class="container">
    <section class="intro-section">
        <h2>বিশেষজ্ঞ ডাক্তার ক্যাটাগরি</h2>
        <p>আপনার প্রয়োজনীয় বিশেষজ্ঞ ডাক্তার খুঁজে নিন</p>
    </section>

    <!-- Category Grid -->
    <section class="category-grid">
        {% for category, doctor_list in categories %}
        <div class="category-card">
            <div class="category-header">
                <h3>{{ category }}</h3>
                <span class="doctor-count">{{ doctor_list|length }} জন</span>
            </div>
            
            <div class="category-body">
                <button class="btn-expand" onclick="toggleCategory('{{ forloop.counter }}')">
                    বিস্তারিত দেখুন ▼
                </button>
                
                <div id="category-{{ forloop.counter }}" class="category-details" style="display: none;">
                    <table class="mini-table">
                        <thead>
                            <tr>
                                <th>নাম</th>
                                <th>হাসপাতাল</th>
                                <th>যোগাযোগ</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for doctor in doctor_list %}
                            <tr>
                                <td>
                                    <a href="{% url 'doctors:detail' doctor.pk %}">
                                        {{ doctor.name }}
                                    </a>
                                </td>
                                <td>{{ doctor.get_clean_hospital }}</td>
                                <td>{{ doctor.contact|striptags|slice:":20" }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        {% empty %}
        <p class="no-data">কোনো ক্যাটাগরি পাওয়া যায়নি</p>
        {% endfor %}
    </section>
</div>
{% endblock %}

{% block extra_js %}
<script>
function toggleCategory(id) {
    const details = document.getElementById('category-' + id);
    const button = details.previousElementSibling;
    
    if (details.style.display === 'none') {
        details.style.display = 'block';
        button.textContent = 'বিস্তারিত লুকান ▲';
    } else {
        details.style.display = 'none';
        button.textContent = 'বিস্তারিত দেখুন ▼';
    }
}
</script>
{% endblock %}
```

---

## 👨‍💼 Phase 6: Admin Panel

### Step 6.1: Configure Admin

**Edit `doctors/admin.py`:**
```python
from django.contrib import admin
from django.utils.html import format_html
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Admin interface for Doctor model"""
    
    # List display
    list_display = [
        'name', 
        'specialty', 
        'hospital_display', 
        'category_badge',
        'is_active',
        'updated_at'
    ]
    
    # Filters
    list_filter = [
        'is_active',
        'created_at',
        'updated_at',
    ]
    
    # Search
    search_fields = [
        'name',
        'specialty',
        'hospital',
        'qualification',
    ]
    
    # Ordering
    ordering = ['name']
    
    # Items per page
    list_per_page = 50
    
    # Editable fields in list
    list_editable = ['is_active']
    
    # Date hierarchy
    date_hierarchy = 'created_at'
    
    # Fieldsets for detail view
    fieldsets = (
        ('মূল তথ্য', {
            'fields': ('name', 'specialty', 'is_active')
        }),
        ('যোগ্যতা ও অভিজ্ঞতা', {
            'fields': ('qualification',),
            'description': 'HTML ট্যাগ ব্যবহার করা যাবে (<br> for line break)'
        }),
        ('সময় ও স্থান', {
            'fields': ('schedule', 'hospital', 'contact')
        }),
        ('সিস্টেম তথ্য', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']
    
    # Custom display methods
    def hospital_display(self, obj):
        """Display clean hospital name"""
        return obj.get_clean_hospital()
    hospital_display.short_description = 'হাসপাতাল'
    
    def category_badge(self, obj):
        """Display category as colored badge"""
        category = obj.get_category()
        colors = {
            'প্রসূতি ও স্ত্রীরোগ বিশেষজ্ঞ': '#ec4899',
            'সার্জারি বিশেষজ্ঞ': '#3b82f6',
            'শিশু বিশেষজ্ঞ': '#10b981',
            'হৃদরোগ বিশেষজ্ঞ': '#ef4444',
            'চর্মরোগ বিশেষজ্ঞ': '#f59e0b',
            'মেডিসিন বিশেষজ্ঞ': '#6366f1',
        }
        color = colors.get(category, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, category
        )
    category_badge.short_description = 'ক্যাটাগরি'
    
    # Actions
    actions = ['activate_doctors', 'deactivate_doctors']
    
    def activate_doctors(self, request, queryset):
        """Activate selected doctors"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} জন ডাক্তার সক্রিয় করা হয়েছে')
    activate_doctors.short_description = 'নির্বাচিত ডাক্তার সক্রিয় করুন'
    
    def deactivate_doctors(self, request, queryset):
        """Deactivate selected doctors"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} জন ডাক্তার নিষ্ক্রিয় করা হয়েছে')
    deactivate_doctors.short_description = 'নির্বাচিত ডাক্তার নিষ্ক্রিয় করুন'

# Customize admin site
admin.site.site_header = 'টাঙ্গাইল ডাক্তার তালিকা - অ্যাডমিন'
admin.site.site_title = 'ডাক্তার তালিকা'
admin.site.index_title = 'ড্যাশবোর্ড'
```

### Step 6.2: Create Superuser
```powershell
# Create admin user
python manage.py createsuperuser

# Username: admin
# Email: admin@example.com
# Password: (enter strong password)

# Start server and visit http://127.0.0.1:8000/admin/
python manage.py runserver
```

---

## 🎨 Phase 7: Static Files

### Step 7.1: Create Static Directory Structure
```powershell
# Create static directories
New-Item -ItemType Directory -Path "doctors\static\css" -Force
New-Item -ItemType Directory -Path "doctors\static\js" -Force
New-Item -ItemType Directory -Path "doctors\static\images" -Force
```

### Step 7.2: Copy CSS File

**Copy your existing `styles.css` to `doctors/static/css/styles.css`**

Or create a new one with Bengali font support:

**`doctors/static/css/styles.css`:**
```css
/* Base Styles */
:root {
    --primary-color: #2563eb;
    --secondary-color: #10b981;
    --danger-color: #ef4444;
    --warning-color: #f59e0b;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-300: #d1d5db;
    --gray-700: #374151;
    --gray-900: #111827;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Hind Siliguri', sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: var(--gray-900);
    background: var(--gray-100);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header */
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.site-title {
    font-size: 1.8rem;
    font-weight: 700;
}

.nav {
    display: flex;
    gap: 1rem;
}

.nav-link {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    transition: background 0.3s;
    font-weight: 500;
}

.nav-link:hover,
.nav-link.active {
    background: rgba(255,255,255,0.2);
}

/* Search Section */
.search-section {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    margin: 2rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.search-box {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.search-input {
    flex: 1;
    padding: 0.75rem 1rem;
    border: 2px solid var(--gray-300);
    border-radius: 5px;
    font-size: 1rem;
    font-family: 'Hind Siliguri', sans-serif;
}

.search-btn {
    padding: 0.75rem 2rem;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 600;
    transition: background 0.3s;
}

.search-btn:hover {
    background: #1d4ed8;
}

/* Filters */
.filters {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    align-items: end;
}

.filter-group {
    flex: 1;
    min-width: 200px;
}

.filter-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: var(--gray-700);
}

.filter-select {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid var(--gray-300);
    border-radius: 5px;
    font-family: 'Hind Siliguri', sans-serif;
    font-size: 1rem;
}

.btn-reset {
    padding: 0.75rem 1.5rem;
    background: var(--danger-color);
    color: white;
    text-decoration: none;
    border-radius: 5px;
    font-weight: 600;
    display: inline-block;
    transition: background 0.3s;
}

.btn-reset:hover {
    background: #dc2626;
}

/* Results Info */
.results-info {
    margin-top: 1rem;
    padding: 0.75rem;
    background: var(--gray-100);
    border-radius: 5px;
    text-align: center;
}

/* Doctor Grid */
.doctors-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.doctor-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: transform 0.3s, box-shadow 0.3s;
}

.doctor-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.card-header {
    border-bottom: 2px solid var(--gray-200);
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}

.doctor-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.doctor-category {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background: var(--secondary-color);
    color: white;
    border-radius: 15px;
    font-size: 0.85rem;
}

.doctor-specialty {
    font-size: 1rem;
    color: var(--gray-700);
    margin-bottom: 1rem;
}

.doctor-details p {
    margin-bottom: 0.75rem;
}

.detail-content,
.contact-info {
    padding: 0.5rem;
    background: var(--gray-100);
    border-radius: 5px;
    margin-top: 0.25rem;
    font-size: 0.95rem;
    line-height: 1.7;
}

.card-footer {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--gray-200);
}

.btn-details {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: var(--primary-color);
    color: white;
    text-decoration: none;
    border-radius: 5px;
    font-weight: 600;
    transition: background 0.3s;
}

.btn-details:hover {
    background: #1d4ed8;
}

/* Table Styles */
.table-wrapper {
    background: white;
    border-radius: 10px;
    overflow-x: auto;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.doctors-table {
    width: 100%;
    border-collapse: collapse;
}

.doctors-table th {
    background: var(--primary-color);
    color: white;
    padding: 1rem;
    text-align: left;
    font-weight: 600;
}

.doctors-table td {
    padding: 1rem;
    border-bottom: 1px solid var(--gray-200);
}

.doctors-table tr:hover {
    background: var(--gray-100);
}

.doctor-link {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 600;
}

.doctor-link:hover {
    text-decoration: underline;
}

/* Category Grid */
.category-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.category-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: transform 0.3s;
}

.category-card:hover {
    transform: translateY(-3px);
}

.category-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.doctor-count {
    background: var(--secondary-color);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.9rem;
}

.btn-expand {
    width: 100%;
    padding: 0.75rem;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 600;
    font-family: 'Hind Siliguri', sans-serif;
}

.category-details {
    margin-top: 1rem;
}

/* Footer */
.footer {
    background: var(--gray-900);
    color: white;
    padding: 2rem 0;
    margin-top: 3rem;
    text-align: center;
}

.footer-meta {
    margin-top: 0.5rem;
    opacity: 0.8;
}

/* No Results */
.no-results,
.no-data {
    text-align: center;
    padding: 3rem;
    background: white;
    border-radius: 10px;
    font-size: 1.2rem;
    color: var(--gray-700);
}

/* Responsive */
@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        text-align: center;
    }
    
    .doctors-grid {
        grid-template-columns: 1fr;
    }
    
    .search-box {
        flex-direction: column;
    }
    
    .filters {
        flex-direction: column;
    }
    
    .doctors-table {
        font-size: 0.9rem;
    }
    
    .doctors-table th,
    .doctors-table td {
        padding: 0.5rem;
    }
}
```

### Step 7.3: Copy JavaScript

**Copy your `script.js` to `doctors/static/js/script.js`**

---

## ✅ Phase 8: Testing

### Step 8.1: Run Tests
```powershell
# Check for issues
python manage.py check

# Run development server
python manage.py runserver

# Test URLs:
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/table/
# http://127.0.0.1:8000/categories/
# http://127.0.0.1:8000/admin/
```

### Step 8.2: Test Checklist
- [ ] Homepage loads correctly
- [ ] Search functionality works
- [ ] Category filter works
- [ ] Hospital filter works
- [ ] Table view displays correctly
- [ ] Category view groups correctly
- [ ] Admin panel accessible
- [ ] Can add/edit doctors in admin
- [ ] Mobile responsive design works
- [ ] Bengali text displays properly

---

## 🚀 Phase 9: Deployment

### Option 1: PythonAnywhere (Free)

**Step 1: Create Account**
```
Visit: https://www.pythonanywhere.com
Sign up for free account
```

**Step 2: Upload Code**
```bash
# Via Git
git clone https://github.com/your-repo/tangail-doctors.git

# Or upload zip file via Files tab
```

**Step 3: Setup Virtual Environment**
```bash
mkvirtualenv --python=python3.10 tangail
pip install -r requirements.txt
```

**Step 4: Configure WSGI**
```python
# Edit /var/www/yourusername_pythonanywhere_com_wsgi.py

import sys
import os

project_home = '/home/yourusername/tangail-doctors-django'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Step 5: Static Files**
```bash
python manage.py collectstatic --noinput
```

**Step 6: Database**
```bash
python manage.py migrate
python manage.py import_data --clear
python manage.py createsuperuser
```

### Option 2: Railway.app

**Step 1: Install Railway CLI**
```powershell
npm install -g @railway/cli
```

**Step 2: Create Files**

**`Procfile`:**
```
web: gunicorn config.wsgi --log-file -
```

**`runtime.txt`:**
```
python-3.10.0
```

**Update `requirements.txt`:**
```txt
Django==4.2
gunicorn==21.2.0
whitenoise==6.5.0
pillow==10.0.0
```

**Update `config/settings.py`:**
```python
# Add to MIDDLEWARE (after SecurityMiddleware)
'whitenoise.middleware.WhiteNoiseMiddleware',

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
if not DEBUG:
    ALLOWED_HOSTS = ['*']  # Replace with your domain
    CSRF_TRUSTED_ORIGINS = ['https://your-app.railway.app']
```

**Step 3: Deploy**
```bash
railway login
railway init
railway up
```

---

## 🔧 Troubleshooting

### Issue 1: Virtual Environment Not Activating
```powershell
# Solution: Change execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 2: Bengali Text Not Displaying
```python
# Solution: Check encoding in settings.py
# Add to settings.py:
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
```

### Issue 3: Static Files Not Loading
```bash
# Solution: Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT and STATIC_URL in settings.py
```

### Issue 4: Import Command Not Found
```powershell
# Solution: Verify directory structure
# Ensure __init__.py files exist in:
# doctors/management/__init__.py
# doctors/management/commands/__init__.py
```

### Issue 5: Database Migration Errors
```bash
# Solution: Reset migrations
python manage.py migrate --fake doctors zero
python manage.py migrate doctors
```

---

## 📚 Additional Resources

### Official Documentation
- Django: https://docs.djangoproject.com/
- Python: https://docs.python.org/3/
- SQLite: https://www.sqlite.org/docs.html

### Deployment Guides
- PythonAnywhere: https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
- Railway: https://docs.railway.app/deploy/deployments
- Heroku: https://devcenter.heroku.com/categories/python-support

### Learning Resources
- Django for Beginners: https://djangoforbeginners.com/
- Real Python: https://realpython.com/tutorials/django/

---

## ✅ Final Checklist

### Before Going Live:
- [ ] All data imported successfully
- [ ] Admin panel configured
- [ ] All views tested
- [ ] Mobile responsive verified
- [ ] Search and filters working
- [ ] Static files collected
- [ ] Database backed up
- [ ] ALLOWED_HOSTS configured
- [ ] DEBUG = False in production
- [ ] SECRET_KEY changed
- [ ] HTTPS enabled
- [ ] Custom domain configured (optional)

---

## 🎉 Congratulations!

আপনার Django-based টাঙ্গাইল ডাক্তার তালিকা ওয়েবসাইট এখন সম্পূর্ণ! 

### Next Steps:
1. Add more features (appointment booking, reviews, etc.)
2. Integrate payment gateway (if needed)
3. Add analytics (Google Analytics)
4. SEO optimization
5. Performance optimization
6. Add API endpoints for mobile app

---

**Need Help?**
- Check Django documentation
- Search Stack Overflow
- Join Django community forums

**Good Luck! 🚀**
