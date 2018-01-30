"""
Django settings for the chemie project.
"""

import os


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.environ.get("DEBUG") == "False":
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
else:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'd)%%e$l#xa7xtvro#(%n)q)h$_399wth0i1^@hxrruqz$0&@zx'
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    ALLOWED_HOSTS = ['*']


# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------

ADMINS = [('Webkom', 'webkom@hc.ntnu.no'),
          ('Carl Johan Hambro', 'carljohan.hambro@gmail.com')
          ]
CONTACTS = [('Styret', 'styret@hc.ntnu.no')]


# URL CONFIGURATION
# ------------------------------------------------------------------------------

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
ROOT_URLCONF = 'chemie.urls'
WSGI_APPLICATION = 'chemie.wsgi.application'



# APP CONFIGURATION
# ------------------------------------------------------------------------------

DJANGO_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.humanize',

]
THIRD_PARTY_APPS = [
    'dal',
    'dal_select2',
    'captcha',
    'sorl.thumbnail',
    'material',
    "post_office",
    'wiki',
    'django_nyt',
    'sekizai',
    'wiki.plugins.attachments',
    'wiki.plugins.images',
    'wiki.plugins.macros',
    'mptt',
    'rest_framework',
    'rest_framework.authtoken',
    'smart_selects',
    'ckeditor',
]

LOCAL_APPS = [
    'chemie',
    'home',
    'news',
    'shitbox',
    'committees',
    'events',
    'lockers',
    'yearbook',
    'customprofile',
    'picturecarousel',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
            ],
            'loaders': ['django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader']
        },
    }
]

if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [('django.template.loaders.cached.Loader',
                                           ['django.template.loaders.filesystem.Loader',
                                            'django.template.loaders.app_directories.Loader'])]


# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db1.sqlite3'),
        }
    }
else:
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


# PASSWORD VALIDATION
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
    'hashers_passlib.phpass',
)


# INTERNATIONALIZATION
# ------------------------------------------------------------------------------

LANGUAGE_CODE = 'nb'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# STATIC FILE CONFIGURATION (CSS, JavaScript, Images)
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "chemie/static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")


# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Registration for new HC users
REGISTRATION_KEY = os.environ.get('REGISTRATION_KEY') or ''


# CAPTCHA CONFIGURATION
# ------------------------------------------------------------------------------
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or ''
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or ''

NOCAPTCHA = True


# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'post_office.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST') or ''
EMAIL_PORT = os.environ.get('EMAIL_PORT') or 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER') or ''
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') or None
DEFAULT_FROM_EMAIL = '<webkom@hc.ntnu.no> Webkom'
SERVER_EMAIL = 'webkom@hc.ntnu.no'


# WIKI CONFIGURATION
# ------------------------------------------------------------------------------

WIKI_ACCOUNT_SIGNUP_ALLOWED = False
WIKI_ANONYMOUS_WRITE = False
WIKI_ANONYMOUS_CREATE = False
WIKI_ANONYMOUS = False


# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}


# HAYSTACK CONFIGURATION
# ------------------------------------------------------------------------------

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}


# CACHE CONFIGURATION
# ------------------------------------------------------------------------------

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}


# CKEDITOR CONFIGURATION
# ------------------------------------------------------------------------------
CKEDITOR_CONFIGS = {
    'news': {
        'skin': 'bootstrapck',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', '-', 'Undo', 'Redo', '-', 'PasteText'],
            ['NumberedList', 'BulletedList', '-', 'Link'],
            ['Maximize', 'Find', 'Replace']
        ],
        'customConfig': '/static/js/ckeditor_config.js',
    },

    'events': {
        'skin': 'bootstrapck',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', '-', 'Undo', 'Redo', '-', 'PasteText'],
            ['NumberedList', 'BulletedList', '-', 'Link'],
            ['Maximize', 'Find', 'Replace']
        ],
        'customConfig': '/static/js/ckeditor_config.js',
        'extraPlugins': ','.join(
            ['specialchar']),
    },

    'committees': {
        'skin': 'bootstrapck',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', '-', 'Undo', 'Redo', '-', 'PasteText'],
            ['NumberedList', 'BulletedList', '-', 'Link'],
            ['Maximize', 'Find', 'Replace']
        ],
        'customConfig': '/static/js/ckeditor_config.js',
        'width': '100%'
    },

    'forms': {
        'skin': 'bootstrapck',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', '-', 'Undo', 'Redo', '-', 'PasteText'],
            ['NumberedList', 'BulletedList', '-', 'Link'],
            ['Maximize', 'Find', 'Replace']
        ],
        'customConfig': '/static/js/ckeditor_config.js',
        'width': '100%'
    },

    'flatpages': {
        'skin': 'bootstrapck',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak']},
            '/',
            {'name': 'styles', 'items': ['Format', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            '/',  # put this to force next toolbar on new line
        ],
        'customConfig': '/static/js/ckeditor_config.js',
        'width': '100%'
    },

}

DEFAULT_CONFIG = CKEDITOR_CONFIGS


# OTHER CONFIGURATION
# ------------------------------------------------------------------------------

GOOGLE_MAPS_API_KEY = ''

THUMBNAIL_PRESERVE_FORMAT = True
THUMBNAIL_DEBUG = False

SITE_ID = 1
INTERNAL_IPS = '127.0.0.1'
