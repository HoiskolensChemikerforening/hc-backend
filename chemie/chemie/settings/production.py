from .base import *


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
