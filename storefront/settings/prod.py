import os
import dj_database_url
from .common import *

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')


DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

DJANGO_SETTINGS_MODULE = 'storefront.settings.prod'

REDIS_URL = os.environ.get('REDIS_URL')
CELERY_BROKER_URL = REDIS_URL
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT')
DEFAULT_FROM_EMAIL = "from@solobundle.com"