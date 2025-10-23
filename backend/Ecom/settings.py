from pathlib import Path
from decouple import config
import os

# -------------------------
# BASE SETUP
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')  # For local dev only
DEBUG = True
ALLOWED_HOSTS = ['*']  # Allow all for local testing

# -------------------------
# INSTALLED APPS
# -------------------------
INSTALLED_APPS = [
    # Local apps
    'Ecom',
    'api',

    # Third-party
    'rest_framework',
    'corsheaders',

    # Django built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# -------------------------
# MIDDLEWARE
# -------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be at the top for React
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------
# CORS SETTINGS
# -------------------------
CORS_ALLOW_ALL_ORIGINS = True  # ✅ Allow React on localhost
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']

# -------------------------
# URLS & WSGI
# -------------------------
ROOT_URLCONF = 'Ecom.urls'
WSGI_APPLICATION = 'Ecom.wsgi.application'

# -------------------------
# DATABASE
# -------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('NAME', default='ecom_db'),
        'USER': config('USER', default='postgres'),
        'PASSWORD': config('PASSWORD', default=''),
        'HOST': config('HOST', default='localhost'),
        'PORT': config('PORT', default='5432'),
    }
}

# -------------------------
# REST FRAMEWORK CONFIG
# -------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# -------------------------
# STATIC & MEDIA
# -------------------------
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -------------------------
# TEMPLATE CONFIG
# -------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Optional — only used if you want to serve React build later
        'DIRS': [os.path.join(BASE_DIR, 'frontend', 'build')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------------
# TIME & LANGUAGE
# -------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# -------------------------
# DEFAULTS
# -------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
