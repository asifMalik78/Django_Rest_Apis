from .common import *   

DEBUG = True
SECRET_KEY = 'django-insecure-p7!4-q0)ta=1sp#-jjjs&)x69#o1+x#cqu#vi6bzx5cdhomjuw'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'asif@123',
    }
}

MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

CELERY_BROKER_URL = 'redis://localhost:6379/1'
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "TIMEOUT": 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = 'from@solobundle.com'