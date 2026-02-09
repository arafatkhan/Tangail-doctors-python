# Production Settings Update for config/settings.py
# Add these imports at the top, after existing imports

from decouple import config, Csv
import dj_database_url
import os

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# REPLACE: SECRET_KEY = '...' 
# WITH:
SECRET_KEY = config('SECRET_KEY', default='django-insecure-g#qbaiiv=@jyaht9q7k5d0gb)9ri2n!60wx(av!*4ppb@c!qqo')

# REPLACE: DEBUG = True
# WITH:
DEBUG = config('DEBUG', default=False, cast=bool)

# REPLACE: ALLOWED_HOSTS = []
# WITH:
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================

# REPLACE entire DATABASES section WITH:
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

# UPDATE Static files section:
STATIC_URL = '/static/'
STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(BASE_DIR, 'staticfiles'))
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'doctors', 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'))

# ==============================================================================
# MIDDLEWARE - ADD WHITENOISE
# ==============================================================================

# In MIDDLEWARE list, add WhiteNoise AFTER SecurityMiddleware:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ADD THIS LINE
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==============================================================================
# WHITENOISE CONFIGURATION
# ==============================================================================

# ADD this for static files compression:
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# SECURITY SETTINGS (PRODUCTION)
# ==============================================================================

# ADD at the end of settings.py:

# CSRF/CORS Settings
CSRF_TRUSTED_ORIGINS = [
    'https://tangaildoctors.com',
    'https://www.tangaildoctors.com',
]

# Get real IP behind Cloudflare proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Production Security (only when DEBUG=False)
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

# ==============================================================================
# LOGGING CONFIGURATION (Optional but Recommended)
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/gunicorn/django-errors.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
