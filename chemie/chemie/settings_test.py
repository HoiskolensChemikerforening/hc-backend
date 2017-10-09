from .settings import *

# Using in-memory email backend for testing purposes
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Using an in-memory sqlite3 database for faster testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
