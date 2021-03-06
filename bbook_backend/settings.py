"""Django settings for the bbook_backend project.

Generated by 'dj generate init' using Django 2.0.

Based on stub code generated by 'django-admin'.

For more information on this file, see
    https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
    https://docs.djangoproject.com/en/2.0/ref/settings/

For a deployment checklist before going to production, see
    https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
"""

import os
from djx.environment import get_boolean, get_string
import dj_database_url
import logging

ALLOWED_HOSTS = []

APP = 'bbook_backend'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': (
    #         'django.contrib.auth.'
    #         'password_validation.UserAttributeSimilarityValidator'
    #     )
    # },
    # {
    #     'NAME': (
    #         'django.contrib.auth.'
    #         'password_validation.MinimumLengthValidator'
    #     )
    # },
    # {
    #     'NAME': (
    #         'django.contrib.auth.'
    #         'password_validation.CommonPasswordValidator'
    #     )
    # },
    # {
    #     'NAME': (
    #         'django.contrib.auth.'
    #         'password_validation.NumericPasswordValidator',
    #     )
    # },
]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = get_string('DATABASE_URL')

# Databases
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bbook',
        'USER': 'bbook',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_boolean('DEBUG', False)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'djx',
    'storages',
    'dynamic_rest',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'rest_auth',
    'rest_auth.registration',
    'bbook_backend',
]

# needed for rest_auth.registration
SITE_ID = 1

# for now, turn off registration email confirmation
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'en-us'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '%s.urls' % APP

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_string('DJANGO_SECRET_KEY', 'test')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

WSGI_APPLICATION = '%s.wsgi.application' % APP

AWS_STORAGE_BUCKET_NAME = get_string('BUCKET_NAME', 'b-book-test')

AWS_ACCESS_KEY_ID = get_string('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = get_string('AWS_SECRET_ACCESS_KEY', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Allow all host headers
ALLOWED_HOSTS = ['*']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    }
}

# disable boto logging
# too verbose
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
