from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# SENTRY CONFIGURATION
# ------------------------------------------------------------------------------
sentry_sdk.init(
    dsn="https://5ee2bfcd26c44b45a8473ec7037dedaa@sentry.io/1886982",
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)


# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "database",
        "PORT": "5432",
        "CONN_MAX_AGE": 600,
    }
}

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS")
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = False
