from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hc_chemie',
        'USER': 'hc_chemie',
        'PASSWORD': 'passord',
        'HOST': '127.0.0.1',
        'PORT': '5440:5432',
        'CONN_MAX_AGE': 600,
    }
}