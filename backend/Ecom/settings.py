from pathlib import Path
from decouple import config
import os

# -------------------------
# BASE SETUP
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')  # Use .env for security
DEBUG = True
ALLOWED_HOSTS = ['*']  # Allow all for local dev/testing
AUTH_USER_MODEL = 'api.CustomUser'

# -------------------------
# INSTALLED APPS
# -------------------------
INSTALLED_APPS = [
    # Local apps
    'api',
    'Ecom',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'multiselectfield',

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
    'corsheaders.middleware.CorsMiddleware',  # Must be on top for CORS
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
CORS_ALLOW_ALL_ORIGINS = True  # Allow all for local dev
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
        'NAME': config('NAME', default='ecommerce'),
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

# Optional static directory
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# You can comment this out if you don’t use extra static dirs
# Make sure this path exists if you keep it
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# -------------------------
# TEMPLATE CONFIG (NOT USED FOR DRF)
# -------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.parent / 'frontend'],
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
