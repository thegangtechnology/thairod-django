"""
Django settings for thairod project.

Generated by 'django-admin startproject' using Django 2.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
from datetime import timedelta

import dj_database_url
import environ
import pytz

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET', '_!1ln^vy8@xx5c^-u8anhw(v29gk(fv^r4si_*f558k(difg!5')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'corsheaders',
    'drf_yasg',
    'rest_framework_simplejwt',
    'django_filters',
    # Custom
    'core',
    'user',
    'order_flow',
    'address',
    'warehouse',
    'product',
    'order',
    'shipment',
    'procurement',
    'stock_adjustment'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'thairod.urls'

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

WSGI_APPLICATION = 'thairod.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if os.environ.get('DB_URL') is not None:
    DATABASES = {
        'default': dj_database_url.parse(url=os.environ.get('DB_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': os.environ.get('DB_HOST'),
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
        }

    }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'thairod.utils.paginations.CustomPageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'thairod.auth_debug.DebugAuthentication'
    ]
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'
TIME_ZONE_PY = pytz.timezone(TIME_ZONE)

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SHIPPOP_API_KEY = os.environ.get('SHIPPOP_API_KEY', "")
SHIPPOP_URL = os.environ.get('SHIPPOP_URL', "https://mkpservice.shippop.dev")
SHIPPOP_DEFAULT_COURIER_CODE = os.environ.get('SHIPPOP_DEFAULT_COURIER_CODE', "SPE")
SHIPPOP_EMAIL = os.environ.get('SHIPPOP_EMAIL', "")
SHIPPOP_LOT_CUTTING_TIME = 9  # 24 hr format (9 means cut at 9 am everyday)
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', "")

LINE_ORDER_CREATED_MESSAGE = """
เรียนคุณ {name}
คำขอกล่องไทยรอดของท่านได้ถูกบันทึกแล้ว
หมายเลขคำขอของท่านคือ {order_id}
""".strip()

LINE_TRACKING_MESSAGE = """
กล่องไทยรอดกำลังถูกส่งไปให้ คุณ {name}
โดยท่านสามารถติดตามสถานะได้ที่ {tracking_url}
""".strip()

LINE_PATIENT_CONFIRM_MESSAGE = """
เรียนคุณ {name}
กรุณายืนยันที่อยู่ในการจัดส่งสำหรับกล่องไทยรอด
{patient_confirmation_url}
""".strip()

try:
    TELEMED_WHITELIST = [ip.strip() for ip in os.environ.get('TELEMED_WHITELIST', "127.0.0.1").split(',')]
except ValueError:
    TELEMED_WHITELIST = []
USE_X_FORWARDED_HOST = True
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
}

SHELL_PLUS_IMPORTS = [
    'import thairod.utils.load_seed as load_seed'
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

FRONTEND_URL = "http://localhost:3000/"
DOCTOR_HASH_EXPIRATION_SECONDS = 2 * 60 * 60  # 2 hours
PATIENT_HASH_EXPIRATION_SECONDS = 24 * 60 * 60  # 24 hours
SHIPPOP_TEST_ERR = False

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://localhost')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'rpc')

TEST_RUNNER = 'thairod.utils.test_util.ThairodTestRunner'
