from .base import *
import raven

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'database',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

# SENTRY CONFIGURATION
# ------------------------------------------------------------------------------
RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY'),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}