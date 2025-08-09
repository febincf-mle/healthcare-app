from .base import *
from datetime import timedelta
from decouple import Config

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', cast=str),
        'USER': config('POSTGRES_USER', cast=str),
        'PASSWORD': config('POSTGRES_PASSWORD', cast=str),
        'HOST': config('POSTGRES_HOST', cast=str),
        'PORT': config('POSTGRES_PORT', cast=str),
    }
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=20)
}