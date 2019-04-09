DEBUG = True
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["127.0.0.1"]
THUMBNAIL_DEBUG = True
SECRET_KEY = "lk"

from .base import *

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "webkom",
        "USER": "webkom",
        "PASSWORD": "webkom",
        "HOST": "",
        "PORT": "5432",
        "CONN_MAX_AGE": 600,
    }
}
