"""
Django settings for hindusworld project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path,os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

FILE_URL = os.getenv('File_path')

INTERNAL_IPS = [
    '127.0.0.1',
    # other internal IPs
]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mrubx$1ugvl+)ww$kay%+%f73i8640h$$y(edso%$uw3!5idt!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hindu',
    'rest_framework',
    'drf_yasg',
    "corsheaders",
    "rest_framework_simplejwt",
    "django_filters"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

AUTH_USER_MODEL = 'hindu.Register'

ROOT_URLCONF = 'hindusworld.urls'

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

WSGI_APPLICATION = 'hindusworld.wsgi.application'








# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'hindu_world1.2',
#         'USER': 'root',
#         'PASSWORD': 'admin',
#         'HOST':'localhost',
#         'PORT':'3306',
#     }
# }
DATABASE_ROUTERS = ['hindusworld.db_routers.RegisterRouter']

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE"),
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    },
    'gramadevata': {
        'ENGINE': os.getenv("LOGIN_DB_ENGINE"),
        'NAME': os.getenv("LOGIN_DB_NAME"),
        'USER': os.getenv("LOGIN_DB_USER"),
        'PASSWORD': os.getenv("LOGIN_DB_PASSWORD"),
        'HOST': os.getenv("LOGIN_DB_HOST"),
        'PORT': os.getenv("LOGIN_DB_PORT"),
    },
}

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost:8787"

]
              



# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',  # Redis server address and database index
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         },
#         'KEY_PREFIX': 'hindu',
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
# EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_PORT = os.getenv('EMAIL_PORT')
# EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sandhya.sathayush@gmail.com'
EMAIL_HOST_PASSWORD = 'isha aevi gddv xccr'
DEFAULT_FROM_EMAIL = 'sandhya.sathayush@gmail.com'




# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST='mail.sathayushtech.com'
# EMAIL_USE_TLS=False
# EMAIL_PORT=587
# OTP_EMAIL='otp@sathayushtech.com'
# OTP_EMAIL_PASSWORD='Parents++@1'
# INFO_EMAIL='infogd@sathayushtech.com'
# INFO_EMAIL_PASSWORD='Parents++@1'
# GD_FROM_EMAIL = 'gdf@sathayushtech.com'
# GD_FROM_EMAIL_PASSWORD = 'Parents++@1'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),
}

SIMPLE_JWT = {
    # how long the original token is valid for
    'ACCESS_TOKEN_LIFETIME': timedelta(days=90),

    # allow refreshing of tokens
    'JWT_ALLOW_REFRESH': True,

    # this is the maximum time AFTER the token was issued that
    # it can be refreshed.  exprired tokens can't be refreshed.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
}
 


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    }
}




SMS_USER = os.getenv('SMS_USER')
SMS_PASSWORD = os.getenv('SMS_PASSWORD')
SMS_SENDER = os.getenv('SMS_SENDER')
SMS_TYPE = os.getenv('SMS_TYPE')
SMS_TEMPLATE_ID = os.getenv('SMS_TEMPLATE_ID')
RESEND_SMS_TEMP =os.getenv('RE_SMS_TEMPLATE_ID')


FILE_URL = os.getenv('File_path')