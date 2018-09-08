from .base import *

# Using in-memory email backend for testing purposes
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Using an in-memory sqlite3 database for faster testing

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hc_chemie',
        'USER': 'hc_chemie',
        'PASSWORD': 'passord',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}