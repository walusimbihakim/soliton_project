import os
import dj_database_url
from django.contrib.messages import constants as messages
from decouple import config, Csv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://5bc6fd406f0946d2922e188f9d2b78d0@o419692.ingest.sentry.io/5674222",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default="127.0.0.1", cast=Csv())
PROJECT_APPS = [
    'clients',
    'projects',
    'authentication',
    'custom_errors'
]
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'crispy_forms',
    'javascript_settings',
]
INSTALLED_APPS = PROJECT_APPS + DJANGO_APPS
CRISPY_TEMPLATE_PACK = 'bootstrap3'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For heroku
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'login_required.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

ROOT_URLCONF = 'project_manager.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project_manager.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
ENVIRONMENT = config("ENVIRONMENT")
print(ENVIRONMENT)
if ENVIRONMENT == "digital_ocean":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'USER': config("POSTGRES_USER"),
            'NAME': config("POSTGRES_DB"),
            'PASSWORD': config("POSTGRES_PASSWORD"),
        },
    }
elif ENVIRONMENT == "heroku":
    # postgres database
    DATABASES = {
        'default': dj_database_url.config(default=config("POSTGRES_URI"))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
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
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Kampala'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


SENDGRID_API_KEY = config('SENDGRID_API_KEY')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

# CELERY STUFF
CELERY_TIMEZONE = config('CELERY_TIMEZONE', default="Africa/Kampala")
LOGIN_REDIRECT_URL = 'dashboard_page'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REQUIRED_IGNORE_VIEW_NAMES = [
    'logout',
    'login',
    'password_reset',
    'password_reset_done',
    'password_reset_confirm',
    'password_reset_complete',
]

AUTH_USER_MODEL = "projects.User"
